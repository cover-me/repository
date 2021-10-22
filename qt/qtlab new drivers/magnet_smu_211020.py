# modified by Po on 09/27/2021
# OxfordInstruments_IPS120.py class, to perform the communication between the Wrapper and the device
# Guenevere Prawiroatmodjo <guen@vvtp.tudelft.nl>, 2009
# Pieter de Groot <pieterdegroot@gmail.com>, 2009
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from instrument import Instrument
from time import time, sleep
import visa
import types
import logging
import math

class magnet_smu_211020(Instrument):
    '''
    This is the python driver for the Oxford Instruments IPS 120 Magnet Power Supply

    Usage:
    Initialize with
    <name> = instruments.create('name', 'OxfordInstruments_IPS120_gpib', address='<Instrument address>')
    <Instrument address> = 

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
        self._visainstrument = visa.instrument(self._address, term_chars = '\r')
        self._visainstrument.clear()
        self.FIELD_TO_CURRENT = 1./0.0510#A/T, 0.0510 for side, 4.9675 for DR200 8T magnet
        self._values = {}

        #Add parameters
        MAX_I = 0.105                     
        # for 6430, the current limit is +/- 100 mA                                           
        self.add_parameter('field', type=types.FloatType,
            flags=Instrument.FLAG_GETSET,
            minval=-MAX_I/self.FIELD_TO_CURRENT, maxval=MAX_I/self.FIELD_TO_CURRENT,
            maxstep=2e-5, stepdelay=30, units='T',tags=['sweep'])
        self.add_parameter('current_setpoint', type=types.FloatType,
            flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET,
            minval=-MAX_I, maxval=MAX_I,
            maxstep=0.001, stepdelay=30, units='A',tags=['sweep'])
        self.add_parameter('I_range', type=types.FloatType,
            flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET,
            minval=1e-12, maxval=0.1, units='A')
        self.add_parameter('rampRate', type=types.FloatType,
            flags=Instrument.FLAG_GET,
            minval=0, maxval=14)
        self.add_parameter('ID', flags=Instrument.FLAG_GET, type=types.StringType)
        self.get_all()

    # Functions
    def _execute(self, message):
        logging.info(__name__ + ' : Send the following command to the device: %s' % message)
        self._visainstrument.write('%s' % (message))
        
    def _query(self, message):
        logging.info(__name__ + ' : Send the following command to the device: %s' % message)
        self._visainstrument.write('%s' % (message))
        result = self._visainstrument.read()
        return result

    def get_all(self):                                                  ### Run this command after interupted the measurements.
        self.get_ID()
        self.get_field()
        self.get_current_setpoint()		
        self.get_rampRate()
        self.get_I_range()                                                                                                                               

    def do_set_current_setpoint(self, current):
        logging.info(__name__ + ' : set output current to %s'%current)
        self._execute(':SOUR:CURR %s'%current)
        
    def do_get_current_setpoint(self):
        logging.info(__name__ + ' : get output current')
        ans = self._query(':READ?')
        return float(ans.split(',')[1])
        
    def do_set_field(self, field):
        logging.info(__name__ + ' : set output field to %s'%field)
        current  = field*self.FIELD_TO_CURRENT
        self._execute(':SOUR:CURR %s'%current)
        
    def do_get_field(self):
        logging.info(__name__ + ' : get output field')
        cur = self.do_get_current_setpoint()
        return cur/self.FIELD_TO_CURRENT
        
    def do_set_I_range(self, i_range):
        logging.info(__name__ + ' : set output current range to %s'%i_range)
        self._execute(':SOUR:CURR:RANG %s'%i_range)
        self.do_get_I_range()

    def do_get_I_range(self):
        logging.info(__name__ + ' : get output current range')
        return float(self._query(':SOUR:CURR:RANG?'))    
    
    def do_get_ID(self):
        ans = self._query('*IDN?')
        return ans
    
    def do_get_rampRate(self):
        return 0



