# https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers

from instrument import Instrument
# from time import time, sleep
import visa
import types
import logging
# import math

class Keithley6221_20230430(Instrument):

    def __init__(self, name, address):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])
        self._address = address
        self._visainstrument = visa.instrument(self._address)
        self._visainstrument.clear()

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
            'source_i_level': 
            {   
                'get_cmd':'SOUR:CURR?',
                'set_cmd':'SOUR:CURR %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'maxstep':5e-9, 'stepdelay':30, 'units':'A'}
            },
            'source_range': 
            {
                'get_cmd':':SOUR:CURR:RANG?',
                'set_cmd':':SOUR:CURR:RANG %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET, 'units':'A'}
            },
            'compliance':
            {
                'get_cmd':'SOUR:CURR:COMP?',
                'set_cmd':'SOUR:CURR:COMP %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET, 'units':'V'}
            },
        }
        
        self.add_parameter('Address', flags=Instrument.FLAG_GET, type=types.StringType)
        
        for i in self.dict_parameters:
            cmd = self.dict_parameters[i]['get_cmd']
            if cmd:
                func = lambda cmd=cmd: self._query(cmd)
                setattr(self, 'do_get_%s'%i, func)
            
            cmd = self.dict_parameters[i]['set_cmd']
            if cmd:
                func = lambda x,cmd=cmd: self._execute(cmd%x)
                setattr(self, 'do_set_%s'%i, func)

            self.add_parameter(i, **self.dict_parameters[i]['kw'])

        self.get_all()

    def _execute(self, message):
        return self._visainstrument.write(message)
        
    def _query(self, message):
        return self._visainstrument.ask(message)

    def get_all(self):
        self.get_Address()
        for i in self.dict_parameters:
            self.get(i)
        

    def do_get_Address(self):
        return self._address