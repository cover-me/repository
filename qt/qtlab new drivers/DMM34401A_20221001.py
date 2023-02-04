from instrument import Instrument
import visa
import types
import logging

class DMM34401A_20221001(Instrument):

    def __init__(self, name, address, reset=False):
        Instrument.__init__(self, name, tags=['physical'])

        self._address = address
        self._visainstrument = visa.instrument(self._address)
        self._visainstrument.clear()
        
        self.add_parameter('ID', flags=Instrument.FLAG_GET, type=types.StringType)
        self.add_parameter('address', flags=Instrument.FLAG_GET, type=types.StringType)
        self.add_parameter('function', flags=Instrument.FLAG_GET, type=types.StringType)
        self.add_parameter('range', flags=Instrument.FLAG_GET, type=types.FloatType)
        self.add_parameter('auto_range', flags=Instrument.FLAG_GET, type=types.StringType)
        self.add_parameter('auto_impedance', flags=Instrument.FLAG_GET, type=types.StringType)
        self.add_parameter('auto_zero', flags=Instrument.FLAG_GET, type=types.StringType)
        self.add_parameter('math', flags=Instrument.FLAG_GET, type=types.StringType)
        self.add_parameter('terminals', flags=Instrument.FLAG_GET, type=types.StringType)
        self.add_parameter('resolution', flags=Instrument.FLAG_GET, type=types.FloatType)
        self.add_parameter('NPLC', flags=Instrument.FLAG_GET, type=types.FloatType)
        self.add_parameter('val', flags=Instrument.FLAG_GET,
            units='',
            type=types.FloatType,
            tags=['measure'])
            
        self.get_all()
        
    def get_all(self):
        self.get_ID()
        self.get_address()
        self.get_function()
        self.get_range()
        self.get_auto_range()
        self.get_auto_impedance()
        self.get_auto_zero()
        self.get_math()
        self.get_terminals()
        self.get_resolution()
        self.get_NPLC()
        self.get_val()
        
    def do_get_ID(self):
        return self._visainstrument.ask('*IDN?')
        
    def do_get_address(self):
        return self._address
        
    def do_get_function(self):
        return self._visainstrument.ask('FUNC?').strip('"')
        
    def do_get_range(self):
        func_name = self.get_function().split(':')[0]
        return float(self._visainstrument.ask('%s:RANG?'%func_name))

    def do_get_auto_range(self):
        func_name = self.get_function().split(':')[0]
        ans = self._visainstrument.ask('%s:RANG:AUTO?'%func_name)
        if ans=='1':
            return 'on'
        else:
            return 'off'
 
    def do_get_auto_impedance(self):
        ans = self._visainstrument.ask('INPut:IMPedance:AUTO?')
        if ans=='1':
            return 'on'
        else:
            return 'off'

    def do_get_auto_zero(self):
        ans = self._visainstrument.ask('ZERO:AUTO?')
        if ans=='1':
            return 'on'
        else:
            return 'off'    
    
    def do_get_math(self):
        ans = self._visainstrument.ask('CALCulate:STATe?')
        if ans=='1':
            return 'on'
        else:
            return 'off'
            
    def do_get_terminals(self):
        return self._visainstrument.ask('ROUTe:TERMinals?')
            
    def do_get_resolution(self):
        func_name = self.get_function().split(':')[0]
        return float(self._visainstrument.ask('%s:RES?'%func_name))

    def do_get_NPLC(self):
        func_name = self.get_function().split(':')[0]
        return float(self._visainstrument.ask('%s:NPLC?'%func_name))
        
    def _do_get_val(self,flag=0):
        if  flag != 2:
            self._visainstrument.write('READ?')
        if flag != 1:
            ans = self._visainstrument.read()
            return float(ans)
        return None
        
