# https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers

from instrument import Instrument
import types, time, visa, qt

# Class name should be the same as the file name
# Class methods are wrapped in qtlab, to use raw methods,
# (for debugging), try xxx._ins.yyy

# If "format" in dict_parameters does work, add "import types" in qtclient.py

class Keithley_6500_20250707(Instrument):

    def __init__(self, name, address, term_chars=None):
        Instrument.__init__(self, name, tags=['dmm'])
        print '%-15s\t%-35s\t%-15s'%(name, address, self.__module__)
        
        self._address = address
        self._connect(address, term_chars)
        self._initialize_parameters()
        self.get_all()
        # qt.flow.connect('measurement-start', self._measurement_start_cb)
        # qt.flow.connect('measurement-end', self._measurement_end_cb)

    #############################
    #######  Parameters   #######
    #############################
        
    def _initialize_parameters(self):
        # In qtlab, a value associated with a channel or setting is referred to as a 
        # "parameter" of an instrument. The value of a parameter can be retrieved or
        # modified (if adjustable) through get_xxx and set_xxx functions.
        
        # Some of the class attributes are chosen as parameters
        self.attribute_parameters = ['_address', '__module__']

        # General parameters
        # 'get_cmd' and 'set_cmd' can be the empty string to define corresponding functions manually (do_get_xxx and do_set_xxx),
        # or undeclared to create parameters that are attributes of the class
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
            'mode':
            {
                'get_cmd':'FUNC?',
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
            'val':
            {
                'get_cmd':':READ?',
                'set_cmd':'',
                'kw':{
                        'type': types.FloatType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.1,
                        # 'maxval': 1000,
                        'units': '',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },
            'range':
            {
                'get_cmd':'VOLT:RANG?',
                'set_cmd':'VOLT:RANG %s',
                'kw':{
                        'type': types.FloatType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GETSET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        'minval': 0.1,
                        'maxval': 1000,
                        'units': '',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },
            'nplc':
            {
                'get_cmd':'VOLT:NPLC?',
                'set_cmd':'VOLT:NPLC %s',
                'kw':{
                        'type': types.FloatType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GETSET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        'minval': 0.01,
                        'maxval': 15,
                        # 'units': 'V',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },
            'averaging':
            {
                'get_cmd':'VOLT:AVER:STAT?',
                'set_cmd':'VOLT:AVER:STAT %d',
                'kw':{
                        'type': types.IntType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GETSET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.01,
                        # 'maxval': 15,
                        # 'units': 'V',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },
            'autozero':
            {
                'get_cmd':'VOLT:AZER:STAT?',
                'set_cmd':'VOLT:AZER:STAT %d',
                'kw':{
                        'type': types.IntType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GETSET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.01,
                        # 'maxval': 15,
                        # 'units': 'V',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },
            'autorange':
            {
                'get_cmd':'VOLT:RANG:AUTO?',
                'set_cmd':'VOLT:RANG:AUTO %d',
                'kw':{
                        'type': types.IntType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GETSET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.01,
                        # 'maxval': 15,
                        # 'units': 'V',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },
            'averaging_count':
            {
                'get_cmd':'VOLT:AVER:COUN?',
                'set_cmd':'VOLT:AVER:COUN %d',
                'kw':{
                        'type': types.IntType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GETSET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        'minval': 1,
                        'maxval': 100,
                        # 'units': 'V',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },
            'averaging_type':
            {
                'get_cmd':'VOLT:AVER:TCON?',
                'set_cmd':'VOLT:AVER:TCON %s',
                'kw':{
                        'type': types.StringType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GETSET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 1,
                        # 'maxval': 100,
                        # 'units': 'V',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        'format_map': {"REP":"REP","MOV":"MOV"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },
        }
            
        # Special parameters whose visibility depends on the value of the parameter "function" defined above.
        # self.DICT_PARA_function = { 
            # 'range_i': 
            # {   
                # 'get_cmd':'CURR:RANG?',
                # 'set_cmd':'CURR:RANG %s',
                # 'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'units':'A'}
            # },   
            # 'range_v': 
            # {   
                # 'get_cmd':'VOLT:RANG?',
                # 'set_cmd':'VOLT:RANG %s',
                # 'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'units':'V'}
            # },
            # }

        self.dict_parameters = self.DICT_PARA.copy()
        self._add_parameters()# add attribute_parameters and dict_parameters
        # self._add_function_depend_parameters()# add parameters according the value of the parameter "function"

    # def  _add_function_depend_parameters(self):
        # function_type = self.get_function()
        # s = {'"VOLT"':'_v','"CURR"':'_i'}[function_type]
        # d = {}

        # for i in self.DICT_PARA_function:
            # if i.endswith(s):
                # name = i[:-len(s)]
                # self.dict_parameters[name] = self.DICT_PARA_function[i]
                # d[name] = self.DICT_PARA_function[i]
 
        # self._add_parameters_from_dict(d)
        
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

    def get_all(self):
        for i in self.get_parameters():
            self.get(i)
            
    #############################
    ####### IO operations #######
    #############################

    def _connect(self, address, term_chars):
        self._visainstrument = visa.instrument(self._address, timeout=2)
        self._visainstrument.term_chars = term_chars
        self._visainstrument.clear()# clear readings in the buffer
        
    def close_session(self):
        self._visainstrument.close() 
         
    def _execute(self, message):
        return self._visainstrument.write(message)
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
            
    #############################
    # Ovewrite get/set functions#
    #############################


    #############################
    # Others                    #
    #############################
    
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
