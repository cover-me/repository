from instrument import Instrument
import visa
import types
import logging

class LI5650_20230529(Instrument):

    def __init__(self, name, address, reset=False):
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
            'frequency':
            {
                'get_cmd':'FREQ?',
                'set_cmd':':SOUR:FREQ %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'units':'Hz','minval':1e-3, 'maxval':200e3}
            },
            'amplitude':
            {
                'get_cmd':'SOUR:VOLT:LEV:IMM:AMPL?',
                'set_cmd':'SOUR:VOLT:LEV:IMM:AMPL %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'units':'V','minval':0.000, 'maxval':5.0}
            },
            'phase':
            {
                'get_cmd':':PHAS?',
                'set_cmd':':PHAS %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'units':'deg','minval':-360, 'maxval':729}
            }, 
            'tau':
            {
                'get_cmd':':FILT:TCON?',
                'set_cmd':':FILT:TCON %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET,'units':'s'}
            }, 
            'sensitivity_i':
            {
                'get_cmd':':CURR:AC:RANG?',
                'set_cmd':':CURR:AC:RANG %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET,'units':''}
            }, 
            'sensitivity_v':
            {
                'get_cmd':':VOLT:AC:RANG?',
                'set_cmd':':VOLT:AC:RANG %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET,'units':''}
            }, 
            'dynamic':
            {
                'get_cmd':':DRES?',
                'set_cmd':':DRES %s',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET,'units':'', 'format_map':{"HIGH" : "HIGH", "MED" : "MED", "LOW" : "LOW"}}
            }, 
            'slope':
            {
                'get_cmd':':FILT:SLOP?',
                'set_cmd':':FILT:SLOP %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET,'units':'dB', 'format_map':{6 : 6, 12 : 12, 18 : 18, 24: 24}}
            }, 
            'XY':
            {
                'get_cmd':'FETCH?',
                'set_cmd':'',
                'kw':{'type':types.ListType,'flags':Instrument.FLAG_GET,'units':''}
            },          
        }
        
        self._add_parameters()# add attribute_parameters and dict_parameters


    def _parse(self, ans, message):
        if message == 'FETCH?':
            return [float(i) for i in ans.split(',')]
        else:
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
