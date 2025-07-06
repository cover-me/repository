# https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers

from instrument import Instrument
import visa
import types
import logging
import qt
import time

# The class name should be the same as the file name
# Class methods are wrapped in qtlab, to use raw methods,
# (for debugging), try xxx._ins.yyy

class GS610_20241104(Instrument):

    def __init__(self, name, address, term_chars='\r\n'):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['dac'])
        print '%-15s\t%-35s\t%-15s'%(name, address, self.__module__)
        
        self._address = address
        self._visainstrument = visa.instrument(self._address, timeout=2)
        self._visainstrument.term_chars = term_chars
        self._visainstrument.clear()# clear readings in the buffer
        self._initialize_parameters()
        self.get_all()
        
        # If you need actions before/after a measurment
        # qt.flow.connect('measurement-start', self._measurement_start_cb)
        # qt.flow.connect('measurement-end', self._measurement_end_cb)
        
    def _initialize_parameters(self):
        # In qtlab, a value associated with a channel or setting is referred to as a 
        # "parameter" of an instrument. The value of a parameter can be retrieved or
        # modified (if it is adjustable) using get_xxx and set_xxx functions.
        
        # Parameters from attributes of the class
        self.attribute_parameters = ['_address', '__module__']

        self.DICT_PARA = {
            'ID':
            {
                'get_cmd':'*IDN?',
                'set_cmd':'',
                'kw':{
                        'type': types.StringType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.1,
                        # 'maxval': 1000,
                        # 'units': 'V',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            }, 
            'source_func':
            {
                'get_cmd':'SOURce:FUNC?',
                'set_cmd':'',
                'kw':{
                        'type': types.StringType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.1,
                        # 'maxval': 1000,
                        # 'units': 'V',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },
            'sense_func':
            {
                'get_cmd':'sense:FUNC?',
                'set_cmd':'',
                'kw':{
                        'type': types.StringType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.1,
                        # 'maxval': 1000,
                        # 'units': 'V',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            }, 
            'sense_status':
            {
                'get_cmd':':SENSe:STAT?',
                'set_cmd':':SENSe:STAT %s',
                'kw':{
                        'type': types.IntType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GETSET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.1,
                        # 'maxval': 1000,
                        # 'units': 'V',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            }, 
           'source_status':
            {
                'get_cmd':':OUTP:STAT?',
                'set_cmd':':OUTP:STAT %s',
                'kw':{
                        'type': types.IntType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GETSET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.1,
                        # 'maxval': 1000,
                        # 'units': 'V',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            }, 
            'sense_val':
            {
                'get_cmd':'FETCh?',
                'set_cmd':'',
                'kw':{
                        'type': types.FloatType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.1,
                        # 'maxval': 1000,
                        # 'units': 'V',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {'OFF':0,'ON':1},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            }, 
            'sense_range_auto':
            {
                'get_cmd':':SENSe:RANGe:AUTO?',
                'set_cmd':'',
                'kw':{
                        'type': types.IntType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.1,
                        # 'maxval': 1000,
                        # 'units': 'V',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },  
            'sense_average':
            {
                'get_cmd':':SENS:AVER:STAT?',
                'set_cmd':'',
                'kw':{
                        'type': types.IntType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.1,
                        # 'maxval': 1000,
                        # 'units': 'V',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            }, 
            'sense_autozero':
            {
                'get_cmd':':SENS:AZER:STAT?',
                'set_cmd':'',
                'kw':{
                        'type': types.IntType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.1,
                        # 'maxval': 1000,
                        # 'units': 'V',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },             
        }
            
        # Which parameter to add depends on the value of the parameter "function" defined above.
        self.DICT_PARA_function = { 
            'source_range_i': 
            {   
                'get_cmd':':SOUR:CURR:RANG?',
                'set_cmd':':SOUR:CURR:RANG %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'units':'A'}
            },   
            'source_range_v': 
            {   
                'get_cmd':':SOUR:VOLT:RANG?',
                'set_cmd':':SOUR:VOLT:RANG %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'units':'V'}
            },
            'source_level_i': 
            {   
                'get_cmd':'SOUR:CURR:LEV?',
                'set_cmd':'SOUR:CURR:LEV %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'units':'A'}
            },   
            'source_level_v': 
            {   
                'get_cmd':'SOUR:VOLT:LEV?',
                'set_cmd':':SOUR:VOLT:LEV %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'units':'V'}
            },
            'source_limit_i': 
            {   
                'get_cmd':':SOURce:VOLTage:PROTection:ULIMit?',
                'set_cmd':':SOURce:VOLTage:PROTection:ULIMit %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'units':'V'}
            },   
            'source_limit_v': 
            {   
                'get_cmd':':SOURce:CURR:PROTection:ULIMit?',
                'set_cmd':':SOURce:CURR:PROTection:ULIMit %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'units':'A'}
            },
        }
 

        self.dict_parameters = self.DICT_PARA.copy()
        self._add_parameters()# add attribute_parameters and dict_parameters
        self._add_function_depend_parameters()# add parameters according the value of the parameter "function"

    def  _add_function_depend_parameters(self):
        # pass
        function_type = self.get_source_func()
        s = {'VOLT':'_v','CURR':'_i'}[function_type]
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
        self._visainstrument.write(message)
        # self._visainstrument.read()
        
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
        
    # def _read_until_empty(self):
        # ans = ''
        # line = ''
        # tout_old = self._visainstrument.timeout
        # self._visainstrument.timeout = 0.3
        
        # while 1:
            # try:
                # line = self._visainstrument.read()
                # ans += line + '\n'
            # except:
                # break
                
        # self._visainstrument.timeout = tout_old
        # return ans
    
    # def _query_eager(self, message):
        # self._visainstrument.write(message)
        # return self._read_until_empty()
    

