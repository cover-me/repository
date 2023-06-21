from instrument import Instrument
from time import sleep
import socket
import msvcrt
import visa
import types
import logging
# import math

class IPS_ethernet_20230529_tritonxl(Instrument):
    MARGIN = 1e-3# T
    # PT1 8.3625 A/T,14 T
    # TritonXL 8.7399, 16
    MAX_FIELD = 16
    AtoB = 8.7399
    MAX_RATE = 0.2

    def __init__(self, name, address, term_chars = '\n'):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])
        print '%-15s\t%-35s\t%-15s'%(name, address, self.__module__)
        
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
            'margin':
            {
                'get_cmd':'',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'units':'T'}
            },
            'field': 
            {   
                'get_cmd':'READ:DEV:GRPZ:PSU:SIG:FLD',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'units':'T', 'minval':-self.MAX_FIELD, 'maxval':self.MAX_FIELD, 'format':'%.5f'}
            },
            'field_rate': 
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
                func = lambda cmd=cmd,flag=0: self._query(cmd,flag)
                setattr(self, 'do_get_%s'%i, func)
            
            cmd = self.dict_parameters[i]['set_cmd']
            if cmd:
                func = lambda x,cmd=cmd: self._execute(cmd%x)
                setattr(self, 'do_set_%s'%i, func)

            self.add_parameter(i, **self.dict_parameters[i]['kw'])

        self.set_margin(self.MARGIN)
        self.get_all()
        
        
    def close_session(self):
        self._visainstrument.close()
        
    def do_get_Address(self):
        return self._address
        
    def _execute(self, message):
        return self._visainstrument.ask(message)
        
    def _parse(self, ans, message):
        ans = ans.split(':')[-1]
        if message == 'READ:DEV:GRPZ:PSU:SIG:FLD':
            return ans[:-1] if ans.endswith('T') else None
        elif message == 'READ:DEV:GRPZ:PSU:SIG:RFST':
            return ans[:-3] if ans.endswith('T/m') else None
        elif message == 'READ:DEV:MB1.T1:TEMP:SIG:TEMP':
            return ans[:-1]
        else:
            return ans

    def _query(self, message, flag=0):
        '''
        flag, 0 (default): write command and read respond, 1: write only, 2: read only
        The reading can be non-atomic with the parameter flag
        '''
        if  flag != 2:
            self._visainstrument.write(message)
        if flag != 1:
            ans = self._visainstrument.read()
            return self._parse(ans,message)
        return None
        
    def get_all(self):
        self.get_Address()
        for i in self.dict_parameters:
            self.get(i)
            
    def do_set_field(self,val,wait=True):
        self._execute('SET:DEV:GRPZ:PSU:SIG:FSET:%s'%val)
        self.set_action('RTOS')# system would reset to "HOLD" once field reached
        if wait:
            try:
                while abs(val - self.get_field()) > self.MARGIN or self.get_action() != 'HOLD':
                    self._do_emit_changed()# update the GUI
                    self._check_last_pressed_key()
                    sleep(0.050)
            except KeyboardInterrupt:
                self.set_action('HOLD')
                raise KeyboardInterrupt
        return True

    def do_set_margin(self, x):
        self.margin = x
        
    def do_get_margin(self):
        return self.margin
        
    def _check_last_pressed_key(self):
        last_key = ''
        while msvcrt.kbhit():
           last_key = msvcrt.getch()
        if last_key == '\x05':#ctrl+e(xit)
            raise KeyboardInterrupt
