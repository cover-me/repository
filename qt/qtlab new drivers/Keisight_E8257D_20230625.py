# https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers

from instrument import Instrument
from time import time, sleep
import visa
import types
import logging
import math
# import msvcrt

class Keisight_E8257D_20230625(Instrument):

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
        
        self.dict_parameters = {
            'ID':
            {
                'get_cmd':'*IDN?',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'output':
            {
                'get_cmd':'output?',
                'set_cmd':'output %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:False,1:True}}
            },
            'amplitude':
            {
                'get_cmd':':AMPLitude?',
                'set_cmd':':AMPLitude %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'units':'dBm'}
            },       
            'frequency':
            {
                'get_cmd':':FREQuency?',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'units':'GHz'}
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
            # A virtual parameter
            if 'get_cmd' not in para_dict[i] and 'set_cmd' not in para_dict[i]:
                func = lambda : getattr(self,i)
                setattr(self, 'do_get_%s'%i, func)
                
                func = lambda x: setattr(self,i,x)
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
        return self._visainstrument.write(message)
        
    def _parse(self, ans, message):
        if message==':FREQuency?':
            return float(ans)*1.0e-9
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

    # def _measurement_start_cb(self, sender):
        # pass

    # def _measurement_end_cb(self, sender):
        # pass

    def do_set_frequency(self,x):
        return self._execute(':FREQuency %s'%(x*1.0e9))