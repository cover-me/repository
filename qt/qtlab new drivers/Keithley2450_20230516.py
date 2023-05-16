# https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers

from instrument import Instrument
import visa
import types
import logging

class Keithley2450_20230516(Instrument):

    def __init__(self, name, address):
        logging.info(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])
        print '%-15s\t%-35s\t%-15s'%(name, address, self.__module__)
        
        self._address = address
        self._visainstrument = visa.instrument(self._address)
        self._visainstrument.clear()
        self._initialize_parameters()
        self._add_source_depend_parameters()
        self._add_sense_depend_parameters()
        self.get_all()

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
            'switch_output': 
            {   
                'get_cmd':'OUTP?',
                'set_cmd':'OUTP %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"OFF",1:"ON"}}
            },              
            'mode_source': 
            {   
                'get_cmd':'SOUR:FUNC?',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET,'format_map':{'VOLT':'VOLT','CURR':'CURR'}}
            },
            'mode_sense': 
            {   
                'get_cmd':'SENS:FUNC?',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET,'format_map':{'"VOLT:DC"':'VOLT','"CURR:DC"':'CURR'}}
            },      
            'val': 
            {   
                'get_cmd':'READ?',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GET}
            },
            }
            
        # depend on source type
        self.DICT_PARA_source = { 
            'source_level_i': 
            {   
                'get_cmd':'SOUR:CURR?',
                'set_cmd':'SOUR:CURR %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'maxstep':10e-9, 'stepdelay':30,'units':'A'}
            },      
            'source_level_v': 
            {   
                'get_cmd':'SOUR:VOLT?',
                'set_cmd':'SOUR:VOLT %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'maxstep':10e-3, 'stepdelay':30,'units':'V'}
            }, 
            'source_range_i': 
            {
                'get_cmd':'SOUR:CURR:RANG?',
                'set_cmd':'SOUR:CURR:RANG %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'units':'A'}
            },
            'source_range_v': 
            {
                'get_cmd':':SOUR:VOLT:RANG?',
                'set_cmd':':SOUR:VOLT:RANG %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'units':'V'}
            },
            'source_compliance_i': 
            {   
                'get_cmd':'SOUR:CURR:VLIM?',
                'set_cmd':'SOUR:CURR:VLIM %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'units':'V'}
            },
            'source_compliance_v': 
            {   
                'get_cmd':'SOUR:VOLT:ILIM?',
                'set_cmd':'SOUR:VOLT:ILIM %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'units':'A'}
            },            
            'switch_source_autodelay_i': 
            {   
                'get_cmd':'SOUR:CURR:DEL:AUTO?',
                'set_cmd':'SOUR:CURR:DEL:AUTO %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'format_map':{0:"OFF",1:"ON"}}
            },
            'switch_source_autodelay_v': 
            {   
                'get_cmd':'SOUR:VOLT:DEL:AUTO?',
                'set_cmd':'SOUR:VOLT:DEL:AUTO %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'format_map':{0:"OFF",1:"ON"}}
            },
            'switch_source_readback_i': 
            {   
                'get_cmd':'SOUR:CURR:READ:BACK?',
                'set_cmd':'SOUR:CURR:READ:BACK %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'format_map':{0:"OFF",1:"ON"}}
            },
            'switch_source_readback_v': 
            {   
                'get_cmd':'SOUR:VOLT:READ:BACK?',
                'set_cmd':'SOUR:VOLT:READ:BACK %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'format_map':{0:"OFF",1:"ON"}}
            },
            'source_delay_i': 
            {   
                'get_cmd':'SOUR:CURR:DEL?',
                'set_cmd':'SOUR:CURR:DEL %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'units':'s'}
            },
            'source_delay_v': 
            {   
                'get_cmd':'SOUR:VOLT:DEL?',
                'set_cmd':'SOUR:VOLT:DEL %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'units':'s'}
            },
 
            }
            
        # depend on sense type
        self.DICT_PARA_sense = { 
            'sense_range_i': 
            {   
                'get_cmd':'SENS:CURR:RANG?',
                'set_cmd':'SENS:CURR:RANG %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'units':'A'}
            },
            'sense_range_v': 
            {   
                'get_cmd':'SENS:VOLT:RANG?',
                'set_cmd':'SENS:VOLT:RANG %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'units':'V'}
            }, 
            'switch_autozero_i': 
            {   
                'get_cmd':'SENS:CURR:AZER?',
                'set_cmd':'SENS:CURR:AZER %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'format_map':{0:"OFF",1:"ON"}}
            },
            'switch_autozero_v': 
            {   
                'get_cmd':'SENS:VOLT:AZER?',
                'set_cmd':'SENS:VOLT:AZER %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'format_map':{0:"OFF",1:"ON"}}
            },
            'switch_aver_filter_i': 
            {   
                'get_cmd':'SENS:CURR:AVER?',
                'set_cmd':'SENS:CURR:AVER %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'format_map':{0:"OFF",1:"ON"}}
            },
            'switch_aver_filter_v': 
            {   
                'get_cmd':'SENS:VOLT:AVER?',
                'set_cmd':'SENS:VOLT:AVER %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'format_map':{0:"OFF",1:"ON"}}
            },
            'sense_nplc_i': 
            {   
                'get_cmd':'SENS:CURR:NPLC?',
                'set_cmd':'SENS:CURR:NPLC %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET}
            },
            'sense_nplc_v': 
            {   
                'get_cmd':'SENS:VOLT:NPLC?',
                'set_cmd':'SENS:VOLT:NPLC %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET}
            },
            }
            
        self.dict_parameters = self.DICT_PARA.copy()
        self._add_parameters()# add attribute_parameters and dict_parameters


    def  _add_source_depend_parameters(self):
        
        source_type = self.get_mode_source()
        s = {'VOLT':'_v','CURR':'_i'}[source_type]
        d = {}

        for i in self.DICT_PARA_source:
            if i.endswith(s):
                name = i[:-2]
                self.dict_parameters[name] = self.DICT_PARA_source[i]
                d[name] = self.DICT_PARA_source[i]
 
        self._add_parameters_from_dict(d)
        
    def  _add_sense_depend_parameters(self):
        sense_type = self.get_mode_sense()
        s = {'"VOLT:DC"':'_v','"CURR:DC"':'_i'}[sense_type]
        d = {}

        for i in self.DICT_PARA_sense:
            if i.endswith(s):
                name = i[:-2]
                self.dict_parameters[name] = self.DICT_PARA_sense[i]
                d[name] = self.DICT_PARA_sense[i]
       
        self._add_parameters_from_dict(d)

    # def do_set_mode_source(self,val):
        # self._execute('SOUR:FUNC %s'%val)
        # self._on_source_type_change()
        # self.get_all()

    # def do_set_mode_sense(self,val):
        # self._execute('SENS:FUNC %s'%val)
        # self._on_sense_type_change()
        # self.get_all()
        
    def _parse(self, ans, message):
        return ans
            
    def get_all(self):
        for i in self.get_parameters():
            self.get(i)
            
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
