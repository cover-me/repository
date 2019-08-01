execfile('Qscan.180515.py')
this_file_path = sys._getframe().f_code.co_filename
datapath=r'C:\Users\labuser\Desktop\delete_me'+'\\%s'%strftime('%Y-%m')
filename='data'

delay1 = 1#delay in seconds after setting z, y, and x[0] (before an x-channel scan). Lockin: 10*tau, DC: 1
delay2 = 0.1#delay in seconds before taking data. >=1.5*tau for lockins, default 0.1

instruments_to_read = [('lockin1','1e-6A'),('keithley1','1e-6A'),('Lakeshore','T (K)')]#[(a1,b1),(a2,b2),...],a is an instrument whose readings will be taken, b is a description for the reading.
colx = 1#col number for x axis. Used if is_print_cmd = True, first index is 1
coly = 4#col number for y axis. Used if is_print_cmd = True, first index is 1

g = get_set()
g.add_lockin_conductance({'index':0,'label':'2e2/h','Rin':1.e3,'lockin_osc':0.05*0.01,'Vrange':0.01,'Igain':1.e6})
e = easy_scan()

#MEASUREMENTS
# bwd=True: sweep back after each line; xswp_by_mchn=FALSE or TRUE: usually not used
###1d
#e.scan('Vbias(*0.01mV)','dac2',0,500,100)
#e.scan('Bg(mV)','dac1',0,3000,300)
#e.scan('T_set(K)','Lakeshore',10,5,200)
#e.scan('time1 (s)','time',0,100,50)
#t0 = time();e.scan('t (s)','time',time()-t0,time()-t0+3600*2,1,xswp_by_mchn=True)
#chns=range(1,17);e.scan(['g%d'%x for x in chns],['dac%d'%x for x in chns],[10 for x in chns],[0 for x in chns],50)
###2d
#e.scan('Vbias(*0.01mV)','dac1',-500,500,100,'Bg(mV)','dac2',-1000,0,200)
#e.scan(['Vdc,*0.01 mV'],['dac1'],[100],[-100],100,     ['repeat'],['repeat'],[0],[1],20, bwd=True)
#e.scan('Ibias(*0.1nA)','dac2',-80,80,200,'Vbg(*15mV)','dac3',0,-400,200)
#e.scan('Vdc, *0.01mV,Vac=5uV','dac1',-300 +17,300 +17,300,'field(T)','magnet',-0.1,5,150)
#e.scan('Ibias(*0.1nA)','dac2',-50,50,200,'field(T)','magnet',-0.2,1,40)
e.scan('time1 (s)','time',0,100,100,'time2 (s)','time',0,100,100)
###3d
#e.scan(['g1'],['dac1'],[0],[3],10,     ['g3'],['dac3'],[0],[3],10,     ['g5'],['dac5'],[0],[3],10)