from instrument import Instrument
import visa
import types
import logging

class LI5650_20230204(Instrument):

    def __init__(self, name, address, reset=False):

        logging.info(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])

        self._address = address
        self._visainstrument = visa.instrument(self._address)
        self._visainstrument.clear()
        
        self.add_parameter('ID', flags=Instrument.FLAG_GET, type=types.StringType)
        self.add_parameter('Address', flags=Instrument.FLAG_GET, type=types.StringType)
        
        self.add_parameter('frequency', type=types.FloatType,
            flags=Instrument.FLAG_GETSET,
            minval=1e-3, maxval=200e3,
            units='Hz', format='%.04e')
        self.add_parameter('amplitude', type=types.FloatType,
            flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET,
            minval=0.000, maxval=5.0,
            units='V', format='%.04e')
        self.add_parameter('phase', type=types.FloatType,
            flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET,
            minval=-360, maxval=729, units='deg')
        self.add_parameter('XY', flags=Instrument.FLAG_GET, units='', type=types.ListType)
 
        self.add_parameter('tau', type=types.FloatType,
            flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET, units='s')

        
        self.add_parameter('sensitivity_i', type=types.FloatType,
            flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET, units='')
            
        self.add_parameter('sensitivity_v', type=types.FloatType,
            flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET, units='')
        
        self.add_parameter('dynamic', type=types.StringType,
            flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET,
            units='')
            
        self.add_parameter('slope', type=types.StringType,
            flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET,
            units='')
            
        self.add_function('reset')
        self.add_function('get_all')

        if reset:
            self.reset()
        else:
            self.get_all()

    # Functions
    def reset(self):
        '''
        Resets the instrument to default values

        Input:
            None

        Output:
            None
        '''
        logging.info(__name__ + ' : Resetting instrument')
        self._visainstrument.write('*RST')
        self.get_all()

    def get_all(self):
        '''
        Reads all implemented parameters from the instrument,
        and updates the wrapper.

        Input:
            None

        Output:
            None
        '''
        logging.info(__name__ + ' : reading all settings from instrument')
        self.get_ID()
        self.get_Address()
        self.get_XY()
        self.get_amplitude()
        self.get_frequency()
        self.get_phase()
        self.get_sensitivity_i()
        self.get_sensitivity_v()
        self.get_tau()
        self.get_dynamic()
        self.get_slope()

    def do_get_ID(self):
        return self._visainstrument.ask('*IDN?')
        
    def do_get_Address(self):
        return self._address
        
    def _do_get_XY(self,flag=0):
        '''
        Read XY
        flag, 0 (default): write command and read respond, 1: write only, 2: read only
        '''
        if  flag != 2:
            self._visainstrument.write('FETCH?')
        if flag != 1:
            ans = self._visainstrument.read()
            return [float(i) for i in ans.split(',')]
        return None


    def _do_get_frequency(self):
        return float(self._visainstrument.ask('FREQ?'))
        
    def _do_set_frequency(self, freq):
        self._visainstrument.write(':SOUR:FREQ %s'%freq)

    def _do_get_amplitude(self):
        return float(self._visainstrument.ask('SOUR:VOLT:LEV:IMM:AMPL?'))

    def _do_set_amplitude(self, amplitude):
        self._visainstrument.write('SOUR:VOLT:LEV:IMM:AMPL %s' % amplitude)

 
    def _do_set_tau(self,timeconstant):
        self._visainstrument.write(':FILT:TCON %s' % timeconstant)

    def _do_get_tau(self):
        return float(self._visainstrument.ask(':FILT:TCON?')) 

            
    def _do_set_sensitivity_v(self,sens):
        self._visainstrument.write(':VOLT:AC:RANG %s' % sens)

 
    def _do_get_sensitivity_v(self):
        return float(self._visainstrument.ask(':VOLT:AC:RANG?')) 
        
    def _do_set_sensitivity_i(self,sens):
        self._visainstrument.write(':CURR:AC:RANG %s' % sens)
 
    def _do_get_sensitivity_i(self):
        return float(self._visainstrument.ask(':CURR:AC:RANG?')) 

    def _do_set_dynamic(self,dyn):
        dyn_s = {
        "HIGH" : "HIGH",
        "MED" : "MED",
        "LOW" : "LOW"
        }
        if dyn_s.__contains__(dyn):
            self._visainstrument.write(':DRES %s' % dyn)
        else:
            print 'Dynamic out of range'
            
            
    def _do_get_dynamic(self):
        dyn_s = {
        "HIGH" : "HIGH",
        "MED" : "MED",
        "LOW" : "LOW"
        }
        ans = self._visainstrument.ask(':DRES?')
        return dyn_s.get(ans)

    def _do_set_slope(self,slp):
        slp_s = {
        "6" : "6 dB",
        "12" : "12 dB",
        "18" : "18 dB",
        "24" : "24dB"
        }
        if slp_s.__contains__(slp):
            self._visainstrument.write(':FILT:SLOP %s' % slp)
        else:
            print 'Slope out of range'
            
            
    def _do_get_slope(self):
        slp_s = {
        "6" : "6 dB",
        "12" : "12 dB",
        "18" : "18 dB",
        "24" : "24dB"
        }
        ans = self._visainstrument.ask(':FILT:SLOP?')
        return slp_s.get(ans)

    def _do_get_phase(self):
        return float(self._visainstrument.ask(':PHAS?'))


    def _do_set_phase(self, phase):       
        self._visainstrument.write(':PHAS %s' % phase)
# fucntions added by Stevan in order to control D/A and A/D convereters 
 
        
