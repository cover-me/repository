![qtlab_command_line](https://user-images.githubusercontent.com/22870592/235606148-5f30f130-b4f6-4802-8228-02f1a930a5f0.gif)

![qtlab_qtplot](https://user-images.githubusercontent.com/22870592/235606186-f9a945ef-ecbe-4225-a2a3-9f1470c335ca.gif)

![qtlab_gui](https://user-images.githubusercontent.com/22870592/235606212-5d37d212-45d6-4e17-a551-1975ef917481.gif)


# Description

This folder contains the enhancing script, Qscan.py, for [qtlab](https://github.com/heeres/qtlab). Qscan makes it easier and more efficient to do 1d/2d/3d scans, vector scans (scan multiple channels simultaneously), real-time visualization/operating data (with my forked version of qtplot), and automatically logging (in a WORD file, tips: switch to the web layout so there are no margins and page breaks, turn on the navigation pane). 3d scan is rarely used as it is time-consuming and can be replaced by a few 2d scans.


# A simple example

filename: poscan.py

```python
execfile('Qscan.230520.py')
this_file_path = sys._getframe().f_code.co_filename

'''File path'''
# Data in path\cooldown_name\data, logs and summaries in path\cooldown_name\
datapath=r'[data_folder]\[cooldown_info-fridge_info-sample_info]\data'
filename='dat_[fridge_info]_[cooldown_info]'

channels_to_read = [# (instrument,parameter,label or list of labels)
                    ('smu1','val','I_leak (A)'), 
                    # ('smu2','val','R (ohm)'), 
                    ('lockin1','XY',['Vac_x (V)', 'Vac_y (V)']),
                    ('ppms','temp','T (K)'),
                    ]

channels_to_set = {# name: [unit,instrument,parameter] or [unit, function]
                    'vg':['V','smu1','source_level'],
                    'T':['K','ppms','temp'],
                    'B':['T','ppms','field'],
                     # 'magnet_theta_deg':['Deg',magnet_theta_deg],
                  }

g = get_set()
e = easy_scan()

'''Other settings'''
# Lockin:(0,10*tau,1.5tau-10tau) DC:(0,1,0.1)
delay0,delay1,delay2 = (0,1,0.05)

'''measure'''
# channels, start, end, number of steps ( = point number -1)
e.scan(['vg'],[0],[3],100)# '[' and ']' can be dropped if not vector scan (a combination of channels)
e.set('vg',0)

# e.scan(['Vg1','Vg2'],[0]*2,[100]*2,200)# scan a combination of channels
# e.scan(['Vg1','Vg2'],[0]*2,[100]*2,200, 'B',0,1,50)# higher-dimensional scan

'''more scans'''
# Excute file "poscan_more.py" if exist, then delete it.
e.more_scan('poscan_more.py')
```

- Files generated

The final file name would be `filename_[index]`, where `[index]` starts from 1 and is unique as long as `[data_folder]` does not change.

DAT, SET, PY files would be generated in `datapath`, which are the data file, the instrument snapshot, a copy of the scan script file, respectively. Qscan file will also be copied if not copied yet.

- value labels

Getting paramters: `[instrument_name] (label)` or `[instrument_name]_[parameter_name]_[component_name] (component_label)` (I would like to make it `[instrument_name]_[component_name] (component_label)`...)

Setting parameters: `channel_name_(label)`

# Special scans

A linear scan is a scan whose set value changes linearly. Sometimes one needs to perform a non-linear scan, for example, a vector combination of magnetic fields Bx and By with fixed Btot = sqrt(Bx^2+By^2).

```python
# def vect_sum_valid(bx,by):  
# def get_fields():

# Return: a list of [channel,parameter,setting_value]
def magnet_theta_deg(val):
    B_TOT = 1

    t_rad = val/180*np.pi
    bx = B_TOT * np.cos(t_rad)
    by = B_TOT * np.sin(t_rad)
        
    bx0, by0 = get_fields()
    if vect_sum_valid(bx,by) and vect_sum_valid(bx0,by0):
      if vect_sum_valid(bx,by0):
        return [['magnetX','field',bx],['magnetY','field',by]]
      else:# vect_sum_valid(bx0,by)
        return [['magnetY','field',by],['magnetX','field',bx]]
    else:
      return None

channels_to_set = {'magnet_theta_deg':['D',magnet_theta_deg]}
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

Todo: check if this is still valid in the newest Qscan, and explain it

# Shifted field or dac (to do: need update)

```python
def by_shift(by):# shift By with a Bz-dependent value
    # Get Bz
    # Instead of getting Bz from the instrument, we get it from the qtlab, which is much faster. 
    instr = qt.instruments.get('magnet')
    para = instr.get_parameters()['field']
    b = para['value']
    if b is None:
        b = instr.get(para_name)
        
    by = by - b/36.89
    return by
    
''' if you need to redefine the set function of e.scan()'''
# add "By_shift" channel
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
# We also want to log the original By
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

# qt.instruments.get('magnetY')._ins.MARGIN=1e-3
```

# Notes for qtlab measurement

1. Under the "User Folder", create a new "Data Folder" for each cooldown.  
   - The "User Folder" is similar to X:\UserData\[UserName], where X can be drive C or other drives. For convenience, it is recommended to use the last drive of the system.
   - The suggested name for the "Data Folder": [Cooldown info] [Sample info] [User info], e.g., 20240707-105XL 20221222-InAs2DEGJJ15 UserName.

3. Under the "Data Folder", create:
   - A folder named "data" to store data files. Copy the address of the this subfolder, as it will be used in the scan script.
   - A pptx document with a prefix the same as the "Data Folder" name, and a suffix if multiple ppt files are needed. This is used for discussion during the experiment.
   - A docx document with a prefix the same as the "Data Folder" name, and a suffix if multiple doc files are needed. This is used for semi-automatic experiment logging, and analysis/discussion when the ppt cannot provide sufficient details. Open the docx file, select the "webview" in the bottom right corner, and the measurement code will automatically generate logs to this document.

4. Open qtplot. The shortcut is usually on the desktop or in the desktop qtlab folder. The EXE is in the desktop qtlab/qt_plot folder.

5. Edit and save 80_create_instruments.py to specify which instruments will be loaded. The file location is typically in the qtlab\init\ folder in the desktop qtlab folder. Comment instruments which are not needed, and uncomment instruments that are needed. You can also comment all instruments now and manually add/remove instruments later after running qtlab.

6. Open qtlab. This will bring up a command line prompt and a GUI. The prompt is used to enter commands, and the GUI is used to view the loaded instrument parameters.

7. Measurement:
   - Load more instruments: You can add them line by line in the prompt, following the examples in 80_create_instruments.py. It's ok to add more instruments than necessary as long as they are connected to the computer.
   - Modify instrument parameters: it is recommended to do this from the computer, using commands like lockin1.set_XXX(value). This ensures that the instrument settings in the software and the actual instrument settings are the same. If you modify the settings from an instrument directly, it is recommended to update the corresponding parameters in the software as well using commands, e.g., lockin1.get_all().
   - Edit and save the scan script, which typically locates in the qtlab folder, like XXXscan.py. If you don't have your own measurment script, you can copy and rename someone else's. The measurement, no matter one-dimensional, two-dimensional, or even three-dimensional (not very useful), is done by e.scan(...).
   - Run the scan script. In the command line, enter "run [path_to_scan_file]". You can use the up and down keys to view the history commands, and the tab key to autocomplete the commands. qtplot will visualize data in real-time. The word document will be automatically updated with measurement records, and you can manually insert figures from qtplot to the doc document (click "copy" and then "ctrl+v" to paste or click "to Word", simmilar to ppt files).
  

# Further reading

Demos are available [here](https://cover-me.github.io/2019/03/31/qtplot-demo.html), may be a little out of date.

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
- 23.05.02 update get_rate
