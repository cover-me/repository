from instrument import Instrument
from time import time, sleep
import socket
import visa
import types
import logging
import math

class IPS_ethernet_20220903(Instrument):
    MARGIN = 0.0001

    def __init__(self, name, address):
        Instrument.__init__(self, name, tags=['physical'])
        
        self._address = address
        self._visainstrument = visa.instrument(self._address, term_chars = '\n')
        self._visainstrument.clear()
        
        self.add_parameter('ID', flags=Instrument.FLAG_GET, type=types.StringType)
        self.add_parameter('field', type=types.FloatType,
                flags=Instrument.FLAG_GETSET,
                units='T',
                minval=-1, maxval=1,
                format='%.5f')
                
        self.add_parameter('rampRate', type=types.FloatType,
                flags=Instrument.FLAG_GETSET,
                units='T/min',
                minval=0.0, maxval=0.1, format='%.5f')
                
        self.add_parameter('action', type=types.StringType,
                flags=Instrument.FLAG_GET)

        # Add functions
        self.add_function('get_all')
        self.get_all()
        
    def __del__(self):
        self._visainstrument.close()

    def get_all(self):
        self.get_ID()
        self.get_field()
        self.get_rampRate()
        self.get_action()
    
    def _query(self,msg):
        self._visainstrument.write(msg)
        # sleep(0.1)
        return self._visainstrument.read()

    def do_get_ID(self):
        return self._query('*IDN?\n')
        
    def do_get_field(self):
        # FSET: target field
        # FLD: most recent field
        ans = self._query('READ:DEV:GRPZ:PSU:SIG:FLD\n')
        ans = ans.split(':')[-1]
        if ans.endswith('T'):
            return float(ans[:-1])
        else:
            return None
            
    def do_set_field(self,val,wait=True):
        ans = self._query('SET:DEV:GRPZ:PSU:SIG:FSET:%s\n'%val)
        if wait:
            while math.fabs(val - self.get_field()) > self.MARGIN:
                sleep(0.050)

        return True
        
    def do_get_rampRate(self):
        ans = self._query('READ:DEV:GRPZ:PSU:SIG:RFST\n')
        ans = ans.split(':')[-1]
        if ans.endswith('T/m'):
            return float(ans[:-3])
        else:
            return None
            
    def do_set_rampRate(self,val):
        ans = self._query('SET:DEV:GRPZ:PSU:SIG:RFST:%s\n'%val)
        return True
        
        
    def do_get_action(self):
        ans = self._query('READ:DEV:GRPZ:PSU:ACTN\n')
        return ans.split(':')[-1]
