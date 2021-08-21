# Keithley_6500, by Po
# Keithley_6500.py driver for Keithley 2100 DMM
# Pieter de Groot <pieterdegroot@gmail.com>, 2008
# Martijn Schaafsma <qtlab@mcschaafsma.nl>, 2008
# Reinier Heeres <reinier@heeres.eu>, 2008 - 2010
#
# Update december 2009:
# Michiel Jol <jelle@michieljol.nl>
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
import numpy
import qt


class Keithley_6500_210821(Instrument):
    '''
    This is the driver for the Keithley 6500 Multimeter

    Usage:
    Initialize with
    <name> = instruments.create(
        '<name>', 'Keithley_6500',
        address='<USB address>')
    '''

    def __init__(self, name, address):
        '''
        Initializes the Keithley_6500, and communicates with the wrapper.

        Input:
            name (string)           : name of the instrument
            address (string)        : USB address
        Output:
            None
        '''
        # Initialize wrapper functions
        logging.info('Initializing instrument Keithley_6500')
        Instrument.__init__(self, name, tags=['physical'])

        # Add some global constants
        self._address = address
        self._visainstrument = visa.instrument(self._address)

        # Add parameters to wrapper
        self.add_parameter('range',
            flags=Instrument.FLAG_GETSET,
            units='', minval=0.1, maxval=1000, type=types.FloatType)
            
        # self.add_parameter('trigger_continuous',
            # flags=Instrument.FLAG_GETSET,
            # type=types.BooleanType)
        # self.add_parameter('trigger_count',
            # flags=Instrument.FLAG_GETSET,
            # units='#', type=types.IntType)
        # self.add_parameter('trigger_delay',
            # flags=Instrument.FLAG_GETSET,
            # units='s', minval=0, maxval=999999.999, type=types.FloatType)
        # self.add_parameter('trigger_source',
            # flags=Instrument.FLAG_GETSET,
            # units='')
        # self.add_parameter('trigger_timer',
            # flags=Instrument.FLAG_GETSET,
            # units='s', minval=0.001, maxval=99999.999, type=types.FloatType)\

        self.add_parameter('id',
            flags=Instrument.FLAG_GET,
            type=types.StringType, units='')
          
        self.add_parameter('mode',
            flags=Instrument.FLAG_GET,
            type=types.StringType, units='')

        self.add_parameter('readlastval', flags=Instrument.FLAG_GET,
            units='V',
            type=types.FloatType,
            tags=['measure'])
        self.add_parameter('readnextval', flags=Instrument.FLAG_GET,
            units='V',
            type=types.FloatType,
            tags=['measure'])
        self.add_parameter('nplc',
            flags=Instrument.FLAG_GETSET,
            units='#', type=types.FloatType, minval=0.01, maxval=15)

        self.add_parameter('averaging', flags=Instrument.FLAG_GETSET,
            type=types.BooleanType)
        self.add_parameter('averaging_count',
            flags=Instrument.FLAG_GETSET,
            units='#', type=types.IntType, minval=1, maxval=100)
        self.add_parameter('averaging_type',
            flags=Instrument.FLAG_GETSET,
            type=types.StringType, units='')

        self.add_function('get_all')
        self.get_all()

    def clear(self):
        self._visainstrument.clear()

    def get_all(self):
        self.get_id()
        self.get_mode()
        self.get_range()
        # self.get_trigger_continuous()
        # self.get_trigger_count()
        # self.get_trigger_delay()
        # self.get_trigger_source()
        # self.get_trigger_timer()
        self.get_nplc()
        self.get_averaging()
        self.get_averaging_count()
        self.get_averaging_type()

    def do_get_readnextval(self):
        '''
        Waits for the next value available and returns it as a float.
        Note that if the reading is triggered manually, a trigger must
        be send first to avoid a time-out.

        Input:
            None

        Output:
            value(float) : last triggerd value on input
        '''
        text = self._visainstrument.ask(':READ?')
        return float(text)

    def do_get_readlastval(self):
        # The insturment seems to be not able to measure continousely in remote mode.
        return self.do_get_readnextval()

    def do_set_range(self, val):
        self._visainstrument.write('VOLT:RANG %f'%val)

    def do_get_range(self):
        ans = self._visainstrument.ask('VOLT:RANG?')
        return float(ans.strip())
        
    # def do_set_trigger_continuous(self, val):
        # self._visainstrument.write(':INIT:CONT %d'%val)

    # def do_get_trigger_continuous(self):
        # ans = self._visainstrument.ask(':INIT:CONT?')
        # return bool(int(ans))
        
    # def do_set_trigger_count(self, val):
        # self._visainstrument.write(':TRIG:COUN %d'%val)

    # def do_get_trigger_count(self):
        # ans = self._visainstrument.ask(':TRIG:COUN?')
        # return int(ans)

    def do_set_nplc(self, val):
        self._visainstrument.write('VOLT:NPLC %f'%val)
        
    def do_get_nplc(self, mode=None, unit='APER'):
        ans = self._visainstrument.ask('VOLT:NPLC?')
        return float(ans)
        
    def do_get_id(self):
        ans = self._visainstrument.ask('*IDN?')
        return ans

    def do_get_mode(self):
        ans = self._visainstrument.ask('FUNC?')
        return ans

    # Only voltage mode is supported    
    # def do_set_mode(self, mode):
        # self._visainstrument.write('FUNC "%s"'%mode)

    def do_set_averaging(self, val):
        self._visainstrument.write('VOLT:AVER:STAT %d'%val)

    def do_get_averaging(self):
        ans = self._visainstrument.ask('VOLT:AVER:STAT?')
        return bool(int(ans))
        
    def do_set_averaging_count(self, val):
        self._visainstrument.write('VOLT:AVER:COUN %d'%val)
        
    def do_get_averaging_count(self):
        ans = self._visainstrument.ask('VOLT:AVER:COUN?')
        return int(ans)

    def do_set_averaging_type(self, type):
        self._visainstrument.write('VOLT:AVER:TCON %s'%val)

    def do_get_averaging_type(self):
        ans = self._visainstrument.ask('VOLT:AVER:TCON?')
        return ans
        

