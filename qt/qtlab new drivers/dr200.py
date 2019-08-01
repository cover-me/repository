# 07/19/2019 Po
''' Read temperatures from DR200'''
from instrument import Instrument
import visa
import types
import logging
from time import sleep,time

class dr200(Instrument):
    def __init__(self, name, address):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])
        self._address = address
        self._visainstrument = visa.instrument(self._address,term_chars=">")
        self.last_ask_time = time()
        self.last_cmd = ''
        self.cache = ''

        #Add parameters
        self.add_parameter('4K', type=types.FloatType,
            flags=Instrument.FLAG_GET)
        self.add_parameter('still', type=types.FloatType,
            flags=Instrument.FLAG_GET)
        self.add_parameter('cold', type=types.FloatType,
            flags=Instrument.FLAG_GET)
        self.add_parameter('MC', type=types.FloatType,
            flags=Instrument.FLAG_GET)
        self.add_parameter('MCcnx', type=types.FloatType,
            flags=Instrument.FLAG_GET)
        self.add_parameter('R_MC', type=types.FloatType,
            flags=Instrument.FLAG_GET)

        # Add functions
        self.add_function('get_all')
        self.get_all()

    def get_all(self):
        self.get_4K()
        self.get_still()
        self.get_cold()
        self.get_MC()
        self.get_R_MC()
        self.get_MCcnx()
        
    # Functions
    def _ask(self, message):
        if self.last_cmd != message or time()-self.last_ask_time>10:
            self._visainstrument.write(message)
            line = ''
            self.cache = ''
            while not line.endswith('<end'):
                line = self._visainstrument.read()
                self.cache += line + '>'
            self.last_cmd = message
            self.last_ask_time = time()

            
    def temperatures(self):
        self._ask('temperatures\n')
        result = self.cache
        names = []
        temps = []
        rs = []
        for i in result.split('\n'):
            if i.startswith('channel'):
                j = i.split(';')
                if len(j) == 9:
                    names.append(j[1][7:])
                    temps.append(float(j[7][14:]))
                    rs.append(float(j[6][13:]))
        return names, temps, rs

    def do_get_4K(self):
        n,t,r = self.temperatures()
        return t[1]
        
    def do_get_still(self):
        n,t,r = self.temperatures()
        return t[2]
        
    def do_get_cold(self):
        n,t,r = self.temperatures()
        return t[3]
        
    def do_get_MCcnx(self):
        n,t,r = self.temperatures()
        return t[4]

    def do_get_MC(self):
        n,t,r = self.temperatures()
        return t[5]
        
    def do_get_R_MC(self):
        n,t,r = self.temperatures()
        return r[5]