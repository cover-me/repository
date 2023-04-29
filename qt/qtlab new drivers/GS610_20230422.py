from instrument import Instrument
from time import time, sleep
import visa
import types
import logging
import math

class GS610_20230422(Instrument):

    
    def __init__(self, name, address):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])
        self._address = address
        self._visainstrument = visa.instrument(self._address)
        self._visainstrument.clear()
                                          
        self.add_parameter('ID', flags=Instrument.FLAG_GET, type=types.StringType)
        self.add_parameter('address', flags=Instrument.FLAG_GET, type=types.StringType)
        self.add_parameter('source_type', type=types.StringType, flags=Instrument.FLAG_GET)
        self.add_parameter('source_v_range', type=types.FloatType, flags=Instrument.FLAG_GET)
        self.add_parameter('source_v_level', type=types.FloatType, flags=Instrument.FLAG_GETSET, maxstep=0.001, stepdelay=30, units='')
        
        self.add_parameter('sense_type', type=types.StringType, flags=Instrument.FLAG_GET)
        self.add_parameter('val', type=types.FloatType, flags=Instrument.FLAG_GET)

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
        self.get_source_v_range()
        self.get_source_v_level()
        self.get_sense_type()
        self.get_val()

    def do_get_ID(self):
        return self._query('*IDN?')

    def do_get_address(self):
        return self._address
        
    def do_get_source_type(self):
        return self._query('SOURce:FUNC?')
        
    def do_get_source_v_range(self):
        return float(self._visainstrument.ask(':SOURce:VOLTage:RANGe?'))
        
    def do_get_source_v_level(self):
        return float(self._query('SOUR:VOLTage:LEV?'))
        
    def do_set_source_v_level(self,lvl):
        return self._execute('SOUR:VOLTage:LEV %s'%lvl)
        
    def do_get_sense_type(self):
        return self._query('sense:FUNC?')
        
    def do_get_val(self):
        return float(self._query('FETCh?'))





