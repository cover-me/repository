# A general scan script for qtlab
# modified from sudc.py by Po
# what's new
# 18.06.17 add scan delay/rates/elapsed/filename to .doc notes
# 18.07.22 add _scan1d. auto qtplot now works with 1d bwd
from numpy import linspace, zeros, shape, arange, repeat, allclose, vstack, empty, nan, meshgrid, save, load
from lib.file_support.spyview import SpyView
import qt
import timetrack
import sys
import data as d
import traces
import os
from time import time, strftime
import socket
from shutil import copyfile, rmtree
from tempfile import mkdtemp
class qtplot_client():
    def __init__(self,mute=False,mmap2npy=True,interval = 1):
        self.mute = mute #mute the client or not
        self.mmap2npy = mmap2npy #create .npy file or not
        self.filepath = ''#.dat file path
        self.npy_path = ''
        self.lastfile = ''
        self.last_update_time = 0
        self.mdata = None#mapped data from .npy file
        self.counter = 0
        self.interval = interval
    def set_file(self,filepath,col=0,x_pts=[],y_pts=[]):
        if not self.mute:
            self.filepath = filepath
            if self.mmap2npy:
                self.npy_path = os.path.join(mkdtemp(), 'qtplot_temp.npy')
                meta_path = self.npy_path[:-3]+'meta.txt'
                copyfile(filepath,meta_path)
                row = len(x_pts) * len(y_pts)
                m = empty((row,col))*nan
                m[:,:2] = vstack(meshgrid(x_pts,y_pts)).reshape(2,-1).T
                save(self.npy_path,m)
                self.mdata = load(self.npy_path, mmap_mode='r+')
    def add_data(self,values):
        if (not self.mute) and self.mmap2npy:
            self.mdata[self.counter,:] = values
            self.counter += 1
    def update_plot(self):#if mmap2npy, there will be an interval
        if not self.mute and (time()>self.last_update_time+self.interval or not self.mmap2npy):
            self.last_update_time = time()
            filename = self.npy_path if self.mmap2npy else self.filepath
            try:
                sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sckt.connect(('127.0.0.1',1787))
                if self.lastfile == filename:
                    sckt.send('REFR:%s'%filename)
                else:
                    print 'update qtplot with the new file ...',
                    self.lastfile = filename
                    sckt.send('FILE:%s;SHOW:'%filename)
                    print sckt.recv(128)
                sckt.close()
            except Exception:
                self.mute = True
                print 'Socket failed. Mute client.'
    def compare(self,data):
        if (not self.mute) and self.mmap2npy:
            print 'Comparing .npy data and data ...',
            is_equal =  allclose(self.mdata[:self.counter,:],data,rtol=1e-12,atol=0.)
            print '%s!'%is_equal
    def close(self):
        del self.mdata
        if (not self.mute) and self.lastfile.endswith('.npy'):
            self.mmap2npy = False
            self.update_plot()
            self.mute = True
        if self.npy_path != '':
            rmtree(os.path.split(self.npy_path)[0],ignore_errors=True)
class easy_scan():
    def __init__(self):
        self._filename=filename
        self._datapath=datapath if datapath.endswith('\\') else (datapath+'\\')
        self._generator=d.IncrementalGenerator(self._datapath+self._filename,1)
        self._vallabels = g.get_vallabels()#value labels, [reading1, reading2, reading3, ..]
        self._coolabels = ['','','']#coordinator labels, [output1, output2, output3]
    def _print_gnucmd(self,dfpath,dfpath_bwd):
        lbs = self._coolabels + self._vallabels
        gnucmd = "set xlabel '%s' font ',11';set ylabel '%s' font ',11';"%(lbs[colx-1],lbs[coly-1])
        gnucmd += r"set format x '%.03s %c';set format y '%.01s %c';"
        gnucmd += "plot '%s' using %d:%d with lp"%(dfpath,colx,coly)
        gnucmd += ", '%s' using %d:%d with lp ls 3"%(dfpath_bwd,colx,coly) if dfpath_bwd else ""
        print "\n*****You can now copy the following command to gnuplot*****\n" + gnucmd + '\n'
    def _print_progress(self,x,values,is_fwd_now):
        pbar_width = 5
        a = int(x*(pbar_width+1))
        b = 2*(pbar_width-a)
        ch = chr(2) if is_fwd_now else chr(1)
        progress_bar = '\r('+'_'*a+ch+'_'*b+ch+'_'*a+') ' if b>0 else '\r(%s) '%('_'*(pbar_width*2+2))
        progress_bar += ' '.join(['%+.2e']*len(values))%tuple(values)
        print progress_bar[:TERM_WIDTH],
    def _sendToWord(self,msg,addTimestamp=True):
        towordPath = r'..\toWord.2018.06.17\toWord.2018.06.17.exe'
        if os.path.isfile(towordPath):
            _ = strftime('%m/%d %H:%M, ')+msg if addTimestamp else msg
            os.system('%s'%towordPath+' "%s"'%_)
        else:
            print 'toWord: Can not find toWord.exe'
    #generate data file, spyview file and copy the pyton script.
    def _create_data(self,
                    x_vector,x_coordinate,x_parameter,#coordinate: labels, parameter: the string that specifies a channel
                    y_vector,y_coordinate,y_parameter,
                    z_vector,z_coordinate,z_parameter,bwd=False):
        qt.Data.set_filename_generator(self._generator)
        data = qt.Data(name=self._filename)
        self._coolabels = ['%s_(%s)'%(x_parameter,x_coordinate),'%s_(%s)'%(y_parameter,y_coordinate),'%s_(%s)'%(z_parameter,z_coordinate)]
        (xstart,xend) = (x_vector[-1],x_vector[0]) if bwd else (x_vector[0],x_vector[-1])
        data.add_coordinate(self._coolabels[0],
                            size=len(x_vector),
                            start=xstart,
                            end=xend) 
        data.add_coordinate(self._coolabels[1],
                            size=len(y_vector),
                            start=y_vector[0],
                            end=y_vector[-1]) 
        data.add_coordinate(self._coolabels[2],
                            size=len(z_vector),
                            start=z_vector[0],
                            end=z_vector[-1])
        for i in self._vallabels:
            data.add_value(i)#add value labels
        data.create_file()#Create data file
        SpyView(data).write_meta_file()#Create spyview meta.txt file
        qscan_file_path = sys._getframe().f_code.co_filename
        qscan_copyto_path = os.path.join(data._dir,os.path.split(qscan_file_path)[1])
        if not os.path.isfile(qscan_copyto_path):
            print 'Copy file:', qscan_file_path
            copyfile(qscan_file_path,qscan_copyto_path)
        traces.copy_script(this_file_path,data._dir,self._filename+str(self._generator._counter-1))# Copy the python script into the data folder
        data._file.flush()
        return data
    def _paraok_scan(self,a,b,c):
        '''check whether parameters are OK for self._scan()'''
        if 1==len(shape(a))==len(shape(b))==(len(shape(c))-1) and len(a)==len(b)==len(c):
            return True
        else:
            print '_scan(): parameter error'
            return False
    def _paraokscan(self,a,b,c,d):
        '''check whether parameters are OK for self.scan()'''
        isok = False
        if len(shape(a))==len(shape(b))==len(shape(c))== len(shape(d))<2:
            if len(shape(a))==0:#0d
                isok = True
            elif len(a)==len(b)==len(c)==len(d):#1d
                isok = True
        if not isok:
            print 'scan(): parameter error'
        return isok
    def _scan(self,
               xlbl=[''],xchan=['xchannel'],xpnt=[[0]],
               ylbl=[''],ychan=['ychannel'],ypnt=[[0]],
               zlbl=[''],zchan=['zchannel'],zpnt=[[0]],bwd=False,xswp_by_mchn=False):
        #check parameters
        if self._paraok_scan(xlbl,xchan,xpnt) and self._paraok_scan(ylbl,ychan,ypnt) and self._paraok_scan(zlbl,zchan,zpnt):
            xlen = len(xlbl);ylen = len(ylbl);zlen = len(zlbl)
            xptlen = len(xpnt[0]);yptlen = len(ypnt[0]);zptlen = len(zpnt[0])
            if xswp_by_mchn and xptlen!=2:
                print 'You have set xswp_by_mchn=True while left xsteps!=1. No sweeps have been performed'
                return
        else:
            return
        if xswp_by_mchn:
            print '\n********WARNING********\nxswp_by_mchn=True:\n    sweeping in the instrument side may NOT stop after you stop or pause the program manually\n    output will be set to the last value in the first loop!!'
        #start
        qt.mstart()
        t_scanstart = time() 
        data = self._create_data(xpnt[0],xlbl[0],xchan[0],ypnt[0],ylbl[0],ychan[0],zpnt[0],zlbl[0],zchan[0])# create data file, spyview metafile, copy script
        data_bwd = self._create_data(xpnt[0],xlbl[0],xchan[0],ypnt[0],ylbl[0],ychan[0],zpnt[0],zlbl[0],zchan[0],bwd) if bwd else None
        data_loop = [data,data_bwd]
        counter = 0
        numloops = yptlen*zptlen
        dfpath = data.get_filepath()
        qclient = qtplot_client(mute=(zptlen!=1),mmap2npy=True)#only works for 1 and 2d
        qclient.set_file(dfpath,3+len(self._vallabels),xpnt[0],ypnt[0])
        qclient.update_plot()
        dfpath_bwd = data_bwd.get_filepath() if bwd else None
        if is_print_cmd:#print command for gnuplot
            self._print_gnucmd(dfpath,dfpath_bwd)
        print 'Start scanning: %d lines, %d points per line'%(numloops,xptlen)
        print 'File path:', dfpath, '| %s'%os.path.split(dfpath_bwd)[1] if bwd else ''
        print 'Labels:', self._coolabels + self._vallabels
        self.user_interrrupt = False
        ############# scan #############
        try:
            # set z channel(s)
            for iz in arange(zptlen):
                for i in arange(zlen):
                    g.set_val(zchan[i],zpnt[i][iz])
                z_val0 = zpnt[0][iz]
                # set y channel(s) and initialize x channel(s)
                for iy in arange(yptlen):
                    [starttime, counter] = timetrack.start(counter)
                    for i in arange(ylen):
                        g.set_val(ychan[i],ypnt[i][iy])
                    y_val0 = ypnt[0][iy]
                    for i in arange(xlen):
                        g.set_val(xchan[i],xpnt[i][0])
                    # delay after setting x back to x[0]
                    qt.msleep(delay1)
                    # sweep x channel(s)
                    is_fwd_now = True
                    is1d = (numloops==1)
                    t0 = time()
                    for d_item in data_loop:# there may be two sets of data (if bwd=True), one for sweeping forward and the other for sweeping backward
                        if d_item:
                            if is_fwd_now==False and is1d:
                                print
                                qclient.compare(data.get_data())
                                qclient.close()
                                qclient = qtplot_client(mute=(zptlen!=1),mmap2npy=True)
                                qclient.set_file(dfpath_bwd,3+len(self._vallabels),xpnt[0][::-1],ypnt[0][::-1])
                                qclient.update_plot()
                            self._scan1d(xchan,xpnt,xptlen,xlen,d_item,is_fwd_now,xswp_by_mchn,y_val0,z_val0,is1d,qclient)
                            is_fwd_now = not is_fwd_now
                    print '\r'+' '*TERM_WIDTH+'\r%.1f, %.3f'%((time()-t0),(time()-t0)/xptlen),
                    timetrack.remainingtime(starttime,numloops,counter)# Calculate and print remaining scantime
            print
        ############# end scan #############
        except KeyboardInterrupt:#so the data file can be closed normally if one pressed ctrl+c
            print '\n\nInterrupted by ctrl+c'
            self.user_interrrupt = True
        for d_item in data_loop:
            if d_item:
                d_item._write_settings_file()# Overwrite the settings file created at the beginning, this ensures updating the sweep variable with the latest value
                d_item.close_file()
        if bwd==True and is1d:
            qclient.compare(data_bwd.get_data())
        else:
            qclient.compare(data.get_data())
        qclient.close()
        qt.mend()
        t_scan = (time()-t_scanstart)/60
        print 'Scan finished.'
        dfname = data.get_filename().replace('.dat','')
        dfname_bwd = '/%s'%data_bwd.get_filename().replace('.dat','') if data_bwd else ''
        self._sendToWord('%.1f, %s%s<return>'%(t_scan,dfname,dfname_bwd),addTimestamp=False)
        if self.user_interrrupt:
            sys.exit()
    def _scan1d(self,xchan,xpnt,xptlen,xlen,d_item,is_fwd_now,xswp_by_mchn,y_val0,z_val0,is1d,qclient):#y_val0=ypnt[0][iy],z_val0=zpnt[0][iz]
        ix = 0 if is_fwd_now else (xptlen-1)
        index_end = xptlen-1-ix
        issweeping = False
        while -1 < ix < xptlen:
            #set xchans
            if not issweeping:
                if xswp_by_mchn:
                    for i in arange(xlen):
                        g.set_val(xchan[i],xpnt[i][index_end])
                    issweeping = True
                else:
                    for i in arange(xlen):
                        g.set_val(xchan[i],xpnt[i][ix])
            #delay before each point
            if delay2>0:
                qt.msleep(delay2)
            #get xchans
            x_val0 = g.get_val(xchan[0]) if xswp_by_mchn else xpnt[0][ix]
            #take and log data
            datavalues = [x_val0,y_val0,z_val0]+g.take_data()
            d_item.add_data_point(*datavalues)
            self._print_progress(1.*ix/xptlen,datavalues,is_fwd_now)
            if is_fwd_now or is1d:
                qclient.add_data(datavalues)
                qclient.update_plot()
            #change ix
            if xswp_by_mchn:
                ix = 0 if xpnt[0][0]<=x_val0<=xpnt[0][-1] or xpnt[0][-1]<=x_val0<=xpnt[0][0] else -1
            else:
                ix += 1 if is_fwd_now else -1
        d_item.new_block()
    def scan(self,
               xlbl=[''],xchan=['xchannel'],xstart=[0],xend=[0],xsteps=0,
               ylbl=[''],ychan=['ychannel'],ystart=[0],yend=[0],ysteps=0,
               zlbl=[''],zchan=['zchannel'],zstart=[0],zend=[0],zsteps=0,bwd=False,xswp_by_mchn=False):
        #check parameters:
        if self._paraokscan(xlbl,xchan,xstart,xend):
            if len(shape(xlbl))==0:
                xlbl=[xlbl];xchan=[xchan];xstart=[xstart];xend=[xend]
        else:
            return
        if self._paraokscan(ylbl,ychan,ystart,yend):
            if len(shape(ylbl))==0:
                ylbl=[ylbl];ychan=[ychan];ystart=[ystart];yend=[yend]
        else:
            return
        if self._paraokscan(zlbl,zchan,zstart,zend):
            if len(shape(zlbl))==0:
                zlbl=[zlbl];zchan=[zchan];zstart=[zstart];zend=[zend]
        else:
            return
        print '  %s \n'%('_'*(TERM_WIDTH-3)) +' (%s)\n'%('_'*(TERM_WIDTH-3))
        #send message to word
        scanStr = "scan(%s,%s,%s,%s,%s, "%(xlbl,xchan,xstart,xend,xsteps) if xsteps else ''
        scanStr += "%s,%s,%s,%s,%s, "%(ylbl,ychan,ystart,yend,ysteps) if ysteps else ''
        scanStr += "%s,%s,%s,%s,%s, "%(zlbl,zchan,zstart,zend,zsteps) if zsteps else ''
        scanStr += "bwd=True, " if bwd else ''
        scanStr += "xswp_by_mchn=True, " if xswp_by_mchn else ''
        if scanStr[-2:] == ", ":#drop last ', ' away
            scanStr = scanStr[:-2]
        scanStr += '), dly(%s,%s), rt(%s,%s,%s), '%(delay1,delay2,g.get_rate(xchan[0]),g.get_rate(ychan[0]),g.get_rate(zchan[0]))
        self._sendToWord(scanStr)
        #generate points
        xchnum = len(xchan)
        xpnt = zeros((xchnum,xsteps+1))
        for i in arange(xchnum):
            xpnt[i] = linspace(xstart[i],xend[i],xsteps+1)
            
        ychnum = len(ychan)
        ypnt = zeros((ychnum,ysteps+1))
        for i in arange(ychnum):
            ypnt[i] = linspace(ystart[i],yend[i],ysteps+1)
            
        zchnum = len(zchan)
        zpnt = zeros((zchnum,zsteps+1))
        for i in arange(zchnum):
            zpnt[i] = linspace(zstart[i],zend[i],zsteps+1)
            
        self._scan(xlbl,xchan,xpnt,
               ylbl,ychan,ypnt,
               zlbl,zchan,zpnt,bwd,xswp_by_mchn)
    def set(self,chan,val):
        scanStr = "set(%s,%s)<return>"%(chan,val)
        if chan == 'ivvi':
            for i in ivvi.get_parameter_names():
                g.set_val(i,val)
        elif chan == 'ivvi_rate':
            delay = 30
            scanStr += ', %s ms'%delay
            for i in ivvi.get_parameter_names():
                ivvi.set_parameter_rate(i,val,delay)
        else:
            g.set_val(chan,val)
        self._sendToWord(scanStr)
class get_set():
    '''get readings, set outputs'''
    def __init__(self):
        self.t0  = time()
        self._rdlabels = []#labels used for taking data
        self._rdchans = []
        self._prcss_labels = ['time']
        self._prcss_list = []
        for a,b in instruments_to_read:
            insObj = qt.instruments.get(a)._ins
            if hasattr(insObj,'_address') and insObj._address.startswith('GPIB') and hasattr(insObj,'_visainstrument'):
                print 'visa_clear: %s'%a
                qt.instruments.get(a)._ins._visainstrument.clear()#clear the buffer
            if hasattr(qt.instruments.get(a),'get_all'):
                print 'get_all:    ', a
                qt.instruments.get(a).get_all()
            if a.startswith('lockin'):
                self._rdlabels.append(('%s (%s)'%(a,b)).replace('lockin',"lockin_R"))
                self._rdlabels.append(('%s (%s)'%(a,b)).replace('lockin',"lockin_P"))
                self._rdchans.append(qt.instruments.get(a))
                self._rdchans.append(qt.instruments.get(a))
            else:
                self._rdlabels.append('%s (%s)'%(a,b))
                self._rdchans.append(qt.instruments.get(a))
        if not all(self._rdchans):
            print 'Some instruments you want to read has not been loaded by qtlab. No scan has been done.'
            sys.exit()
        self._rdnum = len(self._rdlabels)
    def take_data(self):
        '''take data from input channels and do some calculation'''
        val = []
        #print 'taking data'
        for i in range(self._rdnum):
            lb = self._rdlabels[i]
            ch = self._rdchans[i]
            if lb.startswith('keithley'):
                val.append(ch.get_readlastval())
            elif lb.startswith('lockin_R'):#make sure to keep consistent with self._rdlabels
                val.append(ch.get_R())
            elif lb.startswith('lockin_P'):#make sure to keep consistent with self._rdlabels
                val.append(ch.get_P())
            elif lb.startswith('Lakeshore'):
                val.append(ch.get_kelvinA())
            elif lb.startswith('LPR'):
                val.append(ch.get_MC())
            else:
                print 'cannot read channel: %s\n!!!'%ch
        val = val + self.get_prcss(val)#add processed data        
        #qt.msleep(0.01)
        return val
    def get_vallabels(self):
        return self._rdlabels + self._prcss_labels
    def is_dac_name(self,dn):#'dn': dac name
        return len(dn)<6 and dn[0:3]=='dac' and dn[3:5].isdigit() and int(dn[3:5])<=16
    def get_val(self,chan):#'chan': channel
        '''get values from an output channel, keep update with set_val!'''
        if self.is_dac_name(chan):
            return ivvi.get(chan)# 4.3 ms
        elif chan == 'magnet' or chan == 'magnetX':
            return qt.instruments.get(chan).get_field()#same speed as magnet.get_field(), ~ 600 ms
        elif chan == 'Lakeshore':
            return qt.instruments.get(chan).get_kelvinA()
        elif chan == 'time':
            return time()-self.t0
    def set_val(self,chan,val):
        '''set values of an output channel, keep update with get_val and get_rate!'''
        if self.is_dac_name(chan):
            #print 'setting %s to %f'%(chan,val)
            return ivvi.set(chan,val)
        elif chan == 'magnet' or chan == 'magnetX':
            #print 'setting B to %f'%(val)
            return qt.instruments.get(chan).set_field(val)
        # elif chan == 'magnet_r_theta':better to write a driver
            # t_rad = val2/180.*math.pi
            # x = val*math.cos(t_rad)
            # z = val*math.sin(t_rad)
            # qt.instruments.get('magnetX').set_field(x)
            # return qt.instruments.get('magnet').set_field(z)
        elif chan == 'Lakeshore':
            return qt.instruments.get(chan).set_setpoint1(val)
        return False
    def get_rate(self,chan):
        '''get rates from an output channel, keep update with set_val!'''
        if self.is_dac_name(chan):
            _ = ivvi.get_parameters()[chan]
            return '%s/%s'%(_['maxstep'],_['stepdelay'])
        elif chan == 'magnet' or chan == 'magnetX':
            _ = qt.instruments.get(chan).get_rampRate()
            return '%s'%_
        return ''   
    ############## process data #####################
    def add_lockin_conductance(self,arg_dict):
        '''
        lockin_osc: lockin osc out * 0.01
        Vrange: ivvi output voltage range in V/V, usually 0.01
        Igain: 1.e6
        '''
        names = ['index','label','Rin','lockin_osc','Vrange','Igain']
        if len(arg_dict) != len(names) or (not all([(i in arg_dict) for i in names])):
            print 'Failed to add lockin_conductance!'
            return
        self._prcss_labels.append(arg_dict['label'])
        self._prcss_list.append({'function':self.get_lockin_conductance,'arg':arg_dict})
    def get_lockin_conductance(self,arg_dict,val):
        ac_excitation = arg_dict['lockin_osc'] * arg_dict['Vrange']
        ac_current = val[arg_dict['index']]/arg_dict['Igain']
        sigma = ac_current/ac_excitation
        r0 = 12906
        return r0*sigma/(1.-arg_dict['Rin']*sigma)
    def get_prcss(self,val):
        p_val = [time()-self.t0]
        for i in self._prcss_list:
            p_val.append(i['function'](i['arg'],val))
        return p_val

def get_term_width():#get linewith of the console
    a, b = os.popen('mode con /status').read().split('\n')[4].strip().split(':')
    if a == 'Columns':
        return int(b)
TERM_WIDTH = get_term_width()-1
print '''
%s  __   ____   ___   __   __ _
%s /  \ / ___) / __) / _\ (  ( \ 
%s(  O )\___ \( (__ /    \/    /
%s \__\)(____/ \___)\_/\_/\_)__)
'''%(tuple([' '*(TERM_WIDTH/2-15)]*4))
ivvi = qt.instruments.get('ivvi')
is_print_cmd = True