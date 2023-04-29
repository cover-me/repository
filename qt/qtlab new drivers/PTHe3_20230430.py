# https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers

from instrument import Instrument
# from time import time, sleep
import visa
import types
import logging
# import math

class PTHe3_20230430(Instrument):

    def __init__(self, name, address):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])
        self._address = address
        self._visainstrument = visa.instrument(self._address, term_chars = '\n')
        self._visainstrument.clear()
        
        self.add_parameter('ID', flags=Instrument.FLAG_GET, type=types.StringType)
        self.add_parameter('Address', flags=Instrument.FLAG_GET, type=types.StringType)
        
        # self.add_parameter('something', type=types.FloatType, flags=Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET, maxstep=1e-3, stepdelay=30, units='V')
        # self.add_parameter('state', type=types.StringType, flags=Instrument.FLAG_GET)
        self.add_parameter('state', type=types.StringType, flags=Instrument.FLAG_GET)
        self.add_parameter('he3pot', type=types.FloatType, flags=Instrument.FLAG_GET)
        self.add_parameter('1kpot', type=types.FloatType, flags=Instrument.FLAG_GET)
        self.add_parameter('sorb', type=types.FloatType, flags=Instrument.FLAG_GET)
        self.get_all()
        
    def _query(self, message):
        return self._visainstrument.ask(message).split(':')[-1]

    def get_all(self):
        self.get_ID()
        self.get_Address()
        self.get_state()
        self.get_he3pot()
        self.get_1kpot()
        self.get_sorb()

    # getting and setting functions
    def do_get_ID(self):# ID
        ans = self._visainstrument.ask('*IDN?')
        return ans[4:]

    def do_get_Address(self):# Address
        return self._address
   
    def do_get_state(self):# state
        return self._query('READ:DEV:HelioxX:HEL:SIG:STAT')
        
    def do_get_he3pot(self):# state
        ans = self._query('READ:DEV:HelioxX:HEL:SIG:TEMP')
        return float(ans[:-1])
        
    def do_get_1kpot(self):# state
        ans = self._query('READ:DEV:DB6.T1:TEMP:SIG:TEMP')
        return float(ans[:-1])
        
    def do_get_sorb(self):# state
        ans = self._query('READ:DEV:MB1.T1:TEMP:SIG:TEMP')
        return float(ans[:-1])
    
