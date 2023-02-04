from instrument import Instrument
from time import time, sleep
import visa
import types
import logging
import math

class GS210_20221001(Instrument):

    
    def __init__(self, name, address):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])
        self._address = address
        self._visainstrument = visa.instrument(self._address, term_chars = '\r')
        self._visainstrument.clear()
                                          
        self.add_parameter('ID', flags=Instrument.FLAG_GET, type=types.StringType)
        self.add_parameter('address', flags=Instrument.FLAG_GET, type=types.StringType)
        self.add_parameter('source_type', type=types.StringType, flags=Instrument.FLAG_GET)
        self.add_parameter('source_range', type=types.FloatType, flags=Instrument.FLAG_GET)
        self.add_parameter('source_level', type=types.FloatType, flags=Instrument.FLAG_GETSET, maxstep=0.001, stepdelay=30, units='')

        self.get_all()

    # Functions
    def _execute(self, message):
        self._visainstrument.write('%s' % (message))
        
    def _query(self, message):
        self._visainstrument.write('%s' % (message))
        result = self._visainstrument.read()
        return result

    def get_all(self):                                                  ### Run this command after interupted the measurements.
        self.get_ID()
        self.get_address()
        self.get_source_type()
        self.get_source_range()
        self.get_source_level()

    def do_get_ID(self):
        return self._query('*IDN?')

    def do_get_address(self):
        return self._address
        
    def do_get_source_type(self):
        return self._query('SOURce:FUNC?')
        
    def do_get_source_range(self):
        return float(self._visainstrument.ask(':SOURce:RANGe?'))
        
    def do_get_source_level(self):
        return float(self._query('SOUR:LEV?'))
        
    def do_set_source_level(self,lvl):
        return self._execute('SOUR:LEV %s'%lvl)





