# -*- coding: utf-8 -*-

import matplotlib.dates as md
import numpy as np
import time
import os
############# modifiy here ##############
timestr = '2019-04-11 00:00:00'
#########################################
fp_key = ['Date', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'Flow', 'MG0', 'MG1', 'MG2', 'MG3', 'MG4', 'MG5', 'PT on', 'W_in', 'W_out', 'He', 'Oil', 'P_low', 'P_high', 'PT current', 'State0', 'State1', 'State2']
t = md.datestr2num(timestr)
fns = os.listdir(os.getcwd())
for i in fns:
    if ".txt" in i or '.dat' in i:
        try:
            # print i
            data = np.loadtxt(i,delimiter='\t',converters={0:md.datestr2num})
            if len(np.shape(data))==2:
                if data[-1,0]>t:
                    ind = np.where(data[:,0]>t)[0][0]
                    # print ind
                    print md.num2date(data[ind,0])
                    for i1,i2 in zip(fp_key,data[ind,:]):
                        print i1,'\t',i2
                    break
        except:
            pass