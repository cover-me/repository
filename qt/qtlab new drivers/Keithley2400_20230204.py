# https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers

from instrument import Instrument
# from time import time, sleep
import visa
import types
import logging
# import math

class Keithley2400_20230204(Instrument):

    def __init__(self, name, address):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])
        self._address = address
        self._visainstrument = visa.instrument(self._address)
        self._visainstrument.clear()
        
        # use upper-case names so it shows at the top on the GUI
        # It is dangerouse to use FLAG_GET_AFTER_SET flag for parameters you want to update units
        # For example, if you get a value and update the units, it will triger another getting action and ends up with a death loop
        self.add_parameter('ID', flags=Instrument.FLAG_GET, type=types.StringType)
        self.add_parameter('Address', flags=Instrument.FLAG_GET, type=types.StringType)
        self.add_parameter('output_status', type=types.IntType, flags=Instrument.FLAG_GETSET)
        self.add_parameter('source_type', type=types.StringType, flags=Instrument.FLAG_GETSET)
        self.add_parameter('source_range', type=types.FloatType, 
                            flags=Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET)
        self.add_parameter('source_i_level', type=types.FloatType, flags=Instrument.FLAG_GETSET, 
                            maxstep=1e-9, stepdelay=30, units='A')
        self.add_parameter('source_v_level', type=types.FloatType, flags=Instrument.FLAG_GETSET, 
                            maxstep=1e-3, stepdelay=30, units='V')
        self.add_parameter('compliance', type=types.FloatType, 
                            flags=Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET)
        self.add_parameter('nplc', type=types.IntType, flags=Instrument.FLAG_GETSET)
        self.add_parameter('sense_type', type=types.StringType, flags=Instrument.FLAG_GETSET)
        self.add_parameter('sense_range', type=types.FloatType, 
                            flags=Instrument.FLAG_GETSET|Instrument.FLAG_GET_AFTER_SET)
        self.add_parameter('vals', flags=Instrument.FLAG_GET, type=types.ListType)

        self.get_all()

    def _execute(self, message):
        self._visainstrument.write('%s' % (message))
        
    def _query(self, message):
        return self._visainstrument.ask(message)

    def get_all(self):
        self.get_ID()
        self.get_Address()
        self.get_output_status()
        self.get_source_type()
        self.get_source_range()
        self.get_source_i_level()
        self.get_source_v_level()
        self.get_compliance()
        self.get_nplc()
        self.get_sense_type()
        self.get_sense_range()

    # getting and setting functions
    def do_get_ID(self):
        return self._query('*IDN?')

    def do_get_Address(self):
        return self._address
   
    ## source
    def do_get_output_status(self):# output_status
        return int(self._query(':OUTP?'))

    def do_set_output_status(self,i):
        if i in [0,1]:
            return self._execute(':OUTP %s'%i)
        else:
            print 'Error parameter!'
            
    def do_get_source_type(self):# source_type
        return self._query('SOUR:FUNC?')
        
    def do_set_source_type(self,s):
        s = s.upper()
        plist = ['VOLT','CURR']
        if s in plist:
            self._execute('SOUR:FUNC %s'%s)
        else:
            print 'Unknown source type (should be in %s)!'%plist
                    
    def do_get_source_range(self):# source_range
        stype = self.get_source_type()
        d = {'VOLT':'V','CURR':'A'}
        if stype in d:
            # self.set_parameter_options('source_range',units=d[stype])# death loop
            return float(self._query(':SOUR:%s:RANG?'%stype))
        else:
            print 'Unknown source type!'

    def do_set_source_range(self, x):
        stype = self.get_source_type()
        d = {'VOLT':'VOLT','CURR':'CURR'}
        if stype in d:
            self._execute(':SOUR:%s:RANG %s'%(d[stype],x))
        else:
            print 'Unknown source type!'
        
    def do_get_source_i_level(self):# source_i_level
        return float(self._query('SOUR:CURR?'))
        
    def do_set_source_i_level(self,lvl):
        return self._execute('SOUR:CURR %s'%lvl)
        
    def do_get_source_v_level(self):# source_v_level
        return float(self._query('SOUR:VOLT?'))
        
    def do_set_source_v_level(self,lvl):
        return self._execute('SOUR:VOLT %s'%lvl)
        
    def do_get_compliance(self):# compliance
        stype = self.get_source_type()
        d = {'VOLT':'A','CURR':'V'}
        d2 = {'VOLT':'CURR','CURR':'VOLT'}
        if stype in d:
            # self.set_parameter_options('compliance',units=d[stype])# death loop
            return float(self._query(':SENS:%s:PROT?'%d2[stype]))
        else:
            print 'Unknown source type!'
            
    def do_set_compliance(self, x):
        stype = self.get_source_type()
        d = {'VOLT':'CURR','CURR':'VOLT'}
        if stype in d:
            self._execute(':SENS:%s:PROT %s'%(d[stype],x))
        else:
            print 'Unknown source type!'            

    ## sense    
    def do_get_nplc(self):# nplc
        return int(float(self._query('NPLC?')))
    
    def do_set_nplc(self,n):
        return self._execute('NPLC %s'%n)
    
    def do_get_sense_type(self):# sense_type
        return self._query('SENS:FUNC?')
        
    def do_set_sense_type(self,s):
        s = s.upper()
        plist = ['"VOLT"','"CURR"','"VOLT","CURR"']
        if s in plist:
            self._execute('SENS:FUNC %s'%s)
        else:
            print 'Unknown source type (should be in %s)!'%plist

    def do_get_sense_range(self):# sense_range
        # print "Get sense range: for V source, get I-measure range, and vice versa"
        stype = self.get_source_type()
        d = {'VOLT':'A','CURR':'V'}
        d2 = {'VOLT':'CURR','CURR':'VOLT'}       
        if stype in d:
            # self.set_parameter_options('sense_range',units=d[stype])# death loop
            return float(self._query(':SENS:%s:RANG?'%d2[stype]))
        else:
            print 'Unknown source type!' 
            
    def do_set_sense_range(self, x):
        # print "Set sense range: for V source, set I-measure range, and vice versa"
        stype = self.get_source_type()# sense type is related to source type
        d = {'VOLT':'CURR','CURR':'VOLT'}
        if stype in d:
            self._execute(':SENS:%s:RANG %s'%(d[stype],x))
        else:
            print 'Unknown source type!'
        


    def do_get_vals(self):
        ans = self._query('read?').split(',')
        volt, curr, res, ts, status = [float(i) for i in ans]
        return [volt, curr]





