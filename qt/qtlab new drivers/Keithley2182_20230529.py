# https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers

from instrument import Instrument
# from time import time, sleep
import visa
import types
import logging
# import math
import qt

class Keithley2182_20230619(Instrument):
    CHANGE_TRIGGER_SOURCE = True
    CHANGE_DISPLAY = True

    def __init__(self, name, address):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['dmm'])
        print '%-15s\t%-35s\t%-15s'%(name, address, self.__module__)
        
        self._address = address
        self._visainstrument = visa.instrument(self._address, timeout=2)
        self._visainstrument.clear()
        self._initialize_parameters()
        self.get_all()
        
        qt.flow.connect('measurement-start', self._measurement_start_cb)
        qt.flow.connect('measurement-end', self._measurement_end_cb)

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
            'channel': 
            {   
                'get_cmd':':SENS:CHAN?',
                'set_cmd':':SENS:CHAN %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{1:"CHAN1",2:"CHAN2"}}
            },
            'nplc': 
            {
                'get_cmd':':SENS:VOLT:NPLC?',
                'set_cmd':':SENS:VOLT:NPLC %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET}
            },
            'val':
            {   
                'get_cmd':'',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GET, 'units':'V',
                    'doc': 'If trigger_source == IMM, use :FETCH?\nIf trigger_source == BUS, use *TRG;:FETCH? to forcely refresh the buffer.\nSee also change_trigger_source.'}
            },
            'initiate_continuous': 
            {   
                'get_cmd':':INIT:CONT?',
                'set_cmd':':INIT:CONT %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET, 'format_map':{0:False,1:True}}
            },
            'trigger_source': 
            {   
                'get_cmd':':TRIGger:SOURce?',
                'set_cmd':':TRIGger:SOURce %s',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET, 'format_map':{'IMM':"immediate",'MAN':"manual",'TIM':"timer",'EXT':"external",'BUS':"bus",}}
            },
            'trigger_count': # 1 to 9999 or INF (+9.9e37)
            {   
                'get_cmd':':TRIG:COUN?',
                'set_cmd':':TRIG:COUN %s',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET}
            },
            'trigger_delay': 
            {   
                'get_cmd':':TRIG:DEL?',
                'set_cmd':':TRIG:DEL %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'minval':0, 'maxval':999999.999}
            },
            'trigger_delay_auto': 
            {   
                'get_cmd':':TRIG:DEL:AUTO?',
                'set_cmd':':TRIG:DEL:AUTO %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'format_map':{0:False,1:True}}
            },
            'line_sync': 
            {   
                'get_cmd':':SYSTem:LSYNc?',
                'set_cmd':':SYSTem:LSYNc %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET,'format_map':{0:False,1:True}}
            },
            'ch1_analog_filter': 
            {   
                'get_cmd':':SENS:VOLT:CHAN1:LPAS:STAT?',
                'set_cmd':':SENS:VOLT:CHAN1:LPAS:STAT %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:False,1:True}}
            },
            'ch1_digital_filter': 
            {   
                'get_cmd':':SENS:VOLT:CHAN1:DFIL:STAT?',
                'set_cmd':':SENS:VOLT:CHAN1:DFIL:STAT %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:False,1:True}}
            },  
            'ch1_range': 
            {
                'get_cmd':':SENS:VOLT:CHAN1:RANG?',
                'set_cmd':':SENS:VOLT:CHAN1:RANG %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET, 'units':'V'}
            },
            'digits': 
            {
                'get_cmd':':SENS:VOLT:DC:DIG?',
                'set_cmd':':SENS:VOLT:DC:DIG %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET}
            },            
            'auto_zero': 
            {   
                'get_cmd':':SYST:AZER:STAT?',
                'set_cmd':':SYST:AZER:STAT %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:False,1:True}}
            },
            'auto_zero_front': 
            {   
                'get_cmd':':SYST:FAZ?',
                'set_cmd':':SYST:FAZ %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:False,1:True}}
            },
            'display': 
            {   
                'get_cmd':':DISPlay:ENABle?',
                'set_cmd':':DISPlay:ENABle %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:False,1:True}}
            },
            'change_display': 
            {
                'kw':{'type':types.BooleanType,'flags':Instrument.FLAG_GETSET,
                'doc': 'Turn display OFF (ON) before (after) a measurement to increase the speed.'}
            },
            'change_trigger_source': 
            {
                'kw':{'type':types.BooleanType,'flags':Instrument.FLAG_GETSET,
                'doc': 'Set trigger_source to BUS (IMM) before (after) a measurement.'}
            },
            
        }

        self._add_parameters()# add attribute_parameters and dict_parameters
        self.set_change_display(self.CHANGE_DISPLAY)
        self.set_change_trigger_source(self.CHANGE_TRIGGER_SOURCE)
        
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
            if i != 'val':
                self.get(i)
        self.get('val')
        
    def _get_parameter_fast(self, name):
        p = self.get_parameters()
        if name in p:
            val = p[name]['value']
            if val is None:
                return self.get(name)
            else:
                return val
        else:
            return None

    def do_get_val(self,flag=0):
        trg_source = self._get_parameter_fast('trigger_source')
        if trg_source == 'BUS':
            return self._query('*TRG;:FETCH?',flag)
        elif trg_source == 'IMM':
            return self._query(':FETCH?',flag)
        else:
            print 'Keithley2182: To get "val", please set "trigger_source" to "BUS" or "IMM"'
            return None
            
    def _measurement_start_cb(self, sender):
        if self.get_change_display():
            print "Kethley 2182: Turn off the display to increase the speed."
            self.set_display(0)
        if self.get_change_trigger_source():
            print "Kethley 2182: Set trigger_source to BUS to use the trigger-and-read mode."
            self.set_trigger_source('BUS')

    def _measurement_end_cb(self, sender):
        if self.get_change_display():
            print "Kethley 2182: Turn on the display"
            self.set_display(1)
        if self.get_change_trigger_source():
            print "Kethley 2182: Set trigger_source to IMMediate (continuously measure)."
            self.set_trigger_source('IMM')