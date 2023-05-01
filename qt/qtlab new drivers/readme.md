# Description

This folder contains qtlab drivers. [Qtlab](https://github.com/heeres/qtlab) is a python based data-taking program.

# Simple example

The following example shows a qtlab driver for the Oxford PT system. The key concept is the parameter. In this driver we have parameters such as Address, Module name, ID, status, et al..

```python
# https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers

from instrument import Instrument
# from time import time, sleep
import visa
import types
import logging
# import math

class PTHe3_20230501(Instrument):

    def __init__(self, name, address, term_chars = '\n'):
        logging.debug(__name__ + ' : Initializing instrument')
        Instrument.__init__(self, name, tags=['physical'])
        
        self._address = address
        self._visainstrument = visa.instrument(self._address, term_chars = term_chars)
        self._visainstrument.clear()
        
        self.attribute_parameters = ['_address', '__module__']

        self.dict_parameters = { 
            'ID':
            {
                'get_cmd':'*IDN?',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'status': 
            {   
                'get_cmd':'READ:DEV:HelioxX:HEL:SIG:STAT',
                'set_cmd':'',
                'kw':{'type':types.StringType,'flags':Instrument.FLAG_GET}
            },
            'he3pot': 
            {   
                'get_cmd':'READ:DEV:HelioxX:HEL:SIG:TEMP',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GET}
            },
            'onekpot': 
            {   
                'get_cmd':'READ:DEV:DB6.T1:TEMP:SIG:TEMP',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GET}
            },
            'sorb': 
            {   
                'get_cmd':'READ:DEV:MB1.T1:TEMP:SIG:TEMP',
                'set_cmd':'',
                'kw':{'type':types.FloatType,'flags':Instrument.FLAG_GET}
            },
           
        }
        
        # Add parameters
        for i in self.attribute_parameters:
            para_name = i.strip('_').upper()
            func = lambda attr_name=i: getattr(self,attr_name) 
            setattr(self, 'do_get_%s'%para_name, func)
            self.add_parameter(para_name, flags=Instrument.FLAG_GET, type=types.StringType)

        for i in self.dict_parameters:
            cmd = self.dict_parameters[i]['get_cmd']
            if cmd:
                func = lambda cmd=cmd,flag=0: self._query(cmd,flag)
                setattr(self, 'do_get_%s'%i, func)
            
            cmd = self.dict_parameters[i]['set_cmd']
            if cmd:
                func = lambda x,cmd=cmd: self._execute(cmd%x)
                setattr(self, 'do_set_%s'%i, func)

            self.add_parameter(i, **self.dict_parameters[i]['kw'])

        self.get_all()
        
    def close_session(self):
        self._visainstrument.close() 

    def _execute(self, message):
        return self._visainstrument.ask(message)
        
    def _query(self, message, flag=0):
        '''
        flag, 0 (default): write command and read respond, 1: write only, 2: read only
        '''
        if  flag != 2:
            self._visainstrument.write(message)
        if flag != 1:
            ans = self._visainstrument.read()
            return self._parse(ans,message)
        return None
            
    def _parse(self, ans, message):
        if message == '*IDN?':
            return ans[4:]
        ans = ans.split(':')[-1]
        if message == 'READ:DEV:HelioxX:HEL:SIG:STAT':
            return ans
        else:
            return ans[:-1]       

    def get_all(self):
        for i in self.attribute_parameters:
            para_name = i.strip('_').upper()
            self.get(para_name)
        for i in self.dict_parameters:
            self.get(i)
```

To use the driver, one copies the driver file to folder `[qtlab folder]/instrument_plugins`, then either copies the command `heliox = qt.instruments.create('heliox','PTHe3_20230501',address='[ADDRESS]')` into file `[qtlab folder]/init/80_create_instruments.py` or run it directly in qtlab command line window. If all goes well, the qtlab GUI would show something like the picture below,

![image](https://user-images.githubusercontent.com/22870592/235501149-0ebc65db-0980-4f04-a8b1-bbc57e4ce6ca.png)

Most parameters of a driver are defined in a dictionary `dict_parameters`. Each parameter has three sub-parameters, `get_cmd`, `set_cmd`, and `kw`. `get_cmd` and `set_cmd` are used to create functions `do_get_[parameter name]` and `do_set_[parameter name]`, respectively. `do_get_[parameter name]` and `do_set_[parameter name]` are not exposed to qtlab users. Instead, qtlab users use higher lever functions `get_[parameter name]` (`set_[parameter name]`) or `get([parameter name])` (`set([parameter name])`) to get or set these paramters, respectively. The corresponding functions are not created or can be created manually (by `def do_get_[parameter name]...`) if `get_cmd` or `set_cmd` are empty. `kw` is used in `self.add_parameter([parameter name], **self.dict_parameters[[parameter name]]['kw'])`, to ask qtlab for creating parameters.

The `flag` parameter in function `_query(self, message, flag=0)` helps the data-taking precess to be more efficient, see [Data taking program: make it non-atomic](https://cover-me.github.io/2021/10/17/data-taking-program-make-it-non-atomic.html). It is an upgrade to the following `_query` function,

```python
def _query(self, message):
    ans = self._visainstrument.ask(message)
    return self._parse(ans,message)
```

# More examples

- Multiple readings. Put `'type':types.ListType` in `kw`.

- Optional keywords in `kw`

Reference: https://github.com/heeres/qtlab/blob/master/source/instrument.py#L237

```
optional keywords:
    type: types.FloatType, types.StringType, etc.
    flags: bitwise or of Instrument.FLAG_ constants.
        If not set, FLAG_GETSET is default
    channels: tuple. Automagically create channels, e.g.
        (1, 4) will make channels 1, 2, 3, 4.
    minval, maxval: values for bound checking
    units (string): units for this parameter
    maxstep (float): maximum step size when changing parameter
    stepdelay (float): delay when setting steps (in milliseconds)
    tags (array): tags for this parameter
    doc (string): documentation string to add to get/set functions
    format_map (dict): map describing allowed options and the
        formatted (mostly GUI) representation
    option_list (array/tuple): allowed options
    persist (bool): if true load/save values in config file
    probe_interval (int): interval in ms between automatic gets
    listen_to (list of (ins, param) tuples): list of parameters
        to watch. If any of them changes, execute a get for this
        parameter. Useful for a parameter that depends on one
        (or more) other parameters.
```
 
- Convert the value of a parameter from a number to a description string. Use 'format_map',

```python
'output_status': 
{   
    'get_cmd':':OUTP?',
    'set_cmd':':OUTP %s',
    'kw':{'type':types.IntType,'flags':Instrument.FLAG_GETSET,'format_map':{0:"OFF",1:"ON"}}
},
```

# Suggestions

- Reduce IO operations. For example, for lockins, add parameters `XY` and `RT` besides `X`, `Y`, `R`, and `Theta`.

- Make parameter-setting functions (`do_set_[parameter name]`) which may take a long time interruptible by a shortcut, such as ctrl+e (e for exit).

```python
def _check_last_pressed_key(self):
    last_key = ''
    while msvcrt.kbhit():
       last_key = msvcrt.getch()
    if last_key == '\x05':#ctrl+e(xit)
        raise KeyboardInterrupt
        # or raise UserWarning('exit')
```
