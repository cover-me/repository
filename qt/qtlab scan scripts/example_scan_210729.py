execfile('Qscan.210729.draft23.py')
this_file_path = sys._getframe().f_code.co_filename

'''File path'''
datapath=r'C:\qtlab\data\user1_pc1'+'\\%s'%strftime('%Y-%m')
filename='datC%s'%strftime('%y%m')#C: center, S: side

'''Measurement setup'''
# Manually update the following details as a note.
device1 = {
    'chip': '20210101 InAs 10',
    'device': '1.1',
    'source': {'p4-p2': (1,2),# pins
        'in': (2, '0.5 kHz', 'no lockin'),# slot position, filter, ISO in
        'module': ('S4m','10 uA/V','V2=0'),# !!! change elsewhere: labels in e.scan
        },
    'measure': {'p4-p2': (3,4),# pins
        'out': (2, '0.1 kHz', '0.1 kHz + keithley1, no lockin'),# slot position, filter, ISO out
        'module': ('M2b', '1 kV/V', '1 kV/V'),# !!! change elsewhere: labels channels_to_read and lockin_list. First is dc amp, second is ac amp
        },
    'gates': ('5, dac11, 1 V/V'),# !!! change elsewhere: labels in e.scan. 
    }

'''Print source-drain info for double check'''
# This does not work very well...
# label_src, label_meas_dc, label_meas_ac = get_SD_info(device1)

'''Other settings'''
delay0,delay1,delay2 = (0,0.5,0.035)# Delays after setting Z (and Y0), Y (and X0), X. Lockin:(0,10*tau,1.5tau-10tau) DC:(0,1,0.1)
channels_to_read = [('keithley1','readnextval','e-3V')]#, ('lockin1', 'XY', label_meas_ac)# ('fridge', 'MC', 'K')

'''initialize instruments'''
qt.instruments.get('fridge').get_all()
for i in []:# lockins
    qt.instruments.get(i)._ins._visainstrument.clear()
    qt.instruments.get(i).set_amplitude(4e-3)# 4e-3. for SR830, 0 for other lockins.
    qt.instruments.get(i).set_sensitivity(26)# 26. 10 for 5 uV, 15 for 200 uV, 19 for 5 mV, 20 for 10 mV, 21: 20 mV, 22: 50 mV, 23: 100 mV, 24: 200 mV, 25: 500 mV, 26: 1 V, usually 20
    qt.instruments.get(i).set_dynamic(1)# 1. 0 (high),1 (med),2 (low)
    qt.instruments.get(i).set_tau(8)# 8. [6: 10 ms, 7: 30 ms, 8: 100 ms, 9: 300 ms]
    qt.instruments.get(i).set_slope(3)# 3. 0,1 (12 dB),2,3


''' if you need to redefine the set function of e.scan()'''
# add microwave source, dac field source
def field_to_dac_val(val):
    return 0
    
def get_setpoint2(self,chan,val):
    if self.is_dac_name(chan):
        return [['ivvi',chan,val],]
    elif chan == 'magnet' or chan == 'magnetX' or chan == 'magnetY':
        return [[chan,'field',val],]
    elif chan == 'dBy':
        return [['ivvi','dac1',field_to_dac_val(val)],]
    elif chan == 'mw_power':
        return [['mw','power',val],]
    elif chan == 'mw_freq':
        return [['mw','frequency',val],]
    return None
get_set.get_setpoint = get_setpoint2

g = get_set()
e = easy_scan()



'''measure'''
# labels, channels, start, end, number of steps ( = point number -1)

'''1d'''
# e.scan(['I2(e-2uA)'],['dac2'],[-300],[300],100)
# e.set('dac2',0)
# e.scan(['Vg1(mV)'],['dac11'],[0],[100],200,bwd=True)
# e.scan(['Vg1_Vg2(mV)','Vg2(mV)'],['dac11','dac12'],[0]*2,[100]*2,200)

'''2d'''
# e.scan(['I2(e-2uA)'],['dac2'],[-100],[100],150,['Vg2(mV)'],['dac12'],[-50],[50],50)
# e.scan(['I2(e-2uA)'],['dac2'],[0],[50],50,['By(T)'],['By'],[-1],[1],50)

'''useful'''
# for i in [0.01,-0.005,0.005,-0.002,0.002,-0.001,0.001,-0.0005,0.0005,-0.0002,0.0001,0]:
    # e.set('magnet',i)
# e.set('ivvi_rate',2)
# e.set('dac2_rate',5)

'''more scans'''
# Excute file "poscan_more.py" if exist, then delete it.
e.more_scan('poscan_more.py')
