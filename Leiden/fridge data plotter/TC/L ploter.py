# -*- coding: utf-8 -*-
# A script to plot Impedance Bridge/AVS/FP data of a Leidon DR
# How to use: put all the data files in the same folder as this script. Modify y coloum number and label. Then run this script. It will plot data from all files in one figure. You can zoom in/out/save ....
# plot with time axis: https://stackoverflow.com/questions/4090383/plotting-unix-timestamps-in-matplotlib
# plot with engineering formatter (n, u, m, k, ...): https://matplotlib.org/examples/api/engineering_formatter.html

import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt
import time
import os
from matplotlib.ticker import EngFormatter
############# modifiy here ##############
fp_key = ['Date', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'Flow', 'MG0', 'MG1', 'MG2', 'MG3', 'MG4', 'MG5', 'PT on', 'W_in', 'W_out', 'He', 'Oil', 'P_low', 'P_high', 'PT current', 'State0', 'State1', 'State2']
tc_key = ['Date1', 'Date2', 'R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'T0', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'I0', 'I1', 'I2', 'I3']
ycol=3;ylabel=tc_key[ycol]
ycol2=-1;ylabel2=tc_key[ycol2]
#########################################
plt.subplots_adjust(bottom=0.2)
plt.xticks(rotation=25)
ax=plt.gca()
xfmt = md.DateFormatter('%m-%d %H:%M')
yfmt = EngFormatter()
ax.xaxis.set_major_formatter(xfmt)
ax.yaxis.set_major_formatter(yfmt)
ax.set_xlabel('time')
ax.set_ylabel('r: %s, b: %s'%(ylabel,ylabel2) if ycol2>-1 else 'r: %s'%ylabel)
#ax.set_ylim(1000,1100)
#ax.set_xlim(md.datestr2num('2018-05-30 00:00:00'),md.datestr2num('2018-06-6 00:00:00'))
fns = os.listdir(os.getcwd())
for i in fns:
    if ".txt" in i or '.dat' in i:
        print i
        if ycol2>-1:
            t,y,y2 = np.loadtxt(i,delimiter='\t',converters={0:md.datestr2num},usecols=(0,ycol,ycol2),unpack=True)
            plt.plot(t,y,'r.',label=ylabel)
            plt.plot(t,y2,'b.',label=ylabel2)
        else:
            t,y = np.loadtxt(i,delimiter='\t',converters={0:md.datestr2num},usecols=(0,ycol),unpack=True)
            plt.plot(t,y,'r-',label=ylabel)
plt.show()