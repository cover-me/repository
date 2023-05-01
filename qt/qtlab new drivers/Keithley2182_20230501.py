# https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers

from instrument import Instrument
# from time import time, sleep
import visa
import types
import logging
# import math

class Keithley2182_20230501(Instrument):

    def __init__(self, name, address):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])
        self._address = address
        self._visainstrument = visa.instrument(self._address)
        self._visainstrument.clear()
        
        self.attribute_parameters = ['_address', '__module__']

        self.dict_parameters = { 
            'ID':
            {
                'get_cmd':'*IDN?',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'channel': 
            {   
                'get_cmd':':SENS:CHAN?',
                'set_cmd':':SENS:CHAN %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{1:"CHAN1",2:"CHAN2"}}
            },
            'nplc': 
            {
                'get_cmd':':SENS:VOLT:NPLC?',
                'set_cmd':':SENS:VOLT:NPLC %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET}
            },
            'last_val': 
            {   
                'get_cmd':':FETCH?',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GET, 'units':'V'}
            },
            'ch1_analog_filter': 
            {   
                'get_cmd':':SENS:VOLT:CHAN1:LPAS:STAT?',
                'set_cmd':':SENS:VOLT:CHAN1:LPAS:STAT %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"OFF",1:"ON"}}
            },
            'ch1_digital_filter': 
            {   
                'get_cmd':':SENS:VOLT:CHAN1:DFIL:STAT?',
                'set_cmd':':SENS:VOLT:CHAN1:DFIL:STAT %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"OFF",1:"ON"}}
            },  
            'ch1_range': 
            {
                'get_cmd':':SENS:VOLT:CHAN1:RANG?',
                'set_cmd':':SENS:VOLT:CHAN1:RANG %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET, 'units':'V'}
            },
            'digits': 
            {
                'get_cmd':':SENS:VOLT:DC:DIG?',
                'set_cmd':':SENS:VOLT:DC:DIG %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET}
            },            
            'auto_zero': 
            {   
                'get_cmd':':SYST:AZER:STAT?',
                'set_cmd':':SYST:AZER:STAT %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"OFF",1:"ON"}}
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
        return self._visainstrument.write(message)
        
    def _query(self, message, flag=0):
        '''
        flag, 0 (default): write command and read respond, 1: write only, 2: read only
        '''
        if  flag != 2:
            self._visainstrument.write(message)
        if flag != 1:
            ans = self._visainstrument.read()
            return ans
        return None

    def get_all(self):
        for i in self.attribute_parameters:
            para_name = i.strip('_').upper()
            self.get(para_name)
        for i in self.dict_parameters:
            self.get(i)
