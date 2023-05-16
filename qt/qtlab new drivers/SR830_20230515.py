# https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers

from instrument import Instrument
import visa
import types
import logging

class SR830_20230515(Instrument):

    def __init__(self, name, address):
        logging.info(__name__ + ' : Initializing instrument')
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
        
        format_map_tau = {
        0 : "10 us",
        1 : "30 us",
        2 : "100 us",
        3 : "300 us",
        4 : "1 ms",
        5 : "3 ms",
        6 : "10 ms",
        7 : "30 ms",
        8 : "100 ms",
        9 : "300 ms",
        10 : "1 s",
        11 : "3 s",
        12 : "10 s",
        13 : "30 s",
        14 : "100 s",
        15 : "300 s",
        16 : "1 ks",
        17 : "3 ks",
        18 : "10 ks",
        19 : "30 ks"
        }
        
        format_map_sensitivity = {
        0 : "2 nV fA",
        1 : "5 nV fA",
        2 : "10 nV fA",
        3 : "20 nV fA",
        4 : "50 nV fA",
        5 : "100 nV fA",
        6 : "200 nV fA",
        7 : "500 nV fA",
        8 : "1 uV pA",
        9 : "2 uV pA",
        10 : "5 uV pA",
        11 : "10 uV pA",
        12 : "20 uV pA",
        13 : "50 uV pA",
        14 : "100 uV pA",
        15 : "200 uV pA",
        16 : "500 uV pA",
        17 : "1 mV nA",
        18 : "2 mV nA",
        19 : "5 mV nA",
        20 : "10 mV nA",
        21 : "20 mV nA",   
        22 : "50 mV nA",
        23 : "100 mV nA",
        24 : "200 mV nA",
        25 : "500 mV nA",
        26 : "1 V uA"
        }
        
        # Other paramters, use get_cmd and set_cmd, or leave them blank and manually define get/set functions.
        self.dict_parameters = { 
            'ID':
            {
                'get_cmd':'*IDN?',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'reference':
            {   
                'get_cmd':'FMOD?',
                'set_cmd':'FMOD %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"External",1:"Internal"}}
            },
            'input':
            {   
                'get_cmd':'ISRC?',
                'set_cmd':'ISRC %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"A",1:"A-B",2:'I 1M',3:'I 100M'}}
            },
            'input_ground':
            {   
                'get_cmd':'IGND?',
                'set_cmd':'IGND %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"Float",1:"Ground"}}
            },
            'input_coupling':
            {   
                'get_cmd':'ICPL?',
                'set_cmd':'ICPL %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"AC",1:"DC"}}
            },
            'reference':
            {   
                'get_cmd':'FMOD?',
                'set_cmd':'FMOD %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"External",1:"Internal"}}
            },
            'reference_trigger':
            {   
                'get_cmd':'RSLP?',
                'set_cmd':'RSLP %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"Sine zero",1:"TTL rising edge",2:'TTL falling edge'}}
            },
            'filter_notch':
            {   
                'get_cmd':'ILIN?',
                'set_cmd':'ILIN %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"OFF",1:"Line",2:'2*Line',3:'Both'}}
            },
            'filter_sync':
            {   
                'get_cmd':'SYNC?',
                'set_cmd':'SYNC %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"OFF",1:"ON (< 200 Hz)"}}
            },                
            'frequency': 
            {   
                'get_cmd':'FREQ?',
                'set_cmd':'FREQ %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'minval':1e-3,'maxval':102e3,'units':'Hz'}
            },            
            'amplitude': 
            {   
                'get_cmd':'SLVL?',
                'set_cmd':'SLVL %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'minval':0.004,'maxval':5.000,'units':'V'}
            },
            'harmonic': 
            {   
                'get_cmd':'HARM?',
                'set_cmd':'HARM %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'minval':1,'maxval':19999}
            },               
            'phase_shift': 
            {   
                'get_cmd':'PHAS?',
                'set_cmd':'PHAS %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'minval':-360.00,'maxval':729.99,'units':'deg'}
            },
            'XY': 
            {   
                'get_cmd':'SNAP?1,2',
                'set_cmd':'',
                'kw':{'type':types.ListType,'flags':Instrument.FLAG_GET}
            },      
            'RP': 
            {   
                'get_cmd':'SNAP?3,4',
                'set_cmd':'',
                'kw':{'type':types.ListType,'flags':Instrument.FLAG_GET}
            },      
            'XYRP': 
            {   
                'get_cmd':'SNAP?1,2,3,4',
                'set_cmd':'',
                'kw':{'type':types.ListType,'flags':Instrument.FLAG_GET}
            },      
            'status': 
            {   
                'get_cmd':'LIAS?',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },      
            'tau': 
            {   
                'get_cmd':'OFLT?',
                'set_cmd':'OFLT %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':format_map_tau}
            },      
            'out1': 
            {   
                'get_cmd':'AUXV?1',
                'set_cmd':'AUXV 1, %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'minval':-10.5,'maxval':10.5,'units':'V','format':'%.3f'}
            },      
            'out2': 
            {   
                'get_cmd':'AUXV?2',
                'set_cmd':'AUXV 2, %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'minval':-10.5,'maxval':10.5,'units':'V','format':'%.3f'}
            },      
            'out3': 
            {   
                'get_cmd':'AUXV?3',
                'set_cmd':'AUXV 3, %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'minval':-10.5,'maxval':10.5,'units':'V','format':'%.3f'}
            },      
            'out4': 
            {   
                'get_cmd':'AUXV?4',
                'set_cmd':'AUXV 4, %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'minval':-10.5,'maxval':10.5,'units':'V','format':'%.3f'}
            },      
            'sensitivity': 
            {   
                'get_cmd':'SENS?',
                'set_cmd':'SENS %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':format_map_sensitivity}
            },      
            'dynamic': 
            {   
                'get_cmd':'RMOD?',
                'set_cmd':'RMOD %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"High",1:"Normal",2:"Low"}}
            },      
            'slope': 
            {   
                'get_cmd':'OFSL?',
                'set_cmd':'OFSL %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"6 dB",1:"12 dB",2:"18 dB",3:"24 dB"}}
            },   
            'front_panel_enable_in_remote': 
            {   
                'get_cmd':'OVRM?',
                'set_cmd':'OVRM %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:False,1:True}}
            },   
        }
        
        self._add_parameters()

    def _parse(self, ans, message):
        if message.startswith('SNAP?'):
            return [float(i) for i in ans.split(',')]
        elif message=='LIAS?':
            return '{0:08b}'.format(int(ans))
        else:
            return ans

    def auto_phase(self):
        '''
        enables the front panel of the lock-in 
        while being in remote control
        '''
        self._visainstrument.write('APHS')
        
    
    def get_all(self):
        for i in self.attribute_parameters:
            para_name = i.strip('_').upper()
            self.get(para_name)
        for i in self.dict_parameters:
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

        # Add other parameters
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
