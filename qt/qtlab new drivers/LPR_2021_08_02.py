# 2021-02-01: Add feature: set heater currents
# 20190721
# 02/02/2018 Po
# (L)eidon (P)rogram (R)eader for qtlab
# how to use:
#   1. make sure the qtlab PC and the Leidon PC are in the same local LAN (both connect to WIRELESS-PITTNET, for example)
#   2. Run L_messanger.exe (on either PC). This exe talks between qtlab and the Leidon program.
#   3. Put this file in folder instrument_plugins. In file 80_create_instruments.py, add or in qtlab cmd, run:
#        print 'Create (L)eidon (P)rogram (R)eader'
#        fridge = qt.instruments.create('LPR','LPR',address='TCPIP0::10.215.142.232::6340::SOCKET'), the ip address may vary.


from instrument import Instrument
from time import time, sleep
import visa
import types
import logging

class LPR_2021_08_02(Instrument):
    '''
    This is the python driver for the Oxford Instruments IPS 120 Magnet Power Supply

    Usage:
    Initialize with
    <name> = instruments.create('name', 'OxfordInstruments_IPS120', address='<Instrument address>')
    <Instrument address> = ASRL1::INSTR

    Note: Since the ISOBUS allows for several instruments to be managed in parallel, the command
    which is sent to the device starts with '@n', where n is the ISOBUS instrument number.

    '''
#TODO: auto update script
#TODO: get doesn't always update the wrapper! (e.g. when input is an int and output is a string)

    def __init__(self, name, address):
        '''
        Initializes the Oxford Instruments IPS 120 Magnet Power Supply.

        Input:
            name (string)    : name of the instrument
            address (string) : instrument address
            number (int)     : ISOBUS instrument number

        Output:
            None
        '''
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])


        self._address = address
        self._visainstrument = visa.instrument(self._address,term_chars="\r\n")

        #Add parameters
        self.add_parameter('3K', type=types.FloatType,
            flags=Instrument.FLAG_GET,units='K')
        self.add_parameter('still', type=types.FloatType,
            flags=Instrument.FLAG_GET,units='K')
        self.add_parameter('cold', type=types.FloatType,
            flags=Instrument.FLAG_GET,units='K')
        self.add_parameter('MC', type=types.FloatType,
            flags=Instrument.FLAG_GET,units='K')
        self.add_parameter('R_3K', type=types.FloatType,
            flags=Instrument.FLAG_GET,units='kohm')
        self.add_parameter('R_still', type=types.FloatType,
            flags=Instrument.FLAG_GET,units='kohm')
        self.add_parameter('R_cold', type=types.FloatType,
            flags=Instrument.FLAG_GET,units='kohm')
        self.add_parameter('R_MC', type=types.FloatType,
            flags=Instrument.FLAG_GET,units='kohm')
        self.add_parameter('I_list', type=types.ListType,
            flags=Instrument.FLAG_SET,units='uA or mK')
        # Add functions
        self.add_function('get_all')
        sleep(5)
        self.get_all()

    def get_all(self):
        '''
        Reads all implemented parameters from the instrument,
        and updates the wrapper.

        Input:
            None

        Output:
            None
        '''
        logging.info(__name__ + ' : reading all settings from instrument')
        self.get_3K()
        self.get_still()
        self.get_cold()
        self.get_MC()
        self.get_R_3K()
        self.get_R_still()
        self.get_R_cold()
        self.get_R_MC()
        
    # Functions
    def _execute(self, message):
        '''
        Write a command to the device

        Input:
            message (str) : write command for the device

        Output:
            None
        '''
        logging.info(__name__ + ' : Send the following command to the device: %s' % message)
        self._visainstrument.write(message)
        sleep(5e-3) # wait for the device to be able to respond
        result = self._visainstrument.read()
        return result

    def do_get_3K(self):
        result = self._execute('0')
        return float(result)
        
    def do_get_still(self):
        result = self._execute('1')
        return float(result)
        
    def do_get_cold(self):
        result = self._execute('2')
        return float(result)
        
    def do_get_MC(self):
        result = self._execute('3')
        return float(result)

    def do_get_R_3K(self):
        result = self._execute('10')
        return float(result)
        
    def do_get_R_still(self):
        result = self._execute('11')
        return float(result)
        
    def do_get_R_cold(self):
        result = self._execute('12')
        return float(result)
        
    def do_get_R_MC(self):
        result = self._execute('13')
        return float(result)

    def do_set_I_list(self,i_list):
        if len(i_list) == 4 and all([i<=25000 for i in i_list]):
            i_list = ['%g'%i for i in i_list]
            result = self._execute('SET '+','.join(i_list))
        else:
            print 'A wrong list. Nothing has been done.'
