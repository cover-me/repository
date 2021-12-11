# How does it work?

With qtlab, we can get readings from and set parameters in instruments.

With qtplot, we can slice, visualize, and operate data.

With MS Word, we are able to create measurement logs with text, figures, the web layout (without margins and page breaks), and a navigation panel.

Qscan.py makes them work together, providing two major functions: `easy_scan.scan()` and `easy_scan.set()`, which are usually called in a form like `e.scan(['I2(e-2uA)'],['dac2'],[-100],[100],150,['Vg1(mV)','Vg2(mV)'],['dac11','dac12'],[0]*2,[100]*2,200)` (a 2D linear scan, note that two channels, 'dac11' and 'dac12', are able scanned together) and `e.set('magnet',0)`. Messages are sent to qtplot for visualizing and MS Word for logging.

Demos are available [here](https://cover-me.github.io/2019/03/31/qtplot-demo.html), though they may be a little out of date.


# Non-linear scan?

A linear scan is a scan whose set values changes linearly. Sometimes one needs to perform a non-linear scan, for example, a vector combination of magnetic fields Bx and By with fixed Btot = sqrt(Bx^2+By^2). This can be done by writing a driver for vector magnets, or more simply, redefine the set function for e.scan() in the scan script (see the file "example_scan_210729.py"). For example,

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
