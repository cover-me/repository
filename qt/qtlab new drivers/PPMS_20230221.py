# https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers

from instrument import Instrument
from time import sleep
import visa
import types
import logging
import math

class PPMS_20230221(Instrument):

    def __init__(self, name, address):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])
        self.B_MARGIN = 0.0001
        self.T_MARGIN = 0.001
        self.SLEEP_TIME = 0.050
        
        self._address = address
        self._visainstrument = visa.instrument(self._address, term_chars = '\n')
        self._visainstrument.clear()
        
        self.add_parameter('ID', flags=Instrument.FLAG_GET, type=types.StringType)
        self.add_parameter('Address', flags=Instrument.FLAG_GET, type=types.StringType)
        
        # self.add_parameter('something', type=types.FloatType, flags=Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET, maxstep=1e-3, stepdelay=30, units='V')
        self.add_parameter('temp', type=types.FloatType, flags=Instrument.FLAG_GETSET,units='K', minval = 1.6, maxval = 400)
        self.add_parameter('temp_rate', type=types.FloatType, flags=Instrument.FLAG_GETSET,units='K/min', minval = 0.01, maxval = 10)
        self.add_parameter('field', type=types.FloatType, flags=Instrument.FLAG_GETSET,units='T',  minval = -14, maxval = 14)
        self.add_parameter('field_rate', type=types.FloatType, flags=Instrument.FLAG_GETSET,units='T/min', minval = 0, maxval = 0.72)
        self.get_all()

    def _execute(self, message):
        self._visainstrument.write('%s\n'%(message))
        
    def _query(self, message):
        return self._visainstrument.ask('%s\n'%message)

    def get_all(self):
        self.get_ID()
        self.get_Address()
        self.get_temp()
        self.set_temp_rate(10)
        self.get_field()
        self.set_field_rate(0.3)


    # getting and setting functions
    def do_get_ID(self):# ID
        ans = self._query('*IDN?')
        ans = ans.split(', ')[1:3]
        ans = ', '.join(ans)
        return ans

    def do_get_Address(self):# Address
        return self._address
        
    def do_get_temp(self):# temp
        error, status, reading = self._query('TEMP?').split(', ')
        return float(reading)
        
    def do_set_temp(self, t, wait=True):# temp
        r = self.get_temp_rate()
        approach = 0
        self._query('TEMP %s, %s, %i'%(t, r, approach))
        
        if wait:
            while abs(t - self.get_temp()) > self.T_MARGIN:
                sleep(self.SLEEP_TIME)

        return True
        
        
    def do_set_temp_rate(self, r):# temp_rate
        pass
        
    def do_get_temp_rate(self):# temp_rate
        return self.get_parameters()['temp_rate']['value']

    def do_get_field(self):# field
        error, status, reading = self._query('FELD?').split(', ')
        return float(reading)/1.e4
        
    def do_set_field(self, b_tesla, wait=True):# field
        h_oe = b_tesla * 1.e4
        rate_tesla_min = self.get_field_rate()
        rate_oe_s = rate_tesla_min*1.e4/60.
        approach = 0
        mode = 0
        self._query('FELD %s, %s, %i, %i'%(h_oe, rate_oe_s, approach, mode))
        if wait:
            while abs(b_tesla - self.get_field()) > self.B_MARGIN:
                sleep(self.SLEEP_TIME)

        return True

    def do_set_field_rate(self, r):# field_rate
        pass
        
    def do_get_field_rate(self):# field_rate
        return self.get_parameters()['field_rate']['value']



