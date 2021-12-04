# Last modified by Po on 12/03/2021, to use it in center fridge.

from instrument import Instrument
from time import time, sleep
import visa
import types
import logging
import math

class magnet_E3632A(Instrument):
    
    def __init__(self, name, address):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])
        self._address = address
        self._visainstrument = visa.instrument(self._address)
        self._visainstrument.clear()
        self.FIELD_TO_CURRENT = 1/0.01463#A/T, 4.9675 for DR200 8T magnet (not in the fridge any more),  1./0.0510 for side fridge Bx
        self._values = {}

        #Add parameters
        MAX_I = 0.105
        # for 6430, the current limit is +/- 100 mA
        
        self.add_parameter('field', type=types.FloatType,
            flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET,
            minval=-MAX_I/self.FIELD_TO_CURRENT, maxval=MAX_I/self.FIELD_TO_CURRENT,
            maxstep=2e-5, stepdelay=30, units='T',tags=['sweep'])
            
        self.add_parameter('current_setpoint', type=types.FloatType,
            flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET,
            minval=-MAX_I, maxval=MAX_I,
            maxstep=0.001, stepdelay=30, units='A',tags=['sweep'])

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

    def get_all(self):
        self.get_ID()
        self.get_field()
        self.get_current_setpoint()		
        self.get_rampRate()

    def do_set_current_setpoint(self, current):
        self._execute('CURR %.4f'%current)
        
    def do_get_current_setpoint(self):
        ans = self._query('CURR?')
        return float(ans)
        
    def do_set_field(self, field):
        current  = field*self.FIELD_TO_CURRENT
        self._execute('CURR %.4f'%current)
        
    def do_get_field(self):
        cur = self.do_get_current_setpoint()
        return cur/self.FIELD_TO_CURRENT

    def do_get_ID(self):
        ans = self._query('*IDN?')
        return ans
    
    def do_get_rampRate(self):
        return 0



