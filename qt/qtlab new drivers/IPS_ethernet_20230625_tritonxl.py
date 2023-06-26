# https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers

from instrument import Instrument
from time import time, sleep
import visa
import types
import logging
import math
import msvcrt

class IPS_ethernet_20230625_tritonxl(Instrument):
    MARGIN = 1e-3# T
    MARGIN_CHECK_ACTION = True
    # Check the power suppley settings
    # PT1 8.3625 A/T,14 T
    # TritonXL 8.7399 A/T, 16 T
    MAX_FIELD = 16
    MAX_RATE = 0.2

    def __init__(self, name, address, term_chars = '\n', timeout=2):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['magnet'])
        print '%-15s\t%-35s\t%-15s'%(name, address, self.__module__)
        
        self._address = address
        self._visainstrument = visa.instrument(self._address, term_chars = term_chars, timeout=timeout)
        self._visainstrument.clear()
        self._initialize_parameters()
        self.get_all()
        # qt.flow.connect('measurement-start', self._measurement_start_cb)
        # qt.flow.connect('measurement-end', self._measurement_end_cb)

    def _initialize_parameters(self):
        # Parameters that are class attributes 
        self.attribute_parameters = ['_address', '__module__']
        
        # type, flags, units, doc, minval, maxval, format_map
        self.dict_parameters = {
            'ID':
            {
                'get_cmd':'*IDN?',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'margin':
            {
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'units':'T'}
            },
            'margin_check_action':
            {
                'kw':{'type':types.BooleanType,'flags':Instrument.FLAG_GETSET}
            },
            'field': 
            {   
                'get_cmd':'READ:DEV:GRPZ:PSU:SIG:FLD',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'units':'T', 'minval':-self.MAX_FIELD, 'maxval':self.MAX_FIELD}
            },
            'field_rate': 
            {   
                'get_cmd':'READ:DEV:GRPZ:PSU:SIG:RFST',
                'set_cmd':'SET:DEV:GRPZ:PSU:SIG:RFST:%s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'units':'T/min', 'minval':0.0, 'maxval':self.MAX_RATE}
            },
            'action': 
            {   
                'get_cmd':'READ:DEV:GRPZ:PSU:ACTN',
                'set_cmd':'SET:DEV:GRPZ:PSU:ACTN:%s',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GETSET, 'format_map':{'HOLD':'HOLD','RTOS':'RTOS','RTOZ':'RTOZ','CLMP':'CLMP'}}
            },
           
        }
        self._add_parameters()# add attribute_parameters and dict_parameters
        self.set_margin(self.MARGIN)
        self.set_margin_check_action(self.MARGIN_CHECK_ACTION)
   
    def _add_parameters(self):
        '''
        Add parameters from class attributes and parameter dictionary
        '''
        # Add attribute parameters
        for i in self.attribute_parameters:
            para_name = i.strip('_').upper()
            func = lambda attr_name=i: getattr(self,attr_name) 
            setattr(self, 'do_get_%s'%para_name, func)
            self.add_parameter(para_name, flags=Instrument.FLAG_GET, type=types.StringType)
            
        self._add_parameters_from_dict(self.dict_parameters)
        
    def _add_parameters_from_dict(self,para_dict):
        # Add other parameters
        for i in para_dict:
            # A virtual parameter
            if 'get_cmd' not in para_dict[i] and 'set_cmd' not in para_dict[i]:
                func = lambda name='_%s'%i: getattr(self,name)
                setattr(self, 'do_get_%s'%i, func)
                
                func = lambda x,name='_%s'%i: setattr(self,name,x)
                setattr(self, 'do_set_%s'%i, func)
                
                self.add_parameter(i, **para_dict[i]['kw'])
            # An instrument parameter
            else:
                cmd = para_dict[i]['get_cmd']
                if cmd:
                    func = lambda cmd=cmd,flag=0: self._query(cmd,flag)
                    setattr(self, 'do_get_%s'%i, func)
                
                cmd = para_dict[i]['set_cmd']
                if cmd:
                    func = lambda x,cmd=cmd: self._execute(cmd%x)
                    setattr(self, 'do_set_%s'%i, func)

                self.add_parameter(i, **para_dict[i]['kw'])
        
    def close_session(self):
        self._visainstrument.close()
        
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
        for i in self.get_parameters():
            self.get(i)
            
    def do_set_field(self,val,wait=True):
        self._execute('SET:DEV:GRPZ:PSU:SIG:FSET:%s'%val)
        self.set_action('RTOS')# system would reset to "HOLD" once field reached
        if wait:
            try:
                while abs(val - self.get_field()) > self._margin or (self._margin_check_action and self.get_action() != 'HOLD'):
                    self._do_emit_changed()# update the GUI
                    self._check_last_pressed_key()
                    sleep(0.050)
            except KeyboardInterrupt:
                self.set_action('HOLD')
                raise KeyboardInterrupt
        return True

    def _check_last_pressed_key(self):
        last_key = ''
        while msvcrt.kbhit():
           last_key = msvcrt.getch()
        if last_key == '\x05':#ctrl+e(xit)
            raise KeyboardInterrupt

    # def _measurement_start_cb(self, sender):
        # pass

    # def _measurement_end_cb(self, sender):
        # pass
