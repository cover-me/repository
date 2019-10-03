### update 2018 by Po ###
# update get_all() to get more parameters
# add dynamic reserve, out filter slope, lockin status
#########################

# SR830.py, to perform the communication between the Wrapper and the device
# Katja Nowack
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from instrument import Instrument
import visa
import types
import logging

class SR830_2018(Instrument):
    '''
    This is the python driver for the Lock-In SR830 from Stanford Research Systems
    signal generator

    Usage:
    Initialize with
    <name> = instruments.create('name', 'SR830', address='<GPIB address>',
        reset=<bool>)
    '''

    def __init__(self, name, address, reset=False):
        '''
        Initializes the SR830, and communicates with the wrapper.

        Input:
            name (string)    : name of the instrument
            address (string) : GPIB address
            reset (bool)     : resets to default values, default=false

        Output:
            None
        '''
        logging.info(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])

        self._address = address
        self._visainstrument = visa.instrument(self._address)

        self.add_parameter('mode',
           flags=Instrument.FLAG_SET,
           type=types.BooleanType)
        
        self.add_parameter('frequency', type=types.FloatType,
            flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET,
            minval=1e-3, maxval=102e3,
            units='Hz', format='%.04e')
        self.add_parameter('amplitude', type=types.FloatType,
            flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET,
            minval=0.004, maxval=5.0,
            units='V', format='%.04e')
        self.add_parameter('phase', type=types.FloatType,
            flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET,
            minval=-360, maxval=729, units='deg')
        self.add_parameter('X', flags=Instrument.FLAG_GET, units='V', type=types.FloatType)
        self.add_parameter('Y', flags=Instrument.FLAG_GET, units='V', type=types.FloatType)
        self.add_parameter('R', flags=Instrument.FLAG_GET, units='V', type=types.FloatType)
        self.add_parameter('P', flags=Instrument.FLAG_GET, units='deg', type=types.FloatType)
        self.add_parameter('status', flags=Instrument.FLAG_GET, units='', type=types.StringType)
        self.add_parameter('tau', type=types.StringType,
            flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET, units='')
        self.add_parameter('out1', type=types.FloatType, flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET, minval=-10.5, maxval=10.5, units='V', format='%.3f')
        self.add_parameter('out2', type=types.FloatType, flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET, minval=-10.5, maxval=10.5, units='V', format='%.3f')
        self.add_parameter('out3', type=types.FloatType, flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET, minval=-10.5, maxval=10.5, units='V', format='%.3f')
        self.add_parameter('out4', type=types.FloatType, flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET, minval=-10.5, maxval=10.5, units='V', format='%.3f')
        
        self.add_parameter('sensitivity', type=types.StringType,
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
        self.get_P()
        self.get_R()
        self.get_X()
        self.get_Y()
        self.get_amplitude()
        self.get_frequency()
        self.get_phase()
        self.get_sensitivity()
        self.get_tau()
        self.get_dynamic()
        self.get_slope()
        self.get_status()

    # communication with machine  
    
    
    def disable_front_panel(self):
        '''
        enables the front panel of the lock-in 
        while being in remote control
        '''
        self._visainstrument.write('OVRM 0')
    
    def auto_phase(self):
        '''
        enables the front panel of the lock-in 
        while being in remote control
        '''
        self._visainstrument.write('APHS')
    
    def enable_front_panel(self):
        '''
        enables the front panel of the lock-in 
        while being in remote control
        '''
        self._visainstrument.write('OVRM 1')
        
    def direct_output(self):
        '''
        select GPIB as interface
        '''
        self._visainstrument.write('OUTX 1')
    
    def read_output(self,output):
        '''
        Read out R,X,Y or phase (P) of the Lock-In
        
        Input:
            mode (int) :
            1 : "X",
            2 : "Y",
            3 : "R"
            4 : "P"
            
        '''
        parameters = {
        1 : "X",
        2 : "Y",
        3 : "R",
        4 : "P"
        }
        self.direct_output()
        if parameters.__contains__(output):
            logging.info(__name__ + ' : Reading parameter from instrument: %s ' %parameters.get(output))
            readvalue = float(self._visainstrument.ask('OUTP?%s' %output))
        else:
            print 'Wrong output requested.'
        return readvalue    
    
    def _do_get_X(self):
        '''
        Read out X of the Lock In
        '''
        return self.read_output(1)
        
    def _do_get_Y(self):
        '''
        Read out Y of the Lock In
        '''
        return self.read_output(2)
    
    def _do_get_R(self):
        '''
        Read out R of the Lock In
        '''
        return self.read_output(3)
    
    def _do_get_P(self):
        '''
        Read out P of the Lock In
        '''
        return self.read_output(4)
    
    def _do_get_status(self):
        '''
        Read the status byte of Lockin. 0 means no error.
        '''
        readvalue = int(self._visainstrument.ask('LIAS?'))
        return '{0:08b}'.format(readvalue)
        
    def _do_set_frequency(self, frequency):
        '''
        Set frequency of the local oscillator

        Input:
            frequency (float) : frequency in Hz

        Output:
            None
        '''
        logging.debug(__name__ + ' : setting frequency to %s Hz' % frequency)
        self._visainstrument.write('FREQ %e' % frequency)

    
    def _do_get_frequency(self):
        '''
        Get the frequency of the local oscillator

        Input:
            None

        Output:
            frequency (float) : frequency in Hz
        '''
        self.direct_output()
        logging.debug(__name__ + ' : reading frequency from instrument')
        return float(self._visainstrument.ask('FREQ?'))

    def _do_get_amplitude(self):
        '''
        Get the frequency of the local oscillator

        Input:
            None

        Output:
            frequency (float) : frequency in Hz
        '''
        self.direct_output()
        logging.debug(__name__ + ' : reading frequency from instrument')
        return float(self._visainstrument.ask('SLVL?'))
 
    def _do_set_mode(self,val):
        logging.debug(__name__ + ' : Setting Reference mode to external' )
        self._visainstrument.write('FMOD %d' %val)
 
 
    def _do_set_amplitude(self, amplitude):
        '''
        Set frequency of the local oscillator

        Input:
            frequency (float) : frequency in Hz

        Output:
            None
        '''
        logging.debug(__name__ + ' : setting amplitude to %s V' % amplitude)
        self._visainstrument.write('SLVL %e' % amplitude)

 
    def _do_set_tau(self,timeconstant):
        '''
        Set the time constant of the LockIn

        Input:
            time constant (integer) : integer from 1 to 19
            time constant (int) :
            0 : "10mus"
            1 : "30mus",
            2 : "100mus",
            3 : "300mus"
            4 : "1ms"
            5 : "3ms"
            6 : "10ms"
            7 : "30ms"
            8 : "100ms"
            9 : "300ms"
            10 : "1s"
            11 : "3s"
            12 : "10s"
            13 : "30s"
            14 : "100s"
            15 : "300s"
            16 : "1ks"
            17 : "3ks"
            18 : "10ks"
            19 : "30ks"
                      
        Output:
            None
        '''
        
        timeconstants = {
        0 : "10mus",
        1 : "30mus",
        2 : "100mus",
        3 : "300mus",
        4 : "1ms",
        5 : "3ms",
        6 : "10ms",
        7 : "30ms",
        8 : "100ms",
        9 : "300ms",
        10 : "1s",
        11 : "3s",
        12 : "10s",
        13 : "30s",
        14 : "100s",
        15 : "300s",
        16 : "1ks",
        17 : "3ks",
        18 : "10ks",
        19 : "30ks"
        }
        timeconstant_int = int(timeconstant)
        if timeconstants.__contains__(timeconstant_int):
                    
            self.direct_output()
            logging.debug(__name__ + ' : setting time constant on instrument to %s'%timeconstants.get(timeconstant_int))
            self._visainstrument.write('OFLT %s' % timeconstant_int)
        else:
            print 'Time constant out of range'

    def _do_get_tau(self):
        '''
        Get the time constant of the LockIn
        
        Input: 
            None
        Output:
            time constant (integer) : integer from 1 to 19
            time constant (int) :
            0 : "10mus"
            1 : "30mus",
            2 : "100mus",
            3 : "300mus"
            4 : "1ms"
            5 : "3ms"
            6 : "10ms"
            7 : "30ms"
            8 : "100ms"
            9 : "300ms"
            10 : "1s"
            11 : "3s"
            12 : "10s"
            13 : "30s"
            14 : "100s"
            15 : "300s"
            16 : "1ks"
            17 : "3ks"
            18 : "10ks"
            19 : "30ks"
                      
        
        '''
        
        timeconstants = {
        0 : "10mus",
        1 : "30mus",
        2 : "100mus",
        3 : "300mus",
        4 : "1ms",
        5 : "3ms",
        6 : "10ms",
        7 : "30ms",
        8 : "100ms",
        9 : "300ms",
        10 : "1s",
        11 : "3s",
        12 : "10s",
        13 : "30s",
        14 : "100s",
        15 : "300s",
        16 : "1ks",
        17 : "3ks",
        18 : "10ks",
        19 : "30ks"
        }                       
        self.direct_output()
        logging.debug(__name__ + ' : getting time constant on instrument')
        ans = int(self._visainstrument.ask('OFLT?'))
        tc_label = timeconstants.get(ans)
        return '%s (%s)'%(ans,tc_label) 

            
    def _do_set_sensitivity(self,sens):
        '''
        Set the sensitivuty of the LockIn

        Input:
            sensitivity (integer) : integer from 1 to 26
            sensitivity (int) :
            0 : "2  nV"
            1 : "5  nV",
            2 : "10 nV",
            3 : "20 nV"
            4 : "50 nV"
            5 : "100nV"
            6 : "200nV"
            7 : "500nV"
            8 : "1muV"
            9 : "2muV"
            10 : "5muV"
            11 : "10muV"
            12 : "20muV"
            13 : "50muV"
            14 : "100muV"
            15 : "200muV"
            16 : "500muV"
            17 : "1mV"
            18 : "2mV"
            19 : "5mV"
            20 : "10mV"
            21 : "20mV"
            22 : "50mV"
            23 : "100mV"
            24 : "200mV"
            25 : "500mV"
            26 : "1V"
           
          
        Output:
            None
        '''
        
        sensitivities = {
        0 : "2  nV",
        1 : "5  nV",
        2 : "10 nV",
        3 : "20 nV",
        4 : "50 nV",
        5 : "100nV",
        6 : "200nV",
        7 : "500nV",
        8 : "1muV",
        9 : "2muV",
        10 : "5muV",
        11 : "10muV",
        12 : "20muV",
        13 : "50muV",
        14 : "100muV",
        15 : "200muV",
        16 : "500muV",
        17 : "1mV",
        18 : "2mV",
        19 : "5mV",
        20 : "10mV",
        21 : "20mV",   
        22 : "50mV",
        23 : "100mV",
        24 : "200mV",
        25 : "500mV",
        26 : "1V"
        }
        sens_int = int(sens)
        if sensitivities.__contains__(sens_int):
            self.direct_output()
            logging.debug(__name__ + ' : setting sensitivity on instrument to %s'%sensitivities.get(sens_int))
            self._visainstrument.write('SENS %d' % sens_int)
        else:
            print 'Sensitivity out of range'
            
            
    def _do_get_sensitivity(self):
        '''
        Set the sensitivuty of the LockIn
            Output:
            sensitivity (integer) : integer from 1 to 26
            sensitivity (int) :
            0 : "2  nV"
            1 : "5  nV",
            2 : "10 nV",
            3 : "20 nV"
            4 : "50 nV"
            5 : "100nV"
            6 : "200nV"
            7 : "500nV"
            8 : "1muV"
            9 : "2muV"
            10 : "5muV"
            11 : "10muV"
            12 : "20muV"
            13 : "50muV"
            14 : "100muV"
            15 : "200muV"
            16 : "500muV"
            17 : "1mV"
            18 : "2mV"
            19 : "5mV"
            20 : "10mV"
            21 : "20mV"
            22 : "50mV"
            23 : "100mV"
            24 : "200mV"
            25 : "500mV"
            26 : "1V"
           

        '''
        sensitivities = {
        0 : "2  nV",
        1 : "5  nV",
        2 : "10 nV",
        3 : "20 nV",
        4 : "50 nV",
        5 : "100nV",
        6 : "200nV",
        7 : "500nV",
        8 : "1muV",
        9 : "2muV",
        10 : "5muV",
        11 : "10muV",
        12 : "20muV",
        13 : "50muV",
        14 : "100muV",
        15 : "200muV",
        16 : "500muV",
        17 : "1mV",
        18 : "2mV",
        19 : "5mV",
        20 : "10mV",
        21 : "20mV",   
        22 : "50mV",
        23 : "100mV",
        24 : "200mV",
        25 : "500mV",
        26 : "1V"
        }
        self.direct_output()
        logging.debug(__name__ + ' : reading sensitivity from instrument')
        ans = int(self._visainstrument.ask('SENS?'))
        sen_label = sensitivities.get(ans)
        return '%s (%s)'%(ans,sen_label) 
        
        
    def _do_set_dynamic(self,dyn):
        dyn_s = {
        "0" : "0 (High)",
        "1" : "1 (Normal)",
        "2" : "2 (Low)"
        }
        if dyn_s.__contains__(dyn):
            self.direct_output()
            logging.debug(__name__ + ' : setting dynamic on instrument to %s'%dyn_s.get(dyn))
            self._visainstrument.write('RMOD %s' % dyn)
        else:
            print 'Dynamic out of range'
            
            
    def _do_get_dynamic(self):
        dyn_s = {
        "0" : "0 (High)",
        "1" : "1 (Normal)",
        "2" : "2 (Low)"
        }
        self.direct_output()
        logging.debug(__name__ + ' : reading dynamic from instrument')
        ans = self._visainstrument.ask('RMOD?')
        return dyn_s.get(ans)

    def _do_set_slope(self,slp):
        slp_s = {
        "0" : "0 (6 dB)",
        "1" : "1 (12 dB)",
        "2" : "2 (18 dB)",
        "3" : "3 (24dB)"
        }
        if slp_s.__contains__(slp):
            self.direct_output()
            logging.debug(__name__ + ' : setting slope on instrument to %s'%slp_s.get(slp))
            self._visainstrument.write('OFSL %s' % slp)
        else:
            print 'Slope out of range'
            
            
    def _do_get_slope(self):
        slp_s = {
        "0" : "0 (6 dB)",
        "1" : "1 (12 dB)",
        "2" : "2 (18 dB)",
        "3" : "3 (24dB)"
        }
        self.direct_output()
        logging.debug(__name__ + ' : reading slope from instrument')
        ans = self._visainstrument.ask('OFSL?')
        return slp_s.get(ans)

    def _do_get_phase(self):
        '''
        Get the reference phase shift

        Input:
            None

        Output:
            phase (float) : reference phase shit in degree
        '''
        self.direct_output()
        logging.debug(__name__ + ' : reading frequency from instrument')
        return float(self._visainstrument.ask('PHAS?'))


    def _do_set_phase(self, phase):
        '''
        Set the reference phase shift

        Input:
            phase (float) : reference phase shit in degree

        Output:
            None
        '''
        logging.debug(__name__ + ' : setting the refernce phase shift to %s degree' %phase)        
        self._visainstrument.write('PHAS %e' % phase)
# fucntions added by Stevan in order to control D/A and A/D convereters 
    def set_aux(self, output, value):
        '''
        Set the voltage on the aux output
        Input: 
            output - number 1-4 (defining which output you are adressing)
            value  - the voltage in Volts
        Output:
            None
        '''
        logging.debug(__name__ + ' : setting the output %(out)i to value %(val).3f' % {'out':output,'val': value})
        self._visainstrument.write('AUXV %(out)i, %(val).3f' % {'out':output,'val':value})
    def read_aux(self, output):
        '''
        Query the voltage on the aux output
        Input: 
            output - number 1-4 (defining which output you are adressing)
        Output:
            voltage on the output D/A converter 
        '''
        logging.debug(__name__ + ' : reading the output %i' %output)
        return float(self._visainstrument.ask('AUXV? %i' %output)) 
    def _do_get_oaux(self, value):
        '''
        Query the voltage on the aux output
        Input: 
            output - number 1-4 (defining which output you are adressing)
        Output:
            voltage on the input A/D converter 
        '''
        logging.debug(__name__ + ' : reading the input %i' %output)
        return float(self._visainstrument.ask('OAUX %(out)i' %output)) 
    
    def _do_get_out1(self):
        return self.read_aux(1);
        
    def _do_set_out1(self,value):
        self.set_aux(1,value);
    def _do_get_out2(self):
        return self.read_aux(2);   
    def _do_set_out2(self,value):
        self.set_aux(2,value);
    def _do_get_out3(self):
        return self.read_aux(3);
    def _do_set_out3(self,value):
        self.set_aux(3,value);
    def _do_get_out4(self):
        return self.read_aux(4);
    def _do_set_out4(self,value):
        self.set_aux(4,value);    
        
    
        