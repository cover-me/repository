from instrument import Instrument
from time import time, sleep
import visa
import types
import logging
import math

class GS210_20230529(Instrument):

    
    def __init__(self, name, address):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])
        print '%-15s\t%-35s\t%-15s'%(name, address, self.__module__)
        
        self._address = address
        self._visainstrument = visa.instrument(self._address)
        self._visainstrument.clear()
        self._initialize_parameters()
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
            'source_type': 
            {   
                'get_cmd':'SOUR:FUNC?',
                'set_cmd':':',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'source_range': 
            {   
                'get_cmd':':SOUR:RANG?',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GET}
            },
            'source_level': 
            {   
                'get_cmd':'SOUR:LEV?',
                'set_cmd':'SOUR:LEV %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET, 'maxstep':0.005, 'stepdelay':30,}
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
        self._visainstrument.write(message)

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
        return ans
            
    def get_all(self):
        for i in self.get_parameters():
            self.get(i)

