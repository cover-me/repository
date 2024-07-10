import pandas as pd
import contextlib
import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

import qcodes as qc
from qcodes.utils.dataset.doNd import do1d, do2d, dond, plot, LinSweep, LogSweep
from qcodes.dataset.sqlite.database import initialise_or_create_database_at
from qcodes.dataset.experiment_container import load_or_create_experiment
from qcodes.tests.instrument_mocks import DummyInstrument, DummyInstrumentWithMeasurement
from qcodes.dataset.measurements import Measurement
from qcodes.dataset.plotting import plot_dataset
from qcodes.instrument.parameter import Parameter


class TrigQDAC:
    '''
    Setup qdac triggers for fast sacan
    '''
    
    def __init__(self,dac,ch,trg_out=1,trg_in=1,trg_internal=1):
        self.dac = dac
        self.ch_source = ch# output-source channel (0,1,2...)

        self.ch_trig_out = trg_out# output trigger on front panel
        self.ch_trig_in = trg_in# input trigger on back panel
        self.ch_trig_internal = trg_internal# internal trigger used
        
    def initialize_sweep(self, v_list):
        # TODO: check the validation of the v_list

        # Padding with v0 and v1 
        # Add the reverse list for bi-directional scans 
        v0, v1 = v_list[0], v_list[-1]
        volt_list = np.hstack((v_list, v1, v_list[::-1], v0))

        self.dac.write(f'sour{self.ch_source}:dc:trig:sour hold')
        
        # config sweep list
        self.dac.write(f'sour{self.ch_source}:volt:mode list')
        self.dac.visa_handle.write_binary_values(f'sour{self.ch_source}:list:volt ', volt_list)
        
        # trigger mode -> step: one step, one trigger.
        self.dac.write(f'sour{self.ch_source}:list:tmod step')
        # the dwel time must be less than the trigger interval or the step would not be advanced
        self.dac.write(f'sour{self.ch_source}:list:dwel {1e-4}')
        # trigger delay
        self.dac.write(f'sour{self.ch_source}:dc:del {0}')
        self.dac.write(f'sour{self.ch_source}:list:dir up')
        self.dac.write(f'sour{self.ch_source}:list:coun 1')

        # config output trigger
        # link output channel 1 to internal channel 1
        self.dac.write(f'outp:trig{self.ch_trig_out}:sour int{self.ch_trig_internal}')
        # pulse width in seconds
        self.dac.write(f'outp:trig{self.ch_trig_out}:widt {10e-06}')

        # wait for trigger
        self.dac.write(f'sour{self.ch_source}:dc:trig:sour ext{self.ch_trig_in}')
        # continuous tiggger on so it can be triggerred for infinite times (v0, v1, .., vn -> v0, v1, ...)
        self.dac.write(f'sour{self.ch_source}:dc:init:cont on')
        self.dac.write(f'sour{self.ch_source}:dc:init')
    

    def fire_sweep(self):

        # ask something to make sure the device is ressponsive
        # self.dac.ask(f'sour{ch_source}:list:poin?')
        self.dac.write(f'TINT {self.ch_trig_internal}')
        # (re)link the event to the internal trigger otherwise the link is lost after the last command
        self.dac.write(f'sour{self.ch_source}:dc:mark:sst {self.ch_trig_internal}')

    def back_to_no_trig(self):
        print('Setting qdac back to no trigger and fixed voltage...')
        self.dac.write(f'sour{self.ch_source}:dc:trig:sour hold')
        self.dac.write(f'sour{self.ch_source}:volt:mode fix')


class TrigDMM:

    def __init__(self,dmm,nplc=0.2):
        self.dmm = dmm
        self.nplc = nplc
    
    def initialize_meas(self, v_list, trig_delay=0):
        num_points = len(v_list)
        num = num_points + 1

        # if not idle, set to idle
        if not self.is_idle():
            self.dmm.visa_handle.clear()
            self.dmm.abort_measurement()
            # there must be a delay
            time.sleep(0.1)

        self.dmm.NPLC(self.nplc)
        self.dmm.autorange('OFF')
        self.dmm.autozero('OFF')

        # output trigger (VM comp port) slope
        self.dmm.write('OUTPut:TRIGger:SLOPe POS')

        # trigger source
        self.dmm.trigger.source('EXT')
        self.dmm.trigger.slope('POS')
        # this delay applies to every "sample"
        self.dmm.trigger.delay(trig_delay)
        self.dmm.sample.count(1)
        self.dmm.trigger.count(num)

        # it may takes a long time before the sweep finishes
        self.dmm.timeout((0.02*self.nplc+trig_delay)*num*5)
        
    def enter_meas(self):
        self.dmm.init_measurement()
        # ask something to measure the initialization finishes and dmm is responsive, otherwise dmm will igore the first trigger 
        self.dmm.NPLC()

    def back_to_auto_trig(self):
        print('Setting dmm back to auto trig mode (if failed, run it once more)...')

        # necessary if there was a failed fetch
        try:
            self.dmm.timeout(0.5)
            self.dmm.NPLC()
        except:
            self.dmm.visa_handle.clear()
            time.sleep(1)
        # to idle mode
        self.dmm.abort_measurement()
        # there must be a delay
        time.sleep(1)

        self.dmm.NPLC(self.nplc)
        self.dmm.autorange('OFF')
        self.dmm.autozero('OFF')

        self.dmm.trigger.source('IMM')
        self.dmm.trigger.slope('POS')
        self.dmm.trigger.delay(0)
        self.dmm.sample.count(1)
        self.dmm.trigger.count(1)

        self.dmm.timeout(5)

        self.dmm.init_measurement()

    def is_idle(self):
        # standard operation regist, 0: calibrating, 4: Measuring, 5: Waiting for Trig, ..., 13: Blobal error
        sor = int(self.dmm.ask('STATus:OPERation:CONDition?'))
        sor = bin(sor)
        sor = sor[2:]
        sor = sor.zfill(16)
        is_waiting_trig = sor[-6] == '1'
        return not is_waiting_trig
    
    def fetch(self):
        d = self.dmm.fetch()
        return d

