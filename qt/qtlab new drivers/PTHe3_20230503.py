# https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers

from instrument import Instrument
from time import sleep
import visa
import types
import msvcrt
import logging

class PTHe3_20230503(Instrument):
    MARGIN = 1e-3
    def __init__(self, name, address, term_chars = '\n'):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])
        
        self._address = address
        self._visainstrument = visa.instrument(self._address, term_chars = term_chars)
        self._visainstrument.clear()
        
        self.attribute_parameters = ['_address', '__module__']

        self.dict_parameters = { 
            'ID':
            {
                'get_cmd':'*IDN?',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'status': 
            {   
                'get_cmd':'READ:DEV:HelioxX:HEL:SIG:STAT',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'he3pot': 
            {   
                'get_cmd':'READ:DEV:HelioxX:HEL:SIG:TEMP',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'units':'K', 'maxval':300, 'minval':0}
            },              
            'he3pot_setpoint': 
            {   
                'get_cmd':'READ:DEV:HelioxX:HEL:SIG:TSET',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GET,'units':'K'}
            },            
            'he3pot_stable': 
            {   
                'get_cmd':'READ:DEV:HelioxX:HEL:SIG:H3PS',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'onekpot': 
            {   
                'get_cmd':'READ:DEV:DB6.T1:TEMP:SIG:TEMP',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GET,'units':'K'}
            },
            'sorb': 
            {   
                'get_cmd':'READ:DEV:MB1.T1:TEMP:SIG:TEMP',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GET,'units':'K'}
            },
            'onekpot_pressure': 
            {   
                'get_cmd':'READ:DEV:DB3.P1:PRES:SIG:PRES',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GET,'units':'mB'}
            },
           
        }
        
        # Add parameters
        for i in self.attribute_parameters:
            para_name = i.strip('_').upper()
            func = lambda attr_name=i: getattr(self,attr_name) 
            setattr(self, 'do_get_%s'%para_name, func)
            self.add_parameter(para_name, flags=Instrument.FLAG_GET, type=types.StringType)

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

        self.get_all()
        
    def close_session(self):
        self._visainstrument.close() 

    def _execute(self, message):
        return self._visainstrument.ask(message)
        
    def _query(self, message, flag=0):
        '''
        flag, 0 (default): write command and read respond, 1: write only, 2: read only
        '''
        if  flag != 2:
            self._visainstrument.write(message)
        if flag != 1:
            ans = self._visainstrument.read()
            return self._parse(ans,message)
        return None
            
    def _parse(self, ans, message):
        if message == '*IDN?':
            return ans[4:]
        ans = ans.split(':')[-1]
        if message in ['READ:DEV:HelioxX:HEL:SIG:STAT','READ:DEV:HelioxX:HEL:SIG:H3PS']:
            return ans
        elif message == 'READ:DEV:DB3.P1:PRES:SIG:PRES':
            return ans[:-2]
        else:
            return ans[:-1]

    def get_all(self):
        for i in self.attribute_parameters:
            para_name = i.strip('_').upper()
            self.get(para_name)
        for i in self.dict_parameters:
            self.get(i)

    def do_set_he3pot(self,val,wait=True):
        self._execute('SET:DEV:HelioxX:HEL:TSET:%s'%val)
        if wait:
            try:
                while abs(val - self.get_he3pot()) > self.MARGIN or self.get_he3pot_stable() != 'Stable':
                    self.get_he3pot_setpoint()
                    self._do_emit_changed()# update the GUI
                    self._check_last_pressed_key()
                    sleep(0.050)
            except KeyboardInterrupt:
                # val = self.get_he3pot()
                # self._execute('SET:DEV:HelioxX:HEL:TSET:%s'%val)
                raise KeyboardInterrupt
        return True
        
    def _check_last_pressed_key(self):
        last_key = ''
        while msvcrt.kbhit():
           last_key = msvcrt.getch()
        if last_key == '\x05':#ctrl+e(xit)
            raise KeyboardInterrupt
