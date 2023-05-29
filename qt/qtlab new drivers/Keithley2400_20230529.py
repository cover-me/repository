# https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers

from instrument import Instrument
# from time import time, sleep
import visa
import types
import logging
# import math

class Keithley2400_20230529(Instrument):

    def __init__(self, name, address):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])
        print '%-15s\t%-35s\t%-15s'%(name, address, self.__module__)
        
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
            'output_status': 
            {   
                'get_cmd':':OUTP?',
                'set_cmd':':OUTP %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"OFF",1:"ON"}}
            },
            'source_type': 
            {   
                'get_cmd':'SOUR:FUNC?',
                'set_cmd':'SOUR:FUNC %s',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GETSET,'format_map':{'VOLT':'VOLT','CURR':'CURR'}}
            },
            'source_range': 
            {   
                'get_cmd':'',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET}
            },
            'source_i_level': 
            {   
                'get_cmd':'SOUR:CURR?',
                'set_cmd':'SOUR:CURR %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'maxstep':1e-9, 'stepdelay':30, 'units':'A'}
            },
            'source_v_level': 
            {   
                'get_cmd':'SOUR:VOLT?',
                'set_cmd':'SOUR:VOLT %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'maxstep':5e-3, 'stepdelay':30, 'units':'V'}
            },
            'compliance': 
            {   
                'get_cmd':'',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET}
            },
            'nplc': 
            {   
                'get_cmd':'NPLC?',
                'set_cmd':'NPLC %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET}
            },
            'sense_type': 
            {   
                'get_cmd':'SENS:FUNC?',
                'set_cmd':'SENS:FUNC %s',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GETSET,'format_map':{'"VOLT"':'VOLT','"CURR"':'CURR'}}
            },
            'sense_range': 
            {   
                'get_cmd':'',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET}
            },
            'vals': 
            {   
                'get_cmd':'read?',
                'set_cmd':'',
                'kw':{'type':types.ListType,'flags':Instrument.FLAG_GET}
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
            return self._parse(ans,message)
        return None
            
    def _parse(self, ans, message):
        if message == 'read?':
            ans = ans.split(',')
            volt, curr, res, ts, status = [float(i) for i in ans]
            return [volt, curr]
        elif message == 'NPLC?':
            return float(ans)
        return ans    

    def get_all(self):
        for i in self.attribute_parameters:
            para_name = i.strip('_').upper()
            self.get(para_name)
        for i in self.dict_parameters:
            self.get(i)

                    
    def do_get_source_range(self):# source_range
        stype = self.get_source_type()
        d = {'VOLT':'VOLT','CURR':'CURR'}
        if stype in d:
            return float(self._query(':SOUR:%s:RANG?'%d[stype]))
        else:
            print 'Unknown source type!'

    def do_set_source_range(self, x):
        stype = self.get_source_type()
        d = {'VOLT':'VOLT','CURR':'CURR'}
        if stype in d:
            self._execute(':SOUR:%s:RANG %s'%(d[stype],x))
        else:
            print 'Unknown source type!'
        
    def do_get_compliance(self):# compliance
        stype = self.get_source_type()
        d2 = {'VOLT':'CURR','CURR':'VOLT'}
        if stype in d2:
            return float(self._query(':SENS:%s:PROT?'%d2[stype]))
        else:
            print 'Unknown source type!'
            
    def do_set_compliance(self, x):
        stype = self.get_source_type()
        d2 = {'VOLT':'CURR','CURR':'VOLT'}
        if stype in d2:
            self._execute(':SENS:%s:PROT %s'%(d2[stype],x))
        else:
            print 'Unknown source type!' 

    def do_get_sense_range(self):# sense_range
        stype = self.get_source_type()
        d2 = {'VOLT':'CURR','CURR':'VOLT'}       
        if stype in d2:
            return float(self._query(':SENS:%s:RANG?'%d2[stype]))
        else:
            print 'Unknown source type!' 
            
    def do_set_sense_range(self, x):
        stype = self.get_source_type()
        d2 = {'VOLT':'CURR','CURR':'VOLT'}
        if stype in d2:
            self._execute(':SENS:%s:RANG %s'%(d2[stype],x))
        else:
            print 'Unknown source type!'
        







