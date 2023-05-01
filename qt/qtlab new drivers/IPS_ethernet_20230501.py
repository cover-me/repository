from instrument import Instrument
from time import time, sleep
import socket
import visa
import types
import logging
import math

class IPS_ethernet_20230501(Instrument):
    MARGIN = 0.0001
    # PT1 8.3625 A/T,14 T
    MAX_FIELD = 14
    AtoB = 8.3625
    MAX_RATE = 0.15

    def __init__(self, name, address, term_chars = '\n'):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])
        
        self._address = address
        self._visainstrument = visa.instrument(self._address, term_chars = term_chars)
        self._visainstrument.clear()

        self.dict_parameters = { 
            'ID':
            {
                'get_cmd':'*IDN?',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'field': 
            {   
                'get_cmd':'READ:DEV:GRPZ:PSU:SIG:FLD',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'units':'T', 'minval':-self.MAX_FIELD, 'maxval':self.MAX_FIELD, 'format':'%.5f'}
            },
            'rampRate': 
            {   
                'get_cmd':'READ:DEV:GRPZ:PSU:SIG:RFST',
                'set_cmd':'SET:DEV:GRPZ:PSU:SIG:RFST:%s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'units':'T/min', 'minval':0.0, 'maxval':self.MAX_RATE, 'format':'%.5f'}
            },
            'action': 
            {   
                'get_cmd':'READ:DEV:GRPZ:PSU:ACTN',
                'set_cmd':'SET:DEV:GRPZ:PSU:ACTN:%s',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GETSET, 'format_map':{'HOLD':'HOLD','RTOS':'RTOS','RTOZ':'RTOZ','CLMP':'CLMP'}}
            },
           
        }
        
        # Add parameters
        self.add_parameter('Address', flags=Instrument.FLAG_GET, type=types.StringType)
        
        for i in self.dict_parameters:
            cmd = self.dict_parameters[i]['get_cmd']
            if cmd:
                func = lambda cmd=cmd: self._query(cmd)
                setattr(self, 'do_get_%s'%i, func)
            
            cmd = self.dict_parameters[i]['set_cmd']
            if cmd:
                func = lambda x,cmd=cmd: self._execute(cmd%x)
                setattr(self, 'do_set_%s'%i, func)

            self.add_parameter(i, **self.dict_parameters[i]['kw'])

        self.get_all()
        
    def close_session(self):
        self._visainstrument.close()
        
    def do_get_Address(self):
        return self._address
        
    def _execute(self, message):
        return self._visainstrument.ask(message)
        
    def _query(self, message):
        ans = self._visainstrument.ask(message)
        ans = ans.split(':')[-1]
        if message == 'READ:DEV:GRPZ:PSU:SIG:FLD':
            return ans[:-1] if ans.endswith('T') else None
        elif message == 'READ:DEV:GRPZ:PSU:SIG:RFST':
            return ans[:-3] if ans.endswith('T/m') else None
        else:
            return ans

    def get_all(self):
        self.get_Address()
        for i in self.dict_parameters:
            self.get(i)
            
    def do_set_field(self,val,wait=True):
        self._execute('SET:DEV:GRPZ:PSU:SIG:FSET:%s'%val)
        self.set_action('RTOS')# system would reset to "HOLD" once field reached
        if wait:
            while math.fabs(val - self.get('field')) > self.MARGIN:
                sleep(0.050)

        return True
        

