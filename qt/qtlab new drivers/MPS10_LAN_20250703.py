# https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers

from instrument import Instrument
import time, types, math, msvcrt, socket, struct

# Script for Ethernet connection of MPS10 (v1.4.98)
# Device terminates socket connection every 22 seconds -- implement reconnect logic.

# Class name should be the same as the file name
# Class methods are wrapped in qtlab, to use raw methods,
# (for debugging), try xxx._ins.yyy

# If "format" in dict_parameters does work, add "import types" in qtclient.py

class MPS10_LAN_20250703(Instrument):

    MARGIN = 1e-4# T
    MARGIN_CHECK_ACTION = True
    I_B_RATIO = 1# A/T. xs400a Z: 1/0.060948, 6 T; X or Y: 1/0.01111, 1 T; TritonXL 8.7399, 16 T; PT1 8.3625, 14 T
    MAX_FIELD = 0.05# T
    MAX_RATE = 0.2# T/min

    def __init__(self, name, address):
        Instrument.__init__(self, name, tags=['magnet'])
        print '%-15s\t%-35s\t%-15s'%(name, address, self.__module__)

        self._address = address
        self._connect(address)
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
                'get_cmd':'ID:0:5',
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
            'field_status':
            {
                'get_cmd':'field_status:16:1',
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
            'field_target_reached':
            {
                'get_cmd':'field_target_reached:215:1',
                'set_cmd':'',
                'kw':{
                        'type': types.BooleanType,# FloatType, StringType, ...
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
            'pid_output': 
            {   
                'get_cmd':'pid_output:80:6',
                'set_cmd':'',
                'kw':{
                        'type': types.ListType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.1,
                        # 'maxval': 1000,
                        # 'units': 'V',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        'format': '%g, %g, %g',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },
            'pid_K': 
            {   
                'get_cmd':'pid_K:86:6',
                'set_cmd':'',
                'kw':{
                        'type': types.ListType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.1,
                        # 'maxval': 1000,
                        # 'units': 'V',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        'format': '%g, %g, %g',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },
            'pid_K1': 
            {   
                'get_cmd':'pid_K1:192:6',
                'set_cmd':'',
                'kw':{
                        'type': types.ListType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.1,
                        # 'maxval': 1000,
                        # 'units': 'V',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        'format': '%g, %g, %g',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },
            'voltage_output': 
            {   
                'get_cmd':'voltage_output:22:2',
                'set_cmd':'',
                 'kw':{
                        'type': types.FloatType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.1,
                        # 'maxval': 1000,
                        'units': 'V',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },
            'voltage_limit': 
            {   
                'get_cmd':'voltage_limit:108:2',
                'set_cmd':'',
                 'kw':{
                        'type': types.FloatType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.1,
                        # 'maxval': 1000,
                        'units': 'V',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },
            'persist_switch_installed': 
            {
                'get_cmd':'persist_switch_installed:177:1',
                'set_cmd':'',
                'kw':{
                        'type': types.BooleanType,# FloatType, StringType, ...
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
            'persist_switch_status': 
            {
                'get_cmd':'persist_switch_status:178:1',
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
                        'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },
            'persist_switch_I': 
            {
                'get_cmd':'persist_switch_I:182:2',
                'set_cmd':'',
                'kw':{
                        'type': types.FloatType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.1,
                        # 'maxval': 1000,
                        'units': 'mA',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    }, 
            },
            'remote_status':
            {
                'get_cmd':'remote_status:16:1',
                'set_cmd':'',
                'kw':{
                        'type': types.BooleanType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GETSET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.1,
                        # 'maxval': 1000,
                        # 'units': 'mA',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    }, 
            },
            'field_sweep_high': 
            {
                'get_cmd':'field_sweep_high:104:2',
                'set_cmd':'field_sweep_high:104:2:%s',
                'kw':{
                        'type': types.FloatType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GETSET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.1,
                        # 'maxval': 1000,
                        'units': 'T',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    }, 
            },
            'field_sweep_low': 
            {   
                'get_cmd':'field_sweep_low:106:2',
                'set_cmd':'field_sweep_low:106:2:%s',
                'kw':{
                        'type': types.FloatType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GETSET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': 0.1,
                        # 'maxval': 1000,
                        'units': 'T',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },
            'field': 
            {   
                'get_cmd':'field:24:2',
                'set_cmd':'',
                'kw':{
                        'type': types.FloatType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GETSET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        'minval': -self.MAX_FIELD,
                        'maxval': self.MAX_FIELD,
                        'units': 'T',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },
            'field_target': 
            {
                'get_cmd':'field_target:18:2',
                'set_cmd':'field_target:18:2:%s',            
                'kw':{
                        'type': types.FloatType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GETSET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        'minval': -self.MAX_FIELD,
                        'maxval': self.MAX_FIELD,
                        'units': 'T',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },
            'field_rate': 
            {   
                'get_cmd':'field_rate:162:2',
                'set_cmd':'field_rate:162:2:%s',
                'kw':{
                        'type': types.FloatType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GETSET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        'minval': 0.0,
                        'maxval': self.MAX_RATE,
                        'units': 'T/min',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },
            'field_rate_point1': 
            {
                'get_cmd':'field_rate_point1:146:2',
                'set_cmd':'',
                'kw':{
                        'type': types.FloatType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': -self.MAX_FIELD,
                        # 'maxval': self.MAX_FIELD,
                        'units': 'T',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            }, 
            'NOTE':
            {
                'kw':{
                        'type': types.StringType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GETSET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': -self.MAX_FIELD,
                        # 'maxval': self.MAX_FIELD,
                        # 'units': 'T',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },
            'margin':
            {
                'kw':{
                        'type': types.FloatType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GETSET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': -self.MAX_FIELD,
                        # 'maxval': self.MAX_FIELD,
                        'units': 'T',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },
            'margin_check_action':
            {
                'kw':{
                        'type': types.BooleanType,# FloatType, StringType, ...
                        'flags': Instrument.FLAG_GETSET,# FLAG_GETSET, FLAG_GET, FLAG_SET
                        # 'channels': ['%02d'%i for i in range(1,25)],
                        # 'minval': -self.MAX_FIELD,
                        # 'maxval': self.MAX_FIELD,
                        # 'units': 'T',
                        # 'maxstep': 0.5e-3,
                        # 'stepdelay':30,# in ms
                        # 'format_map': {0:"OFF",1:"ON"},
                        # 'format': '%.06f',
                        # 'tags', 'doc', 'option_list', 'persist', 'probe_interval', listen_to
                    },
            },            
        }
        
        
            
        # Special parameters whose visibility depends on the value of the parameter "function" defined above.
        # self.DICT_PARA_function = { 
            # 'source_range_i': 
            # {   
                # 'get_cmd':':SOUR:CURR:RANG?',
                # 'set_cmd':':SOUR:CURR:RANG %s',
                # 'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'units':'A'}
            # },   
            # 'source_range_v': 
            # {   
                # 'get_cmd':':SOUR:VOLT:RANG?',
                # 'set_cmd':':SOUR:VOLT:RANG %s',
                # 'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'units':'V'}
            # },
        # }
        self.dict_parameters = self.DICT_PARA.copy()
        
        self._add_parameters()# add attribute_parameters and dict_parameters
        # self._add_function_depend_parameters()# add parameters according the value of the parameter "function"
        
        self.set_NOTE('I-B ratio: %s A/T'%self.I_B_RATIO)
        self.set_margin(self.MARGIN)
        self.set_margin_check_action(self.MARGIN_CHECK_ACTION)
        # self.set_field_target(self.get_field())
        self.set_remote_status(True)
   
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

    def _connect(self, address):
        # For LAN (socket) connection
        # Not actually perform connecting. 
        # Connecting and reconnecting after disconnection (by MPS10 every ~ 22 s) are implemented in self._write.
        addr_hardware, self._addr_ip, self._addr_port, addr_type = address.split('::')
        self._addr_port = int(self._addr_port)
        self._last_write_time = time.time()-30
        
    def close_session(self):
        self._socket.close()

    def _write(self, msg):
        t = time.time()
        if self._last_write_time+15<t:
            self._last_write_time = t
            self._connect_do()
        return self._socket.sendall(msg)
        
    def _read(self):
        ans = self._socket.recv(512)

        # check validation
        if self._validate_response(ans):
            return ans
        else:
            print 'Error response!'
            return None

    def _execute(self, message):
        message = self._get_real_set_cmd(message)
        self._write(message)
        return self._read()
        
    def _query(self, message, flag=0):
        '''
        flag, 0 (default): write command and read respond, 1: write only, 2: read only
        The reading can be non-atomic with the parameter flag
        '''
        if  flag != 2:
            self._write(self._get_real_get_cmd(message))
        if flag != 1:
            ans = self._read()
            return self._parse(ans,message)
        return None

    def _parse(self, ans, message):
        # byte 1: device id, 2: func code, 3: length, last 2 bytes: crc16 code
        ans = ans[3:-2]# data
        message = message.split(':')[0]
        if message=='ID':
            ans = struct.unpack('>5H', ans)
            ans = '.'.join([str(i) for i in ans])
        elif message=='remote_status':
            ans = self._bin_to_remote_status(ans)
        elif message=='field_status':
            ans = self._bin_to_field_status(ans)
        else:
            # _bin_to_number supports uint16, float32, and float32 array
            ans = self._bin_to_number(ans)
            # _process_unit with 'T': if value is field (judge with "message"), convert to Tesla, else return original value
            ans = self._process_unit(ans, message, 'T')
        return ans
        
    def _connect_do(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self._socket.settimeout(1)
        self._socket.connect((self._addr_ip, self._addr_port))
   
    def _get_real_set_cmd(self, cmd):
        name, start_position, num_of_reg, val = cmd.split(':')
        start_position = int(start_position)
        num_of_reg = int(num_of_reg)#*8bit
        num_of_data = num_of_reg*2#*4bit
        
        # MPS10 operates only with current, not field
        # _process_unit with 'A': if value is field (judge with "name"), convert to Ampere, else return original value
        val = self._process_unit(float(val), name, 'A')

        real_cmd = '\x01\x10'# 01: device id, 10: Write multiple register
        real_cmd +=  struct.pack('>HHB', start_position, num_of_reg, num_of_data)
        real_cmd += self._float_to_bin(val)
        real_cmd += self._crc16(real_cmd)# checksum
        
        return real_cmd
 
    def _get_real_get_cmd(self, cmd):
        name, start_position, length = cmd.split(':')
        start_position = int(start_position)
        length = int(length)

        real_cmd = '\x01\x03'#01: device id, 03: read register
        real_cmd +=  struct.pack('>HH', start_position, length)
        real_cmd += self._crc16(real_cmd)# crc16 checksum 
        
        return real_cmd

    def _bin_to_remote_status(self, binary_string):
        status = ord(binary_string[0])
        return bool(status)

    def _bin_to_field_status(self, binary_string):
        low_status = {0: 'Idle',
                      1: 'Pause',
                      2: 'To upper limit',
                      3: 'To lower limit',
                      4: 'To zero',
                      5: 'To magnet current',
                      6: 'To upper limit (fast)',
                      7: 'To lower limit (fast)',
                      8: 'To zero (fast)',
                      9: 'To magnet current (fast)',
                      10: 'Magnet disconnected',
                      11: 'Shutting down',
                      12: 'Recovering',
                      13: 'Passive zero',
                      14: 'Quench',
                      15: 'Quench'}
        status_code = ord(binary_string[1])
        ans = '%s-%s'%(status_code,low_status[status_code])
        return ans

    def _bin_to_number(self, binary_string):
        lbs = len(binary_string)
        if lbs==2:
            # uint16
            val, = struct.unpack('>H', binary_string)
            return val
        elif lbs==4:
            # float32
            high, low = binary_string[:2], binary_string[2:]
            binary_string = low + high# reverse the order
            val, = struct.unpack('>f', binary_string)
            return val
        elif lbs%4==0:
            # float32 list
            binary_string = [binary_string[i+2:i+4]+binary_string[i:i+2] for i in range(0, lbs, 4)]
            binary_string = ''.join(binary_string)
            val = struct.unpack('>%df'%(lbs/4), binary_string)
            return val
        print 'Error converting to float!'
        return None
        
    def _float_to_bin(self, val):
        binary_string = struct.pack('>f', val)
        high, low = binary_string[:2], binary_string[2:]
        binary_string = low + high# reverse the order
        return binary_string

    def _crc16(self, data):
        crc = 0xFFFF
        for byte in data:
            crc ^= ord(byte)
            for i in range(8):
                if ((crc & 1) != 0):
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        high = crc >> 8
        low = crc & 0xff
        crc_string = '%s%s'%(chr(low), chr(high))
        return crc_string

    def _process_unit(self, val, parameter_name, unit): 
        if parameter_name in ['field', 'field_target', 'field_rate_point1', 'field_sweep_high', 'field_sweep_low']:
            if unit=='T':
                # For reading
                # Raw unit is A, convert it to T
                return val/self.I_B_RATIO
            elif unit=='A':
                # For setting
                # Raw unit is T, convert it to A
                return val*self.I_B_RATIO
            else:
                print 'Wrong unit!'
        elif parameter_name in ['field_rate']:
            if unit=='T':
                # For reading
                # Raw unit is A/s, convert it to T/min
                return val/self.I_B_RATIO*60
            elif unit=='A':
                # For setting
                # Raw unit is T/min, convert it to A/s
                return val*self.I_B_RATIO/60
            else:
                print 'Wrong unit!'
        else:
            return val
 
    def _validate_response(self, resp):
        # device = resp[0]
        code = resp[1]
        check_str = resp[-2:]
        if code=='\x03':
            # return is data
            data_length = ord(resp[2])
            # byte: 1 device id, 2 code, 3 data length, -2 and -1 checksum 
            return len(resp)==data_length+5 and self._crc16(resp[:-2])==check_str
        elif code=='\x10':
            # return is an echo after setting
            # byte: 1 device id, 2 code, 3-4 position, 5-6 size, 7-8 checksum
            return self._crc16(resp[:-2])==check_str
        else:
            return False

    #############################
    # Ovewrite get/set functions#
    #############################
    
    def _set_action(self, cmd):
        d = {
                'SWEEP_PAUSE':1,
                'SWEEP_UP':2,
                'SWEEP_DOWN':3,
                'SWEEP_ZERO':4,
                'REMOTE':0,
                'LOCAL':15,
            }
        if cmd in d:
            action_code = d[cmd]
            cmd2 = '\x01\x10'#01: device id, 10: Write multiple Register
            cmd2 += struct.pack('>H', 17)# position: 17
            cmd2 += struct.pack('>H', 1)# num of register: 1 (*8bit)
            cmd2 += struct.pack('B', 2)# num of data: 2 (*4bit)
            cmd2 += struct.pack('>H',  0xA5<<8|action_code)# first byte 0xA5, second byte action_code
            cmd2 += self._crc16(cmd2)# checksum 
            self._write(cmd2)
            return self._read()
        else:
            print "Error action command!"
        
    def do_set_remote_status(self, val):
        if val==True:
            self._set_action('REMOTE')
        else:
            self._set_action('LOCAL')
    
    def do_set_field(self,val,wait=True):

        b0 = self.get_field()
        self.set_field_target(val)
        # begin with b_lower_lim <= b0 <= b_upper_lim
        # it appears that field_limit changes after field_target changes
        if val<b0:
            # self.set_field_sweep_low(val)
            self._set_action('SWEEP_DOWN')
        else:
            # self.set_field_sweep_high(val)
            self._set_action('SWEEP_UP')

        if wait:
            try:
                while abs(val - self.get_field()) > self._margin or (self._margin_check_action and not self.get_field_target_reached()):
                    self._do_emit_changed()# update the GUI
                    self._check_last_pressed_key()
                    time.sleep(0.05)
                # time.sleep(0.1)
            except KeyboardInterrupt:
                self._set_action('SWEEP_PAUSE')
                raise KeyboardInterrupt
                
        # ~ 35 ms each reading
        # self.get_field_sweep_low()
        # self.get_field_sweep_high()
        
        return True

    def _check_last_pressed_key(self):
        last_key = ''
        while msvcrt.kbhit():
           last_key = msvcrt.getch()
        if last_key == '\x05':#ctrl+e(xit)
            raise KeyboardInterrupt

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
