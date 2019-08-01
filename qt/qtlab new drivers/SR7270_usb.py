# signal recovery 7270 lockin
# Po, 2018
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

class SR7270_usb(Instrument):
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
    
        