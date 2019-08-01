# -*- coding: utf-8 -*-
from collections import OrderedDict
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 9})
import numpy as np
import os
import time

def get_meta(fpath):
    f = open(fpath)
    scan = {}
    for i in range(3):
        points = int(f.readline())
        x0 = float(f.readline())
        x1 = float(f.readline())
        ch = f.readline().split('_')[0]
        if points > 1:
            if ch in scan:
                print 'This is a wrong scan!!! %s'%fpath
                f.close()
                os.sys.exit()
            else:
                if i==1:
                    scan[ch]=[points,x1,x0]#a bug of .meta.txt file. The order for y scan is resersed!
                else:
                    scan[ch]=[points,x0,x1]
                    
    f.close()
    return scan

def get_set(fpath):
    f = open(fpath)
    lines = f.readlines()
    f.close()
    setting = OrderedDict()
    for i in Channel_Names:
        for j in lines:
            if j.startswith('\t'+i):
                ch, x = j[1:].split(': ', 1)

                setting[ch] = float(x)



                break
    ts = time.strptime(lines[1].split(': ', 1)[1].strip())
    return setting, ts

def plot_setting(st_old,st,scan,fpath='',t_elapse=0):#st_old or st: {channel1:value1,channel2:value2,...}, scan: {channel:[points,x0,x1]}
    y0 = -1000
    y1 = 1000
    x = np.arange(len(st))#x values for the plot
    
    plt.figure(figsize=(5,2.5))
    plt.subplots_adjust(left=0.15, bottom=0.3, right=0.99, top=0.9)
    
    ax = plt.gca()
    ax.invert_yaxis()

    png_title = fpath.split('\\')[-1][:-4]
    png_title += '' if t_elapse==0 else ', %.1f min'%t_elapse
    plt.title(png_title,size=9)
    
    if st_old.keys() == st.keys():
        plt.bar(x,np.array(st_old.values())-y0,width=1,bottom=y0,color='grey',alpha=0.2)
        k = 0
        for i in st:
            if st[i]>st_old[i]:
                plt.bar(k,st[i]-st_old[i],width=1,bottom=st_old[i],color='grey')
            elif st[i]<st_old[i]:
                plt.bar(k,st_old[i]-st[i],width=1,bottom=st[i],color='w')
            k += 1
    else:
        plt.bar(x,np.array(st.values())-y0,width=1,bottom=y0,color='grey',alpha=0.5)

    plt.xticks(x+0.5,st.keys(),rotation=90)
    plt.vlines(x,y0,y1,linestyles='dashed')

    
    
    k = 0
    for i in st:
        if i in scan:
            clr = 'b' if scan[i][2]<scan[i][1] else 'r'
            plt.bar(k+0.45,scan[i][2]-scan[i][1],width=0.1,bottom=scan[i][1],color=clr)
            plt.gca().get_xticklabels()[k].set_color(clr)
        k = k + 1
      
    if fpath:
        plt.savefig(fpath)
    else:
        plt.show()
    plt.close()
    # os.sys.exit()
    
def get_other_change(st_old, st, scan):
    change = {}
    for i in st:
        if i not in st_old:
            change[i]=['_','_',st[i]]
        elif i in scan:
            if st_old[i] != scan[i][1]:
                change[i]=['_',st_old[i],scan[i][1]]
        elif st_old[i] != st[i]:
            change[i]=['_',st_old[i],st[i]]
    return change










########### modify here ####################
d_folder = r''# where are your .set and .meta.txt files
n = 1# plot parameters with & after data_n (the nth data)
#Channel_Names = ['dac%d'%i for i in ([1,15,16]+range(2,15))]# [dac1,dac15,dac16,dac2,dac3,...,dac14]
Channel_Names = ['dac%d'%i for i in [1]+range(3,9)]# [dac1,dac15,dac16,dac2,dac3,...,dac14]
filename='dat'
#########   END modify here ################
ind1 = len(filename)+1
py_folder = os.path.split(os.path.realpath(__file__))[0]
fd = [int(x[ind1:-4]) for x in os.listdir(d_folder) if x.endswith('.set')]
ind_data = [min(fd),max(fd)]
fd = [int(x[ind1:-4]) for x in os.listdir(py_folder) if x.endswith('.png')]
ind_png = [min(fd),max(fd)] if fd else [-1,-1]
print ind_data,ind_png
  
st_old=OrderedDict()
tstamp_old=None
html_1 = ''
html_2 = ''
for i in range(n,ind_data[1]):
    if i < ind_png[0] or i > ind_png[1]:
        f1 = d_folder+'\\'+filename+'_%d.meta.txt'%i
        f2 = d_folder+'\\'+filename+'_%d.set'%i
        png_path = os.path.split(f2[:-4]+'.png')[1]#only file name, not full path
        
        scan = get_meta(f1)
        st, tstamp = get_set(f2)#setting after scan, timstamp at which a scan begins
        t_elapse = (os.path.getmtime(f2)-time.mktime(tstamp))/60.

        if (tstamp_old is None):#which means st_old is also empty
            f2 = d_folder+'\\'+filename+'_%d.set'%(i-1)
            if os.path.isfile(f2):
                st_old, tstamp_old = get_set(f2)

        print os.path.split(f2[:-4])[1]#data filename
        print get_other_change(st_old,st,scan)#print the change before a scan starts
        print scan#print the scan
        print
        
        plot_setting(st_old,st,scan,os.path.join(py_folder,png_path),t_elapse)# plot it
        
        isnewday = (tstamp_old is None) or tstamp_old[2] != tstamp[2]
        html = '<hr><h1>%s</h1>\n'%time.asctime(tstamp) if isnewday else ''
        bg_clr = 'CAEFD1' if 6<=tstamp[3]<12 else ('FFF2CC' if 12<=tstamp[3]<18 else ('B892FF' if 18<=tstamp[3]<24 else '8086FB'))
        html += '<div style="background:#%s"><img src="%s" align="middle"> Final: %s</div>\n'%(bg_clr,png_path, str(st.values()))  
        if i < ind_png[0]:
            html_1 += html
        else:
            html_2 += html
        
        st_old = st
        tstamp_old = tstamp
        
    else:
        st_old = OrderedDict()
        tstamp_old = None
h_path = os.path.join(py_folder,'scan.html')
if os.path.isfile(h_path):
    f = open(h_path,'r')
    html = f.read()
    f.close()
else:
    html = ''
f = open(h_path,'w')
f.write(html_1+html+html_2)
f.close()
    
