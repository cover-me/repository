# signal recovery 7270 lockin
# Po, 2018
# 20191002, add frequency, tau, amplitude, sensitivity
 
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


'''
in order to load usb resourses, I commented line 362 in visa.py. This is not a good solution!!!
'''
from instrument import Instrument
import visa
import types
import logging
class instrument_usb(visa.Instrument):
    def __init__(self, resource_name, **keyw):
        visa.ResourceTemplate.__init__(self, resource_name)
        self.term_chars    = keyw.get("term_chars")
        self.chunk_size    = keyw.get("chunk_size", self.chunk_size)
        self.delay         = keyw.get("delay", 0.0)
        #self.send_end      = keyw.get("send_end", True)
        self.values_format = keyw.get("values_format", self.values_format)
        if not self.resource_class:
            warnings.warn("resource class of instrument could not be determined",
                          stacklevel=2)
        elif self.resource_class not in ("INSTR", "RAW", "SOCKET"):
            warnings.warn("given resource was not an INSTR but %s"
                          % self.resource_class, stacklevel=2)

class SR7270_usb_210816(Instrument):
    '''
    This is the python driver for the signal recovery 7270 lockin (usb port).

    Usage:
    Initialize with
    <name> = instruments.create('name', 'SR7270', address='<USB address>')
    '''

    def __init__(self, name, address):
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
        self._visainstrument = instrument_usb(self._address,term_chars='')
        self.add_parameter('X', flags=Instrument.FLAG_GET, units='V', type=types.FloatType)
        self.add_parameter('Y', flags=Instrument.FLAG_GET, units='V', type=types.FloatType)
        self.add_parameter('R', flags=Instrument.FLAG_GET, units='V', type=types.FloatType)
        self.add_parameter('P', flags=Instrument.FLAG_GET, units='D', type=types.FloatType)
        self.add_parameter('frequency', flags=Instrument.FLAG_GET, units='Hz', type=types.FloatType)
        self.add_parameter('tau', flags=Instrument.FLAG_GET, units='s', type=types.FloatType)
        self.add_parameter('amplitude', type=types.FloatType,
            flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET,
            minval=0.0, maxval=5.0,
            units='V', format='%.3f')
        self.add_parameter('sensitivity', type=types.StringType,
            flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET, units='')
        self.add_parameter('ac_gain', type=types.StringType,
            flags=Instrument.FLAG_GETSET | Instrument.FLAG_GET_AFTER_SET, units='')
        self.add_function('get_all')
        self.get_all()

    # Functions
    def get_all(self):
        '''
        Reads all implemented parameters from the instrument,
        and updates the wrapper.

        Input:
            None

        Output:
            None
        '''
        logging.info(__name__ + ' : get all from instrument')
        self.get_X()
        self.get_Y()
        self.get_R()
        self.get_P()
        self.get_frequency()
        self.get_tau()
        self.get_amplitude()
        self.get_sensitivity()
        self.get_ac_gain()
        
    def read_output(self,output):
        logging.info(__name__ + ' : Reading parameter from instrument: %s ' %output)
        readstr = self._visainstrument.ask('%s.\0' %output)
        readvalue = float(readstr[:-4])
        return readvalue  
        
    def _do_get_X(self):
        '''
        Read out X of the Lock In
        '''
        return self.read_output('X')
        
    def _do_get_Y(self):
        '''
        Read out Y of the Lock In
        '''
        return self.read_output('Y')

    def _do_get_R(self):
        '''
        Read out X of the Lock In
        '''
        return self.read_output('MAG')

    def _do_get_P(self):
        '''
        Read out X of the Lock In
        '''
        return self.read_output('PHA')
        
    def _do_get_frequency(self):
        return self.read_output('OF')
    
    def _do_get_tau(self):
        return self.read_output('TC')

    def _do_get_amplitude(self):
        return self.read_output('OA')
        
    def _do_set_amplitude(self, amplitude):
        self._visainstrument.ask('OA. %.3f\0' % amplitude)
        
    def _do_set_sensitivity(self,sens):
        '''
        Set the sensitivuty of the LockIn
        1-27, 2nV-5nV-10nV-....1V
        '''
        sens_int = int(sens)
        if sens_int in range(1,28):
            self._visainstrument.ask('SEN %d\0' % (sens_int))
        else:
            print 'Sensitivity out of range'

    def _do_get_sensitivity(self):
        '''
        Set the sensitivuty of the LockIn
        1-27, 2nV-5nV-10nV-....1V
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
        ans = int(self._visainstrument.ask('SEN\0')[:-4])
        sen_label = sensitivities.get(ans-1)
        return '%s (%s)'%(ans,sen_label) 
        
        
        
    def _do_set_ac_gain(self,ac_amp_str):
        '''
        Set the sensitivuty of the LockIn
        1-27, 2nV-5nV-10nV-....1V
        '''
        ac_amp = int(ac_amp_str)
        if ac_amp in range(0,16):
            self._visainstrument.ask('ACGAIN %d\0' % (ac_amp))
        else:
            print 'Ac gain out of range'

    def _do_get_ac_gain(self):
        '''
        Set the sensitivuty of the LockIn
        1-27, 2nV-5nV-10nV-....1V
        '''
        sensitivities = {
        0 : "0dB,2V",
        1 : "6dB,1V",
        2 : "12dB,500mV",
        3 : "18dB,250mV",
        4 : "24dB,125mV",
        5 : "30dB,62mV",
        6 : "36dB,31mV",
        7 : "42dB,16mV",
        8 : "48dB,8mV",
        9 : "54dB,4mV",
        10 : "60dB,2mV",
        11 : "66dB,1mV",
        12 : "72dB,500uV",
        13 : "78dB,250uV",
        14 : "84dB",
        15 : "90dB",
        }
        ans = int(self._visainstrument.ask('ACGAIN\0')[:-4])
        sen_label = sensitivities.get(ans)
        return '%s (%s)'%(ans,sen_label) 
        
        
