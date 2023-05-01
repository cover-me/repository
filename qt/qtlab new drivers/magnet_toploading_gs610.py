# Last modified by Po on 12/21/2021, to use it in center fridge By (or Bx) with GS210.


from instrument import Instrument
from time import time, sleep
import visa
import types
import logging
import math

class magnet_toploading_gs610(Instrument):
    
    def __init__(self, name, address):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])
        self._address = address
        self._visainstrument = visa.instrument(self._address)
        self._visainstrument.clear()
        self.FIELD_TO_CURRENT = 0.910/0.1#A/T
        self._values = {}

        #Add parameters
        MAX_I = 3.2

        self.add_parameter('field', type=types.FloatType,
            flags=Instrument.FLAG_GETSET,
            minval=-MAX_I/self.FIELD_TO_CURRENT, maxval=MAX_I/self.FIELD_TO_CURRENT,
            maxstep=2e-5, stepdelay=30, units='T')
        self.add_parameter('current_setpoint', type=types.FloatType,
            flags=Instrument.FLAG_GETSET,
            minval=-MAX_I, maxval=MAX_I,
            maxstep=0.002, stepdelay=30, units='A')
        self.add_parameter('I_range', type=types.FloatType,
            flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET,
            minval=1e-12, maxval=3.2, units='A')
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
        self._execute(':SOUR:CURR:LEV %s'%current)
        
    def do_get_current_setpoint(self):
        logging.info(__name__ + ' : get output current')
        ans = self._query(':SOUR:CURR:LEV?')
        return float(ans)
        
    def do_set_field(self, field):
        logging.info(__name__ + ' : set output field to %s'%field)
        current  = field*self.FIELD_TO_CURRENT
        self._execute(':SOUR:CURR:LEV %s'%current)
        
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



