from instrument import Instrument
from time import time, sleep
import visa
import types
import logging
import math
import msvcrt

class tritonxl_20230625(Instrument):
    MARGIN = 5e-3# K

    def __init__(self, name, address,  term_chars = '\n'):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])
        print '%-15s\t%-35s\t%-15s'%(name, address, self.__module__)
        
        self._address = address
        self._visainstrument = visa.instrument(self._address, term_chars = term_chars, timeout=10)
        self._visainstrument.clear()
        self._initialize_parameters()
        self.set_margin(self.MARGIN)
        self.get_all()
        
    def _initialize_parameters(self):
        # Parameters that are class attributes
        self.attribute_parameters = ['_address', '__module__']
        
        self.dict_parameters = { 
            'ID':
            {
                'get_cmd':'*IDN?',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            't_mc_cernox': 
            {   
                'get_cmd':'READ:DEV:T9:TEMP:SIG:TEMP',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GET,'units':'K'}
            },
            't_still':
            {   
                'get_cmd':'READ:DEV:T3:TEMP:SIG:TEMP',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GET,'units':'K'}
            },
            't_cold': 
            {   
                'get_cmd':'READ:DEV:T4:TEMP:SIG:TEMP',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GET,'units':'K'}
            },
            't_magnet': 
            {   
                'get_cmd':'READ:DEV:T13:TEMP:SIG:TEMP',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GET,'units':'K'}
            },
            'dr_action': 
            {   
                'get_cmd':'READ:SYS:DR:ACTN',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'dr_status': 
            {   
                'get_cmd':'READ:SYS:DR:STATUS',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            
            'margin':
            {
                'get_cmd':'',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'units':'K'}
            },
            't_mc': 
            {   
                'get_cmd':'READ:DEV:T12:TEMP:SIG:TEMP',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'units':'K'}
            },

            'loop_range': 
            {   
                'get_cmd':'READ:DEV:T12:TEMP:LOOP:RANGE',
                'set_cmd':'SET:DEV:T12:TEMP:LOOP:RANGE:%s',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'units':'mA'}
            },
            'loop_ramp_enable': 
            {   
                'get_cmd':'READ:DEV:T12:TEMP:LOOP:RAMP:ENAB',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'loop_ramp_rate': 
            {   
                'get_cmd':'READ:DEV:T12:TEMP:LOOP:RAMP:RATE',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'loop': 
            {
                'get_cmd':'READ:DEV:T12:TEMP:LOOP:MODE',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'loop_pid':
            {   
                'get_cmd':'READ:DEV:T12:TEMP:LOOP:P:I:D',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'loop_filter_enable': 
            {   
                'get_cmd':'READ:DEV:T12:TEMP:LOOP:FILT:ENAB',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'pt1_state': 
            {   
                'get_cmd':'READ:DEV:C1:PTC:SIG:STATE',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'pt1_water_in': 
            {   
                'get_cmd':'READ:DEV:C1:PTC:SIG:WIT',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'pt1_water_out': 
            {   
                'get_cmd':'READ:DEV:C1:PTC:SIG:WOT',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'pt2_state': 
            {   
                'get_cmd':'READ:DEV:C2:PTC:SIG:STATE',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'pt2_water_in': 
            {   
                'get_cmd':'READ:DEV:C2:PTC:SIG:WIT',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'pt2_water_out': 
            {
                'get_cmd':'READ:DEV:C2:PTC:SIG:WOT',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
        }

        self._add_parameters()# add attribute_parameters and dict_parameters

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
        ans = self._visainstrument.ask(message)

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
        
    def _parse(self, ans, message):
        ans = ans.split(':')
        if message.endswith('TEMP:SIG:TEMP'):
            return ans[-1][:-1]
        elif message=='READ:DEV:T12:TEMP:LOOP:P:I:D':
            ', '.join([ans[-5],ans[-3],ans[-1]])
        elif message=='READ:DEV:T12:TEMP:LOOP:RANGE':
            return ans[-1][:-2]
        else:
            return ans[-1]
            
    def get_all(self):
        for i in self.get_parameters():
            self.get(i)
            
    def do_set_t_mc(self,val,wait=True):
        self._execute('SET:DEV:T12:TEMP:LOOP:TSET:%s'%val)
        if wait:
            try:
                while abs(val - self.get_t_mc()) > self.MARGIN:
                    self._do_emit_changed()# update the GUI
                    self._check_last_pressed_key()
                    sleep(0.050)
            except KeyboardInterrupt:
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
