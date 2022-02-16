# How does it work?

With qtlab, we can get readings from and set parameters in instruments.

With qtplot, we can slice, visualize, and operate data.

With MS Word, we are able to create measurement logs with text, figures, the web layout (without margins and page breaks), and a navigation panel.

Qscan.py makes them work together, providing two major functions: `easy_scan.scan()` and `easy_scan.set()`, which are usually called in a form like `e.scan(['I2(e-2uA)'],['dac2'],[-100],[100],150,['Vg1(mV)','Vg2(mV)'],['dac11','dac12'],[0]*2,[100]*2,200)` (a 2D linear scan, note that two channels, 'dac11' and 'dac12', are able scanned together) and `e.set('magnet',0)`. Messages are sent to qtplot for visualizing and MS Word for logging.

Demos are available [here](https://cover-me.github.io/2019/03/31/qtplot-demo.html), though they may be a little out of date.

# Minimal working example

```python
# minimal working example.py

execfile('Qscan.211215.py')
this_file_path = sys._getframe().f_code.co_filename

'''File path'''
datapath=r'C:\qtlab\data\user1_pc1'+'\\%s'%strftime('%Y-%m')
filename='datPC1%s'%strftime('%y%m')

'''Other settings'''
delay0,delay1,delay2 = (0,0.5,0.035)# Delays after setting Z (and Y0), Y (and X0), X. Lockin:(0,10*tau,1.5tau-10tau) DC:(0,1,0.1)
channels_to_read = [('keithley1','readnextval','e-3V'), ('lockin1', 'XY', 'e-3V,ac10nA')]# ('fridge', 'MC', 'K')

g = get_set()
e = easy_scan()

'''measure'''
# labels, channels, start, end, number of steps ( = point number -1)

# e.scan(['I2(e-2uA)'],['dac2'],[-300],[300],100)
# e.set('dac2',0)
e.scan(['Vg1_Vg2(mV)','Vg2(mV)'],['dac11','dac12'],[0]*2,[100]*2,200)

```

# Special scans

A linear scan is a scan whose set value changes linearly. Sometimes one needs to perform a non-linear scan, for example, a vector combination of magnetic fields Bx and By with fixed Btot = sqrt(Bx^2+By^2). Sometimes one needs to sweep a channel which is not defined in Qscan.py. We can of cause write a driver for vector magnets, or more simply, redefine the set function for e.scan() in the scan script (see the file "example_scan_210729.py").

```python
B_TOT = 1

def get_setpoint2(self,chan,val):

    if self.is_dac_name(chan):
        return [['ivvi',chan,val],]
        
    elif chan == 'magnet' or chan == 'magnetX' or chan == 'magnetY':
        return [[chan,'field',val],]
        
    elif chan == 'magnet_theta_deg':
        t_rad = val/180*np.pi
        bx = B_TOT * np.cos(t_rad)
        by = B_TOT * np.sin(t_rad)
        
        bx0, by0 = get_fields()
        if vect_sum_valid(bx,by) and vect_sum_valid(bx0,by0):
          if vect_sum_valid(bx,by0):
            return [[magnetX,'field',bx],[magnetY,'field',by]]
          else:# vect_sum_valid(bx0,by)
            return [[magnetY,'field',by],[magnetX,'field',bx]]
        else:
          return None

    return None
get_set.get_setpoint = get_setpoint2
```

# Data processing during scan

```python
''' if you need to add processed data '''
def get_isw(arg_dict,val):
    '''
    Get the switching current
    All values are converted to SI unit, i.e., V, A, ...
    '''
    dc_offset = -6e-6# When bias is zero, there is a dc offset in voltage readings
    threshold_low = 3e-6 + dc_offset
    threshold_high = 5e-6 + dc_offset
    threshold_step = 1.000001
    x0, x1, step = 0., 500., 10.
    delay = 0.03
    
    while 1:
        is_first_value = True
        is_isw_found = False
        for i in np.arange(x0, x1+step, step):
            ivvi.set_dac2(i)
            qt.msleep(delay)
            v = qt.instruments.get('keithley1').get_readnextval()*1e-3
            if is_first_value:
                if v > threshold_low:# x0 is too large
                    print 'x0 error'
                    ivvi.set_dac2(0)
                    return None
                is_first_value = False
            if v > threshold_high:
                is_isw_found = True
                if step < threshold_step:# Isw found
                    ivvi.set_dac2(0)
                    return i*1e-8
                else:
                    x0, x1 = i-step*3., i+step*3.
                    step = step/10.#or 10.
                    break

        if not is_isw_found:# Isw not found in this round            
            print 'Isw not found'
            ivvi.set_dac2(0)
            return None
g = get_set()
g._prcss_labels.append('Isw(A)')
g._prcss_funs.append({'function':get_isw,'arg':None})
e = easy_scan()
```
# Shifted field or dac

```python
def by_shift(by):
    instr = qt.instruments.get('magnet')
    para = instr.get_parameters()['field']
    b = para['value']
    if b is None:
        b = instr.get(para_name)
        
    by = by - b/36.89
    return by
    
''' if you need to redefine the set function of e.scan()'''
# add microwave source, dac field source
def get_setpoint2(self,chan,val):
    if self.is_dac_name(chan):
        return [['ivvi',chan,val],]
    elif chan == 'magnet' or chan == 'magnetX' or chan == 'magnetY':
        return [[chan,'field',val],]
    elif chan == 'dBy':
        return [['ivvi','dac1',field_to_dac_val(val)],]
    elif chan == 'By_shift':
        return [['magnetY','field',by_shift(val)]]
    elif chan == 'mw_power':
        return [['mw','power',val],]
    elif chan == 'mw_freq':
        return [['mw','frequency',val],]
    return None
get_set.get_setpoint = get_setpoint2

g = get_set()
''' if you need to add processed data '''
def get_by(arg_dict,val):
    instr = qt.instruments.get('magnetY')
    para = instr.get_parameters()['field']
    by = para['value']
    if by is None:
        by = instr.get(para_name)
    return by

g._prcss_labels.append('By(T)')
g._prcss_funs.append({'function':get_by,'arg':None})

e = easy_scan()

qt.instruments.get('magnetY')._ins.MARGIN=1e-3
```


# Main changes:
- 18.06.17 add scan delay/rates/elapsed/filename to .doc notes
- 18.07.22 add _scan1d. auto qtplot now works with 1d bwd
- 19.08.06 19.08.04 "Ding!" when a scan has finished. Load more scan without stopping current scan.
- 19.09.06 shortcuts ctrl+e and ctrl+n
- 19.09.16 shifted scan, 3D scan, meander scan
- 21.07.30 When taking data, write to all insturmens and then read, instead of write-read one by one.
- 21.08.23 change keithley reading from lastval to nextval
- 21.10.12 Remove meander, shift, xswp_by_mchn, Store all channels when multiple channels are scanned
- 21.10.17 When setting x channels, wait once instead of x times. Add functions for data labels.
- 21.12.08 Remove "ctrl+n", improve "ctrl+e"
- 21.12.15 clean up
