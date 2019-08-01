import numpy as np
import matplotlib.pyplot as plt



def T(R,a):
    return 10.**Tvi(R,a)
    
def Tvi(R,a):
    x = np.log10(R)
    y = a[0]
    for i in range(len(a)-1):
        y = y*x+a[i+1]
    return y

a=[6909.149278,-38314.10597,93795.12172,-132881.1907,120024.6642,-71674.9838,28300.34447,-7125.7046,1038.446473,-66.75479913][::-1]# 10k cal
r = np.linspace(10.04e3,13e3,100)
t = T(r/1000.,a)/1000.
print t[0]
plt.plot(r/1000.,t,'r')

a=[-314.935268221,433.82512402,-219.319060845,53.060384086,-6.241237456,0.287923899][::-1]# -10k cal
t = T(r,a)/1000.
print t[0]
plt.plot(r/1000.,t,'b')

A=[-466.5447894524,2142.4291021063,-4278.3555127331,4917.1299040457,-3583.1401308326,1717.0597135892,-541.2690345353,108.2776759484,-12.4787840217,0.6315795014][::-1]# PT1000 cal

def smooth(x,n=10):
    x = np.convolve(x, np.ones((n,))/n, mode='valid')
    return x[::n]

'''
3: PT1000, 4: 3k, 5: still, 6:cold, 7:MC
'''
fns = [r".\2019-07\datS1907_%d.dat"%i for i in [10,12,16,17,19,21]]
k = 0
for i in fns:
    if k==0:
        a = np.loadtxt(i)
    else:
        a = np.vstack((a,np.loadtxt(i)))
    k += 1
t = T(a[:,3],A)/1000.
r = a[:,4]
r1 = smooth(r)
t1 = smooth(t)
plt.plot(r,t,'r.-')#,r1,t1,'b.')

print np.where(r1<10.0295), r1[32], t1[32]
ind = 32
x1 = np.linspace(r1[0],r1[ind],10)
y1 = np.interp(x1,r1[:ind][::-1],t1[:ind][::-1])
plt.plot(x1,y1,'g.-')
np.savetxt('curve1.txt',np.array([x1[::-1],y1[::-1]*1000.]).T)
x1 = np.concatenate([np.linspace(r1[ind],r1[ind+32],20),np.linspace(r1[ind+33],11.0887,50)])
y1 = np.interp(x1,r1[ind:],t1[ind:])
plt.plot(x1,y1,'k.-')
np.savetxt('curve2.txt',np.array([x1,y1*1000.]).T)
plt.show()