# https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers

from instrument import Instrument
# from time import time, sleep
import visa
import types
import logging
# import math
import qt

class Agilent34401A_20230622(Instrument):

    def __init__(self, name, address):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['dmm'])
        print '%-15s\t%-35s\t%-15s'%(name, address, self.__module__)
        
        self._address = address
        self._visainstrument = visa.instrument(self._address, timeout=2)
        self._visainstrument.clear()
        self._initialize_parameters()
        self.get_all()
        
        # qt.flow.connect('measurement-start', self._measurement_start_cb)
        # qt.flow.connect('measurement-end', self._measurement_end_cb)

    def _initialize_parameters(self):
        # Parameters that are class attributes 
        self.attribute_parameters = ['_address', '__module__']

        self.DICT_PARA = { 
            'ID':
            {
                'get_cmd':'*IDN?',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'function': 
            {   
                'get_cmd':'FUNC?',
                'set_cmd':'FUNC %s',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GETSET,'format_map':{'"VOLT"':'VOLT','"CURR"':'CURR'}}
            },
            'auto_impedance': 
            {   
                'get_cmd':'INPut:IMPedance:AUTO?',
                'set_cmd':'INPut:IMPedance:AUTO %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'format_map':{0:False,1:True}}
            },   
            'auto_zero': 
            {   
                'get_cmd':'ZERO:AUTO?',
                'set_cmd':'ZERO:AUTO %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'format_map':{0:False,1:True}}
            },   
            'math': 
            {   
                'get_cmd':'CALCulate:STATe?',
                'set_cmd':'CALCulate:STATe %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'format_map':{0:False,1:True}}
            },   
            'terminals': 
            {   
                'get_cmd':'ROUTe:TERMinals?',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },   
            'val': 
            {   
                'get_cmd':'READ?',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GET}
            },   
            }
            
        # depend on parameter "function"
        self.DICT_PARA_function = { 
            'range_i': 
            {   
                'get_cmd':'CURR:RANG?',
                'set_cmd':'CURR:RANG %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'units':'A'}
            },   
            'range_v': 
            {   
                'get_cmd':'VOLT:RANG?',
                'set_cmd':'VOLT:RANG %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'units':'V'}
            },            
            'range_auto_i': 
            {   
                'get_cmd':'CURR:RANG:AUTO?',
                'set_cmd':'CURR:RANG:AUTO %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'format_map':{0:False,1:True}}
            },   
            'range_auto_v': 
            {   
                'get_cmd':'VOLT:RANG:AUTO?',
                'set_cmd':'VOLT:RANG:AUTO %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'format_map':{0:False,1:True}}
            },
            'resolution_i': 
            {   
                'get_cmd':'CURR:RES?',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GET,'units':'A'}
            },   
            'resolution_v': 
            {   
                'get_cmd':'VOLT:RES?',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GET,'units':'V'}
            },
            'nplc_i': 
            {   
                'get_cmd':'CURR:NPLC?',
                'set_cmd':'CURR:NPLC %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET}
            },   
            'nplc_v': 
            {   
                'get_cmd':'VOLT:NPLC?',
                'set_cmd':'VOLT:NPLC %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET}
            },
            
            }

        self.dict_parameters = self.DICT_PARA.copy()
        self._add_parameters()# add attribute_parameters and dict_parameters
        self._add_function_depend_parameters()

    def  _add_function_depend_parameters(self):
        
        function_type = self.get_function()
        s = {'"VOLT"':'_v','"CURR"':'_i'}[function_type]
        d = {}

        for i in self.DICT_PARA_function:
            if i.endswith(s):
                name = i[:-len(s)]
                self.dict_parameters[name] = self.DICT_PARA_function[i]
                d[name] = self.DICT_PARA_function[i]
 
        self._add_parameters_from_dict(d)
        
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
        
    # def _get_parameter_fast(self, name):
        # p = self.get_parameters()
        # if name in p:
            # val = p[name]['value']
            # if val is None:
                # return self.get(name)
            # else:
                # return val
        # else:
            # return None
            
    # def _measurement_start_cb(self, sender):
        # pass

    # def _measurement_end_cb(self, sender):
        # pass
