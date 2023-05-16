# https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers

from instrument import Instrument
from time import sleep
import visa
import types
import msvcrt
import logging

class PPMS_20230515(Instrument):
    MARGIN_B = 1e-4# T
    MARGIN_T = 1e-3# K
    TIME_SLEEP = 0.05# s
    # We have to emulate field rate and temperature rate, becasue they can not be read from PPMS!
    RATE_B = 0.3# T/min
    RATE_T = 10# K/min

    def __init__(self, name, address, term_chars = '\n'):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])
        print '%-15s\t%-35s\t%-15s'%(name, address, self.__module__)
        
        self._address = address
        self._visainstrument = visa.instrument(self._address, term_chars = term_chars)
        self._visainstrument.clear()
        
        self._initialize_parameters()
        # We have to emulate field rate and temperature rate, becasue they can not be read from PPMS!
        self.set_field_rate(self.RATE_B)
        self.set_temp_rate(self.RATE_T)
        
        self.get_all()
        
        
    def _initialize_parameters(self):
        # Parameters that are class attributes
        self.attribute_parameters = ['_address', '__module__']
        
        # Other paramters, use get_cmd and set_cmd, or leave them blank and manually define get/set functions.
        self.dict_parameters = { 
            'ID':
            {
                'get_cmd':'*IDN?',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'temp': 
            {   
                'get_cmd':'TEMP?',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'units':'K', 'maxval':400, 'minval':1.6}
            },              
            'temp_rate': 
            {   
                'get_cmd':'',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'units':'K/min', 'maxval':10, 'minval':0.01}
            },            
            'field': 
            {   
                'get_cmd':'FELD?',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'units':'T', 'maxval':14, 'minval':-14}
            },              
            'field_rate': 
            {   
                'get_cmd':'',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'units':'T/min', 'maxval':0.72, 'minval':0}
            },      
        }
        
        self._add_parameters()

    def _parse(self, ans, message):
        ans = ans.split(', ')
        if message=='*IDN?':
            return ', '.join(ans[1:3])# 0, QuantumDesign, dynacool, N/A, N/A..
        elif message=='TEMP?':
            return ans[2]# error, status, reading
        elif message=='FELD?':
            return float(ans[2])/1.e4# convert Oe to T
            
    def do_set_temp(self, val, wait=True, approach=0):
        '''
        Set the temperature (K)
        Approach: Fast, No Overshoot
        '''
        rate = self.get_temp_rate()
        self._execute('TEMP %s, %s, %i'%(val, rate, approach))

        if wait:
            try:
                while abs(val - self.get_temp()) > self.MARGIN_T:
                    self._do_emit_changed()# update the GUI for temperature value
                    self._check_last_pressed_key()
                    sleep(self.TIME_SLEEP)
            except KeyboardInterrupt:
                raise KeyboardInterrupt
        return True
        
    def do_set_field(self, b_tesla, wait=True, approach=0, endmode=0):
        '''
        Set the field (T)
        Approach: Linear, Oscillate (eliminate flux motion,reduce remanence)
        '''
        h_oe = b_tesla * 1.e4
        rate_tesla_min = self.get_field_rate()
        rate_oe_s = rate_tesla_min*1.e4/60.
        self._execute('FELD %s, %s, %i, %i'%(h_oe, rate_oe_s, approach, endmode))
        
        if wait:
            try:
                while abs(b_tesla - self.get_field()) > self.MARGIN_B:
                    self._do_emit_changed()# update the GUI for field value
                    self._check_last_pressed_key()
                    sleep(self.TIME_SLEEP)
            except KeyboardInterrupt:
                raise KeyboardInterrupt
        return True

    # We have to emulate field rate and temperature rate, becasue they can not be read from PPMS! 
    def do_set_temp_rate(self, r):# temp_rate
        pass
        
    def do_get_temp_rate(self):# temp_rate
        return self.get_parameters()['temp_rate']['value']
        
    def do_set_field_rate(self, r):# field_rate
        pass
        
    def do_get_field_rate(self):# field_rate
        return self.get_parameters()['field_rate']['value']
        
        
                 
    def get_all(self):
        for i in self.attribute_parameters:
            para_name = i.strip('_').upper()
            self.get(para_name)
        for i in self.dict_parameters:
            self.get(i)
            
    def _add_parameters(self):
        # Add attribute parameters
        for i in self.attribute_parameters:
            para_name = i.strip('_').upper()
            func = lambda attr_name=i: getattr(self,attr_name) 
            setattr(self, 'do_get_%s'%para_name, func)
            self.add_parameter(para_name, flags=Instrument.FLAG_GET, type=types.StringType)

        # Add other parameters
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

    def close_session(self):
        self._visainstrument.close() 
        
    def _execute(self, message):
        self._visainstrument.write(message)
        return self._visainstrument.read()
        
        
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


    def _check_last_pressed_key(self):
        last_key = ''
        while msvcrt.kbhit():
           last_key = msvcrt.getch()
        if last_key == '\x05':#ctrl+e(xit)
            raise KeyboardInterrupt
