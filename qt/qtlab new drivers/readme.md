Suggestions on new drivers:

1. Make get functions non-atomic by adding the parameter 'flag':

```python
def _do_get_XY(self,flag=0):
    '''
    Read XY from SR830 lockin
    flag, 0 (default): write command and read respond, 1: write only, 2: read only
    '''
    if  flag != 2:
        self._visainstrument.write('SNAP?1,2')
    if flag != 1:
        ans = self._visainstrument.read()
        return [float(i) for i in ans.split(',')]
    return None
```

2. Reduce IO operations. For example, provide the get_XY() function instead of only provide get_X() and get_Y().

3. Make set functions which may take a long time interruptible by a shortcut, such as ctrl+e (e for exit).

```python
def _check_last_pressed_key(self):
    last_key = ''
    while msvcrt.kbhit():
       last_key = msvcrt.getch()
    if last_key == '\x05':#ctrl+e(xit)
        raise KeyboardInterrupt
```
