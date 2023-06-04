# https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers

from instrument import Instrument
import visa,time
import types
import logging

class SR860_20230604(Instrument):

    def __init__(self, name, address, term_chars = None):
        logging.info(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['lockin'])
        print '%-15s\t%-35s\t%-15s'%(name, address, self.__module__)

        self._address = address
        self._visainstrument = visa.instrument(self._address, timeout=2, term_chars = term_chars)
        self._visainstrument.clear()
        self._initialize_parameters()
        self.get_all()
        

    def _initialize_parameters(self):
        # Parameters that are class attributes
        self.attribute_parameters = ['_address', '__module__']
        
        tau_list = [
            '1 us', '3 us', "10 us", "30 us", "100 us",
            "300 us", "1 ms", "3 ms", 
            "10 ms", "30 ms", "100 ms",
            "300 ms", "1 s", "3 s", 
            "10 s", "30 s", "100 s",
            "300 s", "1 ks", "3 ks",
            "10 ks", "30 ks"
        ]
        format_map_tau = dict(zip(range(len(tau_list)),tau_list))

        sensitivity_list = [
            "1 nV fA", "2 nV fA", "5 nV fA",
            "10 nV fA", "20 nV fA", "50 nV fA",
            "100 nV fA", "200 nV fA", "500 nV fA",
            "1 uV pA", "2 uV pA", "5 uV pA",
            "10 uV pA", "20 uV pA", "50 uV pA",
            "100 uV pA", "200 uV pA", "500 uV pA",
            "1 mV nA", "2 mV nA", "5 mV nA",
            "10 mV nA", "20 mV nA", "50 mV nA",
            "100 mV nA", "200 mV nA", "500 mV nA",
            "1 V uA"]
        format_map_sensitivity = dict(zip(range(len(sensitivity_list)-1,-1,-1),sensitivity_list))
        
        # Other paramters, use get_cmd and set_cmd, or leave them blank and manually define get/set functions.
        self.dict_parameters = { 
            'ID':
            {
                'get_cmd':'*IDN?',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'input_iv_mode':
            {   
                'get_cmd':'IVMD?',
                'set_cmd':'IVMD %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"VOLT",1:"CURR"}}
            },
            'input_v_source':
            {   
                'get_cmd':'ISRC?',
                'set_cmd':'ISRC %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:'A',1:'A-B'}}
            },
            'input_v_ground':
            {   
                'get_cmd':'IGND?',
                'set_cmd':'IGND %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"Float",1:"Ground"}}
            },
            'input_v_coupling':
            {   
                'get_cmd':'ICPL?',
                'set_cmd':'ICPL %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"AC",1:"DC"}}
            },
            'input_v_range':
            {   
                'get_cmd':'IRNG?',
                'set_cmd':'IRNG %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"1 V",1:"300 mV",2:'100 mV',3:'30 mV', 4:'10 mV'}}
            },
            'input_i_gain':
            {   
                'get_cmd':'ICUR?',
                'set_cmd':'ICUR %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"1 M, 1 uA",1:"100 M, 10 nA"}}
            },
            'input_v_range_level':
            {   
                'get_cmd':'ILVL?',
                'set_cmd':'',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GET,'format_map':{0:"0",1:"1",2:"2",3:"3",4:"4 (overload)"}}
            },        
            'sensitivity': 
            {   
                'get_cmd':'SCAL?',
                'set_cmd':'SCAL %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':format_map_sensitivity}
            },         
            'tau': 
            {   
                'get_cmd':'OFLT?',
                'set_cmd':'OFLT %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':format_map_tau}
            },   
            'filter_slope': 
            {   
                'get_cmd':'OFSL?',
                'set_cmd':'OFSL %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"6 dB",1:"12 dB",2:"18 dB",3:"24 dB"}}
            }, 
            'filter_sync':
            {   
                'get_cmd':'SYNC?',
                'set_cmd':'SYNC %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"OFF",1:"ON"}}
            },  
            'filter_adv':
            {   
                'get_cmd':'ADVFILT?',
                'set_cmd':'ADVFILT %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"OFF",1:"ON"}}
            },
            'equivalent_noise_bandwidth':
            {   
                'get_cmd':'ENBW?',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GET,'units':'Hz'}
            },               
            'out1': 
            {   
                'get_cmd':'AUXV? 0',
                'set_cmd':'AUXV 0, %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'minval':-10.5,'maxval':10.5,'units':'V'}
            },      
            'out2': 
            {   
                'get_cmd':'AUXV? 1',
                'set_cmd':'AUXV 1, %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'minval':-10.5,'maxval':10.5,'units':'V'}
            },      
            'out3': 
            {   
                'get_cmd':'AUXV? 2',
                'set_cmd':'AUXV 2, %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'minval':-10.5,'maxval':10.5,'units':'V'}
            },      
            'out4': 
            {   
                'get_cmd':'AUXV? 3',
                'set_cmd':'AUXV 3, %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'minval':-10.5,'maxval':10.5,'units':'V'}
            },  
            'val_XY': 
            {   
                'get_cmd':'SNAP? 0,1',
                'set_cmd':'',
                'kw':{'type':types.ListType,'flags':Instrument.FLAG_GET}
            },      
            'val_RP': 
            {   
                'get_cmd':'SNAP? 2,3',
                'set_cmd':'',
                'kw':{'type':types.ListType,'flags':Instrument.FLAG_GET}
            },      
            'val_DATA': 
            {   
                'get_cmd':'SNAPD?',
                'set_cmd':'',
                'kw':{'type':types.ListType,'flags':Instrument.FLAG_GET}
            },
            'status': 
            {   
                'get_cmd':'LIAS?',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },  
            'sine_out_amplitude': 
            {   
                'get_cmd':'SLVL?',
                'set_cmd':'SLVL %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'minval':1e-9,'maxval':2,'units':'V'}
            },
            'sine_out_dc': 
            {   
                'get_cmd':'SOFF?',
                'set_cmd':'SOFF %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'minval':-5,'maxval':5,'units':'V'}
            },
            'sine_out_dc_mode': 
            {   
                'get_cmd':'REFM?',
                'set_cmd':'REFM %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:'Common',1:'Difference'}}
            },
            'harmonic': 
            {   
                'get_cmd':'HARM?',
                'set_cmd':'HARM %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'minval':1,'maxval':99}
            },   
            'phase_shift': 
            {   
                'get_cmd':'PHAS?',
                'set_cmd':'PHAS %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'minval':-180.00,'maxval':180,'units':'deg'}
            },
            # 'front_panel_enable_in_remote': 
            # {   
                # 'get_cmd':'OVRM?',
                # 'set_cmd':'OVRM %s',
                # 'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:False,1:True}}
            # },  
            'frequency': 
            {   
                'get_cmd':'FREQ?',
                'set_cmd':'FREQ %s',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GETSET,'minval':1e-3,'maxval':500e3,'units':'Hz'}
            },  
            'timebase_mode':
            {   
                'get_cmd':'TBMODE?',
                'set_cmd':'TBMODE %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"Auto",1:"Internal"}}
            },
            'timebase_status':
            {   
                'get_cmd':'TBMODE?',
                'set_cmd':'TBMODE %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GET,'format_map':{0:"External",1:"Internal"}}
            },
            'reference_source':
            {   
                'get_cmd':'RSRC?',
                'set_cmd':'RSRC %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"Internal",1:"External",2:"Dual",3:"Chop"}}
            },
            'reference_trigger':
            {   
                'get_cmd':'RTRG?',
                'set_cmd':'RTRG %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"Sine zero, > 1 Hz",1:"TTL rising edge",2:'TTL falling edge'}}
            },
            'reference_input_impedence':
            {   
                'get_cmd':'REFZ?',
                'set_cmd':'REFZ %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"50 ohm",1:"1 Mohm"}}
            },
            'blazex_mode':
            {   
                'get_cmd':'BLAZEX?',
                'set_cmd':'BLAZEX %s',
                'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"blazex",1:"bipolar sync, -2 to 2 V",2:"unipolar sync, 0 to 2 V"}}
            },
        }
        
        self._add_parameters()

    def _parse(self, ans, message):
        if message.startswith('SNAP?') or message=='SNAPD?':
            return [float(i) for i in ans.split(',')]
        elif message=='LIAS?':
            return '{0:08b}'.format(int(ans))
        else:
            return ans

    def get_all(self):
        time.sleep(0.01)# delay after visa.clear(), for sr860 only
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
        
    # def _query(self, message):
        # ans = self._visainstrument.ask(message)
        # return self._parse(ans,message)
