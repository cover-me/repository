# How does it work?

With qtlab, we can get readings from and set parameters in instruments.

With qtplot, we can slice, visualize, and operate data.

With MS Word, we are able to create measurement logs with text, figures, the web layout (without margins and page breaks), and a navigation panel.

Qscan.py makes them work together, providing two major functions: `easy_scan.scan()` and `easy_scan.set()`, which are usually called in a form like `e.scan(['I2(e-2uA)'],['dac2'],[-100],[100],150,['Vg2(mV)'],['dac12'],[-50],[50],50)` (a 2D linear scan) and `e.set('magnet',0)`. Messages are sent to qtplot for visualizing and MS Word for logging.

Demos are available [here](https://cover-me.github.io/2019/03/31/qtplot-demo.html), though they may be a little out of date.


