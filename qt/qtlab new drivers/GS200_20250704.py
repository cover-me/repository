# https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers

from instrument import Instrument
import visa
import types
import logging
import qt

class GS200_20250704(Instrument):

    def __init__(self, name, address, term_chars=''):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['smu'])
        print '%-15s\t%-35s\t%-15s'%(name, address, self.__module__)
        
        self._address = address
        self._visainstrument = visa.instrument(self._address)
        if term_chars:
            self._visainstrument.term_chars = term_chars
        self._visainstrument.clear()
        self._initialize_parameters()
        self.get_all()
        
    def _initialize_parameters(self):
        # Parameters that are class attributes
        self.attribute_parameters = ['_address', '__module__']
        
        # type, flags, units, doc, minval, maxval, format_map
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
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'output': 
            {   
                'get_cmd':'OUTPut?',
                'set_cmd':'OUTPut %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:False,1:True}}
            },
            'source_range': 
            {   
                'get_cmd':':SOUR:RANG?',
                'set_cmd':':SOUR:RANG %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET}
            },
            'source_level': 
            {   
                'get_cmd':'SOUR:LEV?',
                'set_cmd':'SOUR:LEV %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET, 'maxstep':0.01, 'stepdelay':30,}
            },
            'source_protection_current': 
            {   
                'get_cmd':':SOUR:PROT:CURR?',
                'set_cmd':':SOUR:PROT:CURR %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET, 'minval':1e-3, 'maxval':200e-3}
            },
            'measure': 
            {   
                'get_cmd':':SENSe?',
                'set_cmd':':SENSe %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:False,1:True}}
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

