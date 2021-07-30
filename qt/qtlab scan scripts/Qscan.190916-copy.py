# A(n) all-in-one scan script for qtlab
# Project page: https://github.com/cover-me/repository
# Upgraded from sudc.py by Po
# Main changes:
# 18.06.17 add scan delay/rates/elapsed/filename to .doc notes
# 18.07.22 add _scan1d. auto qtplot now works with 1d bwd
# 19.08.06 19.08.04 "Ding!" when a scan has finished. Load more scan without stopping current scan.
# 19.09.06 shortcuts ctrl+e and ctrl+n
# 19.09.16 shifted scan, 3D scan, meander scan
import qt,timetrack,sys,os,socket,winsound,msvcrt
import IPython.core.interactiveshell as ips
import numpy as np
import data as d
from lib.file_support.spyview import SpyView
from time import time, strftime
from shutil import copyfile, rmtree
from tempfile import mkdtemp

class qtplot_client():
    '''A client for real-time plotting in qtplot'''
    def __init__(self,mute=False,mmap2npy=True,interval = 1):
        self.mute = mute #mute the client or not
        self.mmap2npy = mmap2npy #whether create mmap .npy file or not
        self.filepath = ''#.dat file path
        self.npy_path = ''
        self.lastfile = ''
        self.last_update_time = 0
        self.mdata = None#mmap data which is plotted by qtplot
        self.counter = 0#real-time row number
        self.interval = interval#minimum refresh interval for qtplot
    def set_file(self,filepath,col=0,x_pts=[],y_pts=[],z_pts=[0]):
        if not self.mute:
            self.filepath = filepath
            if self.mmap2npy:
                self.npy_path = os.path.join(mkdtemp(), 'qtplot_temp.npy')
                meta_path = self.npy_path[:-3]+'meta.txt'
                copyfile(filepath,meta_path)
                row = len(x_pts) * len(y_pts) * len(z_pts)
                m = np.empty((row,col))*np.nan#data matrix
                m[:,0] = np.tile(x_pts,len(y_pts) * len(z_pts))
                m[:,1] = np.tile(np.repeat(y_pts,len(x_pts)),len(z_pts))
                m[:,2] = np.repeat(z_pts,len(x_pts) * len(y_pts))
                np.save(self.npy_path,m)
                self.mdata = np.load(self.npy_path, mmap_mode='r+')
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
                    self.lastfile = filename
                    sckt.send('FILE:%s;SHOW:'%filename)
                    print sckt.recv(128)
                sckt.close()
            except Exception:
                self.mute = True
                print2('\nSocket failed. Mute qtplot client.\n','red')
    def compare(self,data):
        if (not self.mute) and self.mmap2npy:
            print 'Comparing .npy data and data ...',
            is_equal =  np.allclose(self.mdata[:self.counter,:],data,rtol=1e-12,atol=0.)
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
        self._generator=d.IncrementalGenerator(self._datapath+self._filename,1)#data number generator
        self._vallabels = g.get_vallabels()#value labels, [reading1, reading2, reading3, ..]
        self._coolabels = ['','','']#coordinator labels, [output1, output2, output3]. Here, the first 3 column are called coordinators, the rest are called values.
    def _print_progress(self,x,values,is_fwd_now):
        '''print the progress bar as well as readings to the console. The bar looks like (__?______?__)'''
        pbar_width = 5
        a = int(x*(pbar_width+1))
        b = 2*(pbar_width-a)
        ch = chr(2) if is_fwd_now else chr(1)
        progress_bar =  '('+'_'*a+ch+'_'*b+ch+'_'*a+') ' if b>0 else '(%s) '%('_'*(pbar_width*2+2))
        progress_bar += ' '.join(['%+.2e']*len(values))%tuple(values)
        progress_bar = '\r' + STR_TIMEINFO + progress_bar
        print progress_bar[:TERM_WIDTH],    
    def _sendToWord(self,msg,addTimestamp=True):
        towordPath = r'..\toWord.2018.06.17\toWord.2018.06.17.exe'
        if os.path.isfile(towordPath):
            _ = strftime('%m/%d %H:%M, ')+msg if addTimestamp else msg
            os.system('%s'%towordPath+' "%s"'%_)
        else:
            print2('toWord: Can not find toWord.exe\n','red')
    def _create_data(self,
                    x_vector,x_coordinate,x_parameter,
                    y_vector,y_coordinate,y_parameter,
                    z_vector,z_coordinate,z_parameter,bwd=False):
        '''Generate the data file, spyview .meta file and copy scan scripts.'''
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
        SpyView(data).write_meta_file()#Create meta.txt file for spyview
        qscan_file_path = sys._getframe().f_code.co_filename
        qscan_copyto_path = os.path.join(data._dir,os.path.split(qscan_file_path)[1])
        if not os.path.isfile(qscan_copyto_path):
            print 'Copy file:', qscan_file_path
            copyfile(qscan_file_path,qscan_copyto_path)
        to_script_path = "%s\\%s_%s.py" % (data._dir,self._filename,str(self._generator._counter-1))
        if os.path.isfile(this_file_path):
            copyfile(this_file_path,to_script_path)
        else:
            f = open(to_script_path,'w')
            f.write(this_file_path)#It's a code string if the function is called by more_scan()
            f.close()
        data._file.flush()
        return data
    def _paraok_scan(self,xlbl,xchan,xpnt,ylbl,ychan,ypnt,zlbl,zchan,zpnt,xswp_by_mchn,xshift):
        '''check whether parameters are OK for self._scan()'''
        isok = True
        if not (1==len(np.shape(xlbl))==len(np.shape(xchan))==(len(np.shape(xpnt))-1) and len(xlbl)==len(xchan)==len(xpnt)):
            isok = False
        if not (1==len(np.shape(ylbl))==len(np.shape(ychan))==(len(np.shape(ypnt))-1) and len(ylbl)==len(ychan)==len(ypnt)):
            isok = False            
        if not (1==len(np.shape(zlbl))==len(np.shape(zchan))==(len(np.shape(zpnt))-1) and len(zlbl)==len(zchan)==len(zpnt)):
            isok = False
        if xshift and not ('slope' in xshift and xshift['slope']!=0 and 'shift' in xlbl[0] and ('y0' in xshift or 'z0' in xshift)):
            isok = False
        if xswp_by_mchn and len(xpnt[0])!=2:
            isok = False
        if not isok:            
            print2('_scan(): Parameter error','red')
            sys.exit()
        if xswp_by_mchn:
            print2('\n********WARNING********\nxswp_by_mchn=True:\n    sweeping in instruments may NOT stop after you stop or pause the program\n    output will be set to the final value in the innermost loop!!','red')
    def _paraokscan(self,xlbl,xchan,xstart,xend,ylbl,ychan,ystart,yend,zlbl,zchan,zstart,zend):
        '''check whether parameters are OK for self.scan()'''
        isok = True
        if not len(np.shape(xlbl))==len(np.shape(xchan))==len(np.shape(xstart))== len(np.shape(xend))<2:
            isok = False
        if not len(np.shape(ylbl))==len(np.shape(ychan))==len(np.shape(ystart))== len(np.shape(yend))<2:
            isok = False
        if not len(np.shape(zlbl))==len(np.shape(zchan))==len(np.shape(zstart))== len(np.shape(zend))<2:
            isok = False
        if len(np.shape(xlbl))==1 and not len(xlbl)==len(xchan)==len(xstart)==len(xend):
            isok = False
        if len(np.shape(ylbl))==1 and not len(ylbl)==len(ychan)==len(ystart)==len(yend):
            isok = False
        if len(np.shape(zlbl))==1 and not len(zlbl)==len(zchan)==len(zstart)==len(zend):
            isok = False
        if not isok:
            print2('scan(): Parameter error','red')
            sys.exit()
    def _scan(self,
               xlbl=[''],xchan=['xchannel'],xpnt=[[0]],
               ylbl=[''],ychan=['ychannel'],ypnt=[[0]],
               zlbl=[''],zchan=['zchannel'],zpnt=[[0]],bwd=False,xswp_by_mchn=False,meander=False,xshift=None):
        self._paraok_scan(xlbl,xchan,xpnt,ylbl,ychan,ypnt,zlbl,zchan,zpnt,xswp_by_mchn,xshift)#check parameters
        xlen = len(xlbl);ylen = len(ylbl);zlen = len(zlbl)
        xptlen = len(xpnt[0]);yptlen = len(ypnt[0]);zptlen = len(zpnt[0])
        #start
        qt.mstart()
        t_scanstart = time()
        data = self._create_data(xpnt[0],xlbl[0],xchan[0],ypnt[0],ylbl[0],ychan[0],zpnt[0],zlbl[0],zchan[0])# create data file, spyview metafile, copy script
        data_bwd = self._create_data(xpnt[0],xlbl[0],xchan[0],ypnt[0],ylbl[0],ychan[0],zpnt[0],zlbl[0],zchan[0],bwd) if bwd else None
        data_loop = [data,data_bwd]
        counter = 0#counter for scan
        global STR_TIMEINFO
        STR_TIMEINFO = '' 
        numloops = yptlen*zptlen
        dfpath = data.get_filepath()
        qclient = qtplot_client(mmap2npy=True)#only works for 1 and 2d
        qclient.set_file(dfpath,3+len(self._vallabels),xpnt[0],ypnt[0],zpnt[0])
        qclient.update_plot()
        dfpath_bwd = data_bwd.get_filepath() if bwd else None
        print 'File:', dfpath, '| %s'%os.path.split(dfpath_bwd)[1] if bwd else ''
        print 'Labels:', self._coolabels + self._vallabels
        print 'Scan: %d lines, %d points per line'%(numloops,xptlen)
        print '...\nctrl+e: exit more safely; ctrl+n: next scan.'
        self.user_interrrupt = False
        ############# scan #############
        try:
            # set z channel(s)
            for iz in np.arange(zptlen):
                for i in np.arange(zlen):
                    g.set_val(zchan[i],zpnt[i][iz])
                z_val0 = zpnt[0][iz]
                if delay0>0:
                    for i in np.arange(ylen):
                        g.set_val(ychan[i],ypnt[i][0])
                    qt.msleep(delay0)
                # set y channel(s) and initialize x channel(s)
                for iy in np.arange(yptlen):
                    t0 = time()
                    for i in np.arange(ylen):
                        g.set_val(ychan[i],ypnt[i][iy])
                    y_val0 = ypnt[0][iy]
                    if xshift:
                        if 'y0' in xshift:
                            xpnt2 = xpnt + (y_val0-xshift['y0'])/xshift['slope']
                        elif 'z0' in xshift:
                            xpnt2 = xpnt + (z_val0-xshift['z0'])/xshift['slope']
                    else:
                        xpnt2 = xpnt
                    if meander and iy%2==1:
                        xpnt2 = xpnt2[:,::-1]#xpnt2[:,] = xpnt2[:,::-1] affects xpnt
                    if delay1>0:
                        for i in np.arange(xlen):
                            g.set_val(xchan[i],xpnt2[i][0])
                        qt.msleep(delay1)
                    # sweep x channels
                    is_fwd_now = True
                    is1d = (numloops==1)
                    t1 = time()
                    for d_item in data_loop:# there may be two sets of data (if bwd=True), one for sweeping forward and the other for sweeping backward
                        if d_item:
                            if is_fwd_now==False and is1d:
                                print
                                qclient.compare(data.get_data())
                                qclient.close()
                                qclient = qtplot_client(mute=(zptlen!=1),mmap2npy=True)
                                qclient.set_file(dfpath_bwd,3+len(self._vallabels),xpnt2[0][::-1],ypnt[0],zpnt[0])#1d data
                                qclient.update_plot()
                            self._scan1d(xchan,xpnt2,xptlen,xlen,d_item,is_fwd_now,xswp_by_mchn,y_val0,z_val0,is1d,qclient)
                            is_fwd_now = not is_fwd_now
                    t2 = time()
                    counter += 1
                    STR_TIMEINFO = '%.3f,%.1f'%((t2-t1)/xptlen,(t2-t0)*(numloops-counter)/60)
        ############# end scan #############
        except UserWarning as warning:
            if warning.message=='next':
                print '\n\n'
                pass
        except KeyboardInterrupt:#so the data file can be closed normally if one pressed ctrl+c
            print2('\n\nInterrupted by user','red')
            self.user_interrrupt = True
        print
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
                    for i in np.arange(xlen):
                        g.set_val(xchan[i],xpnt[i][index_end])
                    issweeping = True
                else:
                    for i in np.arange(xlen):
                        g.set_val(xchan[i],xpnt[i][ix])
            #delay before each point
            qt.msleep(delay2)
            #get xchans
            x_val0 = g.get_val(xchan[0]) if xswp_by_mchn else xpnt[0][ix]
            #take and log data
            datavalues = [x_val0,y_val0,z_val0]+g.take_data()#takes tens of ms
            d_item.add_data_point(*datavalues)#takes around 1 ms or less
            self._print_progress(1.*ix/xptlen,datavalues,is_fwd_now)
            if is_fwd_now or is1d:
                qclient.add_data(datavalues)
                qclient.update_plot()
            #
            last_key = ''
            while msvcrt.kbhit():
               last_key = msvcrt.getch()
            if last_key == '\x05':#ctrl+e(xit)
                raise KeyboardInterrupt
            elif last_key == '\x0e':#ctrl+n(ext)
                raise UserWarning('next')
            #change ix
            if xswp_by_mchn:
                ix = 0 if xpnt[0][0]<=x_val0<=xpnt[0][-1] or xpnt[0][-1]<=x_val0<=xpnt[0][0] else -1
            else:
                ix += 1 if is_fwd_now else -1
        d_item.new_block()
    def scan(self,
               xlbl=[''],xchan=['xchannel'],xstart=[0],xend=[0],xsteps=0,
               ylbl=[''],ychan=['ychannel'],ystart=[0],yend=[0],ysteps=0,
               zlbl=[''],zchan=['zchannel'],zstart=[0],zend=[0],zsteps=0,bwd=False,xswp_by_mchn=False,meander=False,xshift=None):
        """
        Each dimension can be a list of channels or a single channel, or empty.
        bwd: If True, there will be two data files. One for sweeping xchannels forward. The other one for sweeping xchannels backward.
        xswp_by_mchn: Sometimes you want the magnetic field to ramp by itself and take data, instead of stepping up with a list of setpoints.
        meander: Scan x-y channels with in a meander way.
        xshift: Shift x channel setpoints depending on the setpoints of y (or z) with a slope.
        """
        #check parameters
        self._paraokscan(xlbl,xchan,xstart,xend,ylbl,ychan,ystart,yend,zlbl,zchan,zstart,zend)
        if len(np.shape(xlbl))==0:
            xlbl=[xlbl];xchan=[xchan];xstart=[xstart];xend=[xend]
        if len(np.shape(ylbl))==0:
            ylbl=[ylbl];ychan=[ychan];ystart=[ystart];yend=[yend]
        if len(np.shape(zlbl))==0:
            zlbl=[zlbl];zchan=[zchan];zstart=[zstart];zend=[zend]

        #send message to word
        # print2('','scan',True)#set font color
        scanStr = "e.scan(%s,%s,%s,%s,%s, "%(xlbl,xchan,xstart,xend,xsteps) if xsteps or xlbl[0] else ''
        scanStr += "%s,%s,%s,%s,%s, "%(ylbl,ychan,ystart,yend,ysteps) if ysteps or ylbl[0] else ''
        scanStr += "%s,%s,%s,%s,%s, "%(zlbl,zchan,zstart,zend,zsteps) if zsteps or zlbl[0] else ''
        scanStr += "bwd=True, " if bwd else ''
        scanStr += "xswp_by_mchn=True, " if xswp_by_mchn else ''
        scanStr += "meander=True, " if meander else ''
        scanStr += "xshift=%s, "%xshift if xshift else ''
        if scanStr[-2:] == ", ":#drop last ', ' away
            scanStr = scanStr[:-2]
        scanStr += '), dly(%s,%s,%s), rt(%s,%s,%s), '%(delay0,delay1,delay2,g.get_rate(xchan[0]),g.get_rate(ychan[0]),g.get_rate(zchan[0]))
        self._sendToWord(scanStr)
        
        #generate points
        xchnum = len(xchan)
        xpnt = np.zeros((xchnum,xsteps+1))
        for i in np.arange(xchnum):
            xpnt[i] = np.linspace(xstart[i],xend[i],xsteps+1)
            
        ychnum = len(ychan)
        ypnt = np.zeros((ychnum,ysteps+1))
        for i in np.arange(ychnum):
            ypnt[i] = np.linspace(ystart[i],yend[i],ysteps+1)
            
        zchnum = len(zchan)
        zpnt = np.zeros((zchnum,zsteps+1))
        for i in np.arange(zchnum):
            zpnt[i] = np.linspace(zstart[i],zend[i],zsteps+1)
            
        self._scan(xlbl,xchan,xpnt,
               ylbl,ychan,ypnt,
               zlbl,zchan,zpnt,bwd,xswp_by_mchn,meander,xshift)
        # print2('','')#set font to default
        print
        winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
    def set(self,chan,val):
        # print2('','set',True)#set font color
        scanStr = "e.set('%s',%s)"%(chan,val)
        if chan == 'ivvi':
            for i in ivvi.get_parameter_names():
                g.set_val(i,val)
        elif chan.endswith('_rate'):
            chan0 = chan[:-5]
            delay = 30
            scanStr += ', %s ms'%delay
            if chan0 == 'ivvi':
                for i in ivvi.get_parameter_names():
                    ivvi.set_parameter_rate(i,val,delay)
            elif g.is_dac_name(chan0):
                    ivvi.set_parameter_rate(chan0,val,delay)
        else:
            g.set_val(chan,val)
        self._sendToWord(scanStr+'<return>')
        # print2('','')#set font to default
        print
    def more_scan(self,script_path):
        global this_file_path
        while os.path.isfile(script_path):
            f = open(script_path,'r')
            code_str = f.read()
            f.close()
            os.remove(script_path)
            print '========= more scan =========\n%s\n============================='%code_str
            this_file_path=code_str
            exec(code_str)
class get_set():
    '''get readings, set outputs'''
    def __init__(self):
        # print2('','yellow',True)#set font color
        self.t0  = time()
        self._rdlabels = []#labels used for taking data
        self._rdchans = []
        self._prcss_labels = ['time']
        self._prcss_list = []
        for a,b in instruments_to_read:
            if a.startswith('lockin'):
                self._rdlabels.append(('%s (%s)'%(a,b)).replace('lockin',"lockin_R"))
                self._rdlabels.append(('%s (%s)'%(a,b)).replace('lockin',"lockin_P"))
                chn = qt.instruments.get(a)
                self._rdchans.append(chn)
                self._rdchans.append(chn)
            elif a.startswith('[xy]lockin'):
                self._rdlabels.append(('%s (%s)'%(a,b)).replace('[xy]lockin',"lockin_X"))
                self._rdlabels.append(('%s (%s)'%(a,b)).replace('[xy]lockin',"lockin_Y"))
                chn = qt.instruments.get(a[4:])
                self._rdchans.append(chn)
                self._rdchans.append(chn)
            else:
                self._rdlabels.append('%s (%s)'%(a,b))
                chn = qt.instruments.get(a)                
                self._rdchans.append(chn)
            insObj = chn._ins
            if hasattr(insObj,'_address') and insObj._address.startswith('GPIB') and hasattr(insObj,'_visainstrument'):
                print 'visa_clear:\t%s'%a
                insObj._visainstrument.clear()#clear the buffer
            if hasattr(chn,'get_all'):
                print 'get_all:\t', a
                chn.get_all()
        if not all(self._rdchans):
            print2('Some instruments you want to read has not been loaded by qtlab. No scan has been done.','red')
            sys.exit()
        self._rdnum = len(self._rdlabels)
        # print2('','')#set font color
        print
    def take_data(self):
        '''take data from input channels and do some calculation'''
        val = []
        #print 'taking data'
        for i in range(self._rdnum):
            lb = self._rdlabels[i]
            ch = self._rdchans[i]
            if lb.startswith('keithley'):
                val.append(ch.get_readlastval())
            elif lb.startswith('lockin_R'):
                val.append(ch.get_R())
            elif lb.startswith('lockin_P'):
                val.append(ch.get_P())
            elif lb.startswith('lockin_X'):
                val.append(ch.get_X())
            elif lb.startswith('lockin_Y'):
                val.append(ch.get_Y())
            elif lb.startswith('Lakeshore'):
                val.append(ch.get_kelvinA())
            elif lb.startswith('fridge'):
                val.append(ch.get_MC())
            else:
                print2('\nCan\'t read channel: %s\n!!!'%ch,'red')
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
            print2('Failed to add lockin_conductance!\n','red')
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
def print2(s,style='',hold=False):
    stylelist = {'black':'\033[30m','red':'\033[1;31m','green':'\033[32m','yellow':'\033[33m','blue':'\033[34m','magenta':'\033[35m','cyan':'\033[36m','white':'\033[37m',
                'reset':'\033[0m','bold':'\033[1m',
                'scan':'\033[36m','set':'\033[35m',
                }
    post = '' if hold else '\033[0m'
    if style in stylelist:
        ips.io.stdout.write('%s%s%s'%(stylelist[style],s,post))
    else:
        ips.io.stdout.write('%s%s%s'%(style,s,post))
    
TERM_WIDTH = get_term_width()-1
STR_TIMEINFO=''
LOGO = '''
%s\033[1;31m  __   ____   ___   __   __ _
%s\033[1;31m /  \ / ___) / __) / _\ (  ( \ 
%s\033[1;33m(  O )\___ \( (__ /    \/    /
%s\033[1;36m \__\)(____/ \___)\_/\_/\_)__)  \033[1;34mfor qtlab\n
'''%(tuple([' '*(TERM_WIDTH/2-17)]*4))
print2(LOGO)
ivvi = qt.instruments.get('ivvi')
delay0  = 0
