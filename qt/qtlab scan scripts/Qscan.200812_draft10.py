# A(n) all-in-one scan script for qtlab
# Project page: https://github.com/cover-me/repository
# Upgraded from sudc.py by Po
# Main changes:
# 18.06.17 add scan delay/rates/elapsed/filename to .doc notes
# 18.07.22 add _scan1d. auto qtplot now works with 1d bwd
# 19.08.06 19.08.04 "Ding!" when a scan has finished. Load more scan without stopping current scan.
# 19.09.06 shortcuts ctrl+e and ctrl+n
# 19.09.16 shifted scan, 3D scan, meander scan
# 20.08.31 add the parameter "retakejump". remove the parameter "xswp_by_mchn". Store all channels if scanned along a vector of channels.
# todo: 2. make it simpler. 4. non uniform y points. 5. state machine
import qt,timetrack,sys,os,socket,winsound,msvcrt
import IPython.core.interactiveshell as ips
import numpy as np
import data as d
from lib.file_support.spyview import SpyView
from time import time, strftime
from shutil import copyfile, rmtree
from tempfile import mkdtemp

class qtplot_client():
    '''
    A client for real-time plotting in qtplot
    A temp data file is created and mmap is used
    '''
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
    '''
    The class for linear scans up to 3 dimensions, which means, 3 layers of for loops.
    Each dimension of the scan can be a combination of multiple channels, such as ['dac1','dac2','dac3'].
    '''
    def __init__(self):
        self._filename=filename
        self._datapath=datapath if datapath.endswith('\\') else (datapath+'\\')
        self._generator=d.IncrementalGenerator(self._datapath+self._filename,1)#data number generator
        self._vallabels = g.get_vallabels()#value labels, [reading1, reading2, reading3, ..]

    def _print_progress(self,x,values,is_fwd_now,try_times):
        '''print the progress bar as well as readings to the console. The bar looks like (__?______?__)'''
        pbar_width = 5
        a = int(x*(pbar_width+1))
        b = 2*(pbar_width-a)
        ch = chr(2) if is_fwd_now else chr(1)
        progress_bar =  '('+'_'*a+ch+'_'*b+ch+'_'*a+') ' if b>0 else '(%s) '%('_'*(pbar_width*2+2))
        progress_bar += ' '.join(['%+.2e']*len(values))%tuple(values)
        progress_bar = '\r' + STR_TIMEINFO + progress_bar
        if try_times > 0:
            print2(progress_bar[:TERM_WIDTH],'red')
        else:
            print progress_bar[:TERM_WIDTH],
 
    def _sendToWord(self,msg,addTimestamp=True):
        towordPath = r'..\toWord.2018.06.17\toWord.2018.06.17.exe'
        if os.path.isfile(towordPath):
            _ = strftime('%m/%d %H:%M, ')+msg if addTimestamp else msg
            os.system('%s'%towordPath+' "%s"'%_)
        else:
            print2('toWord: Can not find toWord.exe\n','red')

    def _create_data(self,xpnt,xlbl,xchan,ypnt,ylbl,ychan,zpnt,zlbl,zchan):
        '''Generate the data file, spyview .meta file, and copy the .py scan script.'''
        qt.Data.set_filename_generator(self._generator)
        data = qt.Data(name=self._filename)#qtlab data object
        
        setpoint_label_x = ['%s_(%s)'%(i,j) for i,j in zip(xchan,xlbl)]
        setpoint_label_y = ['%s_(%s)'%(i,j) for i,j in zip(ychan,ylbl)]
        setpoint_label_z = ['%s_(%s)'%(i,j) for i,j in zip(zchan,zlbl)]        
        setpoint_labels = [setpoint_label_x[0],setpoint_label_y[0],setpoint_label_z[0]]
        getpoint_labels = self._vallabels
        if len(setpoint_label_x)>1:
            getpoint_labels += setpoint_label_x[1:]
        if len(setpoint_label_y)>1:
            getpoint_labels += setpoint_label_y[1:]
        if len(setpoint_label_z)>1:
            getpoint_labels += setpoint_label_z[1:]
            
        for i,j in zip(setpoint_labels,[xpnt,ypnt,zpnt]):
            _ = j[0]
            data.add_coordinate(i,size=len(_),start=_[0],end=_[-1]) 
        for i in getpoint_labels:
            data.add_value(i)
            
        data.create_file()#Create data file
        SpyView(data).write_meta_file()#Create meta.txt file for spyview
        data._file.flush()

        #copy this file if not copied before
        qscan_file_path = sys._getframe().f_code.co_filename
        qscan_copyto_path = os.path.join(data._dir,os.path.split(qscan_file_path)[1])
        if not os.path.isfile(qscan_copyto_path):
            print 'Copy file:', qscan_file_path
            copyfile(qscan_file_path,qscan_copyto_path)
        #copy and rename scan script
        to_script_path = "%s\\%s_%s.py" % (data._dir,self._filename,str(self._generator._counter-1))
        if os.path.isfile(this_file_path):
            copyfile(this_file_path,to_script_path)
        else:
            f = open(to_script_path,'w')
            f.write(this_file_path)#It's a code string if the function is called by more_scan()
            f.close()
            
        return data
    def _check_scan_para(self,xlbl,xchan,xpnt,ylbl,ychan,ypnt,zlbl,zchan,zpnt,bwd,meander,xshift,retakejump):
        '''check whether parameters are OK for self._scan()'''
        isok = True
        if not (1==len(np.shape(xlbl))==len(np.shape(xchan))==(len(np.shape(xpnt))-1) and len(xlbl)==len(xchan)==len(xpnt)):
            isok = False
        if not (1==len(np.shape(ylbl))==len(np.shape(ychan))==(len(np.shape(ypnt))-1) and len(ylbl)==len(ychan)==len(ypnt)):
            isok = False            
        if not (1==len(np.shape(zlbl))==len(np.shape(zchan))==(len(np.shape(zpnt))-1) and len(zlbl)==len(zchan)==len(zpnt)):
            isok = False
        isok = isok and type(bwd)==bool and type(meander)==bool
        if xshift and not ('slope' in xshift and xshift['slope']!=0 and 'shift' in xlbl[0] and ('y0' in xshift or 'z0' in xshift)):
            isok = False
        if retakejump:
            isok = isok and all([i in retakejump for i in ['index','threshold_x','threshold_y','max_try_times']])
        if not isok:            
            print2('_scan(): Parameter error','red')
            sys.exit()

    def _scan(self,
               xlbl=[''],xchan=['xchannel'],xpnt=[[0]],
               ylbl=[''],ychan=['ychannel'],ypnt=[[0]],
               zlbl=[''],zchan=['zchannel'],zpnt=[[0]],
               bwd=False,meander=False,xshift=None,retakejump=None):
        #Initialize
        self._check_scan_para(xlbl,xchan,xpnt,ylbl,ychan,ypnt,zlbl,zchan,zpnt,bwd,meander,xshift,retakejump)
        xpt_num,ypt_num,zpt_num = len(xpnt[0]),len(ypnt[0]),len(zpnt[0])
        counter = 0#Counter for the progress of scan
        global STR_TIMEINFO,RETAKE_TIMES
        STR_TIMEINFO = '' 
        RETAKE_TIMES = 0
        numloops = ypt_num*zpt_num
        is1d = (numloops==1)
        self.user_interrrupt = False

        #Start
        qt.mstart()
        t_scanstart = time()
        
        #qtlab Data objects
        data = self._create_data(xpnt,xlbl,xchan,ypnt,ylbl,ychan,zpnt,zlbl,zchan)# create data file, spyview metafile, copy script
        data_bwd = self._create_data(xpnt[:,::-1],xlbl,xchan,ypnt,ylbl,ychan,zpnt,zlbl,zchan) if bwd else None
        data_loop = [data,data_bwd]
        dfpath = data.get_filepath()
        dfpath_bwd = data_bwd.get_filepath() if bwd else None
        
        #qtplot communication object
        qclient = qtplot_client(mmap2npy=True)#only works for 1 and 2d
        qclient.set_file(dfpath,3+len(self._vallabels),xpnt[0],ypnt[0],zpnt[0])
        qclient.update_plot()

        print 'File:', dfpath, '| %s'%os.path.split(dfpath_bwd)[1] if bwd else ''
        print 'Labels:', ', '.join([i['name'] for i in data.get_dimensions()])
        print 'Size: %d lines, %d points per line'%(numloops,xpt_num)
        print '-'*24+' Scan started '+'-'*24
        print 'Emergency stop: Press ctrl+c, then manually stop channels that are still changing (magnet), update channel values with xxx.get_xxx() if they are not right. ctrl+c stops the script immediately, there may be unread messages in instrument buffers.'
        print 'Exit script: ctrl+e. Program waits until setting values (field, dac... ) reached, then closes resources and exits; Better than ctrl+c if not in emergencies.'
        print 'Go to next scan: ctrl+n;'
        print 'Pause: Select text by \'shift\' and left mouse keys. It will block the script (but not the magnet).'
        print 'Help: help(e.scan)'
        print 'First two numbers below are elapsed time of each datapoint (s), and remaining time (min)'
        
        ############# scan #############
        try:
            # set z channel(s)
            for iz in np.arange(zpt_num):
                z_iz = zpnt[:,iz]
                for i,j in zip(zchan,z_iz):
                    g.set_val(i,j)
                if delay0>0:
                    y_iy = ypnt[:,0]
                    for i,j in zip(ychan,y_iy):
                        g.set_val(i,j)
                    qt.msleep(delay0)
                # set y channel(s) and initialize x channel(s)
                for iy in np.arange(ypt_num):
                    t0 = time()
                    y_iy = ypnt[:,iy]
                    for i,j in zip(ychan,y_iy):
                        g.set_val(i,j)

                    if xshift:
                        if 'y0' in xshift:
                            xpnt2 = xpnt + (y_iy[0]-xshift['y0'])/xshift['slope']
                        elif 'z0' in xshift:
                            xpnt2 = xpnt + (z_iz[0]-xshift['z0'])/xshift['slope']
                    else:
                        xpnt2 = xpnt
                    if meander and iy%2==1:
                        xpnt2 = xpnt2[:,::-1]#xpnt2[:,] = xpnt2[:,::-1] affects xpnt
                    if delay1>0:
                        for i,j in zip(xchan,xpnt2[:,0]):
                            g.set_val(i,j)
                        qt.msleep(delay1)
                    # sweep x channels
                    is_fwd_now = True
                    t1 = time()
                    for d_item in data_loop:# there may be two sets of data (if bwd=True), one for sweeping forward and the other for sweeping backward
                        if d_item:
                            if is_fwd_now==False and is1d:# If the scan is 1d, plot the realtime backward data as well. Otherwise only forward data is plotted in realtime. 
                                print
                                qclient.compare(data.get_data())
                                qclient.close()
                                qclient = qtplot_client(mute=(zpt_num!=1),mmap2npy=True)
                                qclient.set_file(dfpath_bwd,3+len(self._vallabels),xpnt2[0],ypnt[0],zpnt[0])#1d data
                                qclient.update_plot()
                            self._scan1d(xchan,xpnt2,y_iy,z_iz,d_item,is_fwd_now,is1d,qclient,retakejump)
                            is_fwd_now = not is_fwd_now
                            xpnt2 = xpnt2[:,::-1]
                    t2 = time()
                    counter += 1
                    STR_TIMEINFO = '%.3f,%.1f'%((t2-t1)/xpt_num,(t2-t0)*(numloops-counter)/60)
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
        #Close qtplot client
        if bwd==True and is1d:
            qclient.compare(data_bwd.get_data())
        else:
            qclient.compare(data.get_data())
        qclient.close()
        qt.mend()
        #Send scan info 2 to Word
        print '-'*24+' Scan finished '+'-'*24
        t_scan = (time()-t_scanstart)/60
        dfname = data.get_filename().replace('.dat','')
        dfname_bwd = '/%s'%data_bwd.get_filename().replace('.dat','') if data_bwd else ''
        _ = ', %s'%RETAKE_TIMES if retakejump else ''
        self._sendToWord('%.1f, %s%s%s<return>'%(t_scan,dfname,dfname_bwd,_),addTimestamp=False)
        #Check user_interrrupt
        if self.user_interrrupt:
            sys.exit()

    def _scan1d(self,xchan,xpnt,y_iy,z_iz,d_item,is_fwd_now,is1d,qclient,retakejump):#y_val0=ypnt[0][iy],z_val0=zpnt[0][iz]
        data_line = []#Data "line" returned by 1d scan
        ix = 0#Index of x setpoints
        try_times = 0 #Trying times of retaking the 1d scan due to charge jumps
        xchan_num = len(xpnt)
        xpnt_num = len(xpnt[0])
        global RETAKE_TIMES, RETAKE_MAX_REACHED
        while ix < xpnt_num:
            #Set x dimension channels
            for i in np.arange(xchan_num):
                g.set_val(xchan[i],xpnt[i,ix])
            #Delay(2) before each readpoint
            qt.msleep(delay2)

            #Get data_point
            data_point = [xpnt[0,ix],y_iy[0],z_iz[0]]+g.take_data()#takes tens of ms
            if xchan_num > 1:
                data_point += xpnt[1:,ix]
            if len(y_iy)>1:
                data_point += y_iy[1:]
            if len(z_iz)>1:
                data_point += z_iz[1:]
            
            #Print to console, update qtplot
            self._print_progress(1.*ix/xpnt_num,data_point,is_fwd_now,try_times)
            if is_fwd_now or is1d:
                qclient.add_data(data_point)
                qclient.update_plot()
            
            #If want to retake data_line when there is a jump, data will be saved to the file after the whole line is taken
            #otherwise data is saved point by point
            if retakejump and try_times < retakejump['max_try_times']:
                data_line.append(data_point)
                r_ind,r_x,r_y = retakejump['index'],retakejump['threshold_x'],retakejump['threshold_y']
                isjump = ix > 0 and abs(data_line[ix][r_ind]-data_line[ix-1][r_ind]) > r_x
                if (not RETAKE_MAX_REACHED) and len(d_item.get_data())>= xpnt_num:
                    isjump = isjump or abs(data_line[ix][r_ind]-d_item.get_data()[-xpnt_num+ix][r_ind]) > r_y
                if isjump:
                    RETAKE_TIMES += 1
                    qclient.counter -= ix+1#Reset qclient counter
                    ix = -1
                    data_line = []
                    try_times += 1
            else:
                d_item.add_data_point(*data_point)
            ix += 1

            #Detect key pressing
            last_key = ''
            while msvcrt.kbhit():
               last_key = msvcrt.getch()
            if last_key == '\x05':#ctrl+e(xit)
                raise KeyboardInterrupt
            elif last_key == '\x0e':#ctrl+n(ext)
                raise UserWarning('next')
        if retakejump:
            for i in data_line:
                d_item.add_data_point(*i)
            RETAKE_MAX_REACHED = try_times >= retakejump['max_try_times']
        d_item.new_block()

    def get_scan_str(self,
            xlbl,xchan,xstart,xend,xsteps,
            ylbl,ychan,ystart,yend,ysteps,
            zlbl,zchan,zstart,zend,zsteps,
            bwd,meander,xshift,retakejump):
        # print2('','scan',True)#set font color
        scan_str = "e.scan(%s,%s,%s,%s,%s, "%(xlbl,xchan,xstart,xend,xsteps) if xsteps or xlbl[0] else ''
        scan_str += "%s,%s,%s,%s,%s, "%(ylbl,ychan,ystart,yend,ysteps) if ysteps or ylbl[0] else ''
        scan_str += "%s,%s,%s,%s,%s, "%(zlbl,zchan,zstart,zend,zsteps) if zsteps or zlbl[0] else ''
        scan_str += "bwd=True, " if bwd else ''
        scan_str += "meander=True, " if meander else ''
        scan_str += "xshift=%s, "%xshift if xshift else ''
        scan_str += "retakejump=%s, "%retakejump if retakejump else ''
        if scan_str[-2:] == ", ":#drop last ', ' away
            scan_str = scan_str[:-2]
        scan_str += '), dly(%s,%s,%s), rt(%s,%s,%s), '%(delay0,delay1,delay2,g.get_rate(xchan[0]),g.get_rate(ychan[0]),g.get_rate(zchan[0]))
        return scan_str
        
    def start_end_to_setpoints(self,lbl,chan,start,end,steps):
        #Check if lbl,chan,start,end are all 0D or all 1D
        if not len(np.shape(lbl))==len(np.shape(chan))==len(np.shape(start))== len(np.shape(end))<2:
            print2('Scan parameter error (1)','red')
            sys.exit()
        #If they are all 0D, make them 1D
        if len(np.shape(lbl))==0:
            lbl=[lbl];chan=[chan];start=[start];end=[end]
        #The length should also be the same
        if not len(lbl)==len(chan)==len(start)==len(end):
            print2('Scan parameter error (2)','red')
            sys.exit()
        #Generate setpoints
        chnum = len(chan)
        pnt = np.zeros((chnum,steps+1))
        for i in np.arange(chnum):
            pnt[i] = np.linspace(start[i],end[i],steps+1)
        return lbl,chan,pnt

    def scan(self,
               xlbl=[''],xchan=['xchannel'],xstart=[0],xend=[0],xsteps=0,
               ylbl=[''],ychan=['ychannel'],ystart=[0],yend=[0],ysteps=0,
               zlbl=[''],zchan=['zchannel'],zstart=[0],zend=[0],zsteps=0,
               bwd=False,meander=False,xshift=None,retakejump=None):
        """
        Each dimension can be a list of channels or a single channel, or empty.
        bwd:
            Bool. If True, there will be two data files. One for sweeping xchannels forward. The other one for sweeping xchannels backward.
        meander:
            Bool. Scan x-y channels with in a meander way.
        xshift:
            None, {'y0':xxx,'slope':xxx} or {'z0':xxx,'slope':xxx}.
            If not none, there must be 'shift' in xlbl[0] to pass parameter checking. 
            Shift x channel setpoints depending on the y (or z) setpoint with a given slope.
        retakejump:
            None or {'index':xxx,'threshold_x':xxx,'threshold_y':xxx,'max_try_times':xxx}.
            Retake a data line if there is a (charge) jump. 
        """
        #Send scan information to Word
        scan_str = self.get_scan_str(
                        xlbl,xchan,xstart,xend,xsteps,
                        ylbl,ychan,ystart,yend,ysteps,
                        zlbl,zchan,zstart,zend,zsteps,
                        bwd,meander,xshift,retakejump)
        self._sendToWord(scan_str)
        
        #Generate setpoints, for _scan()
        xlbl,xchan,xpnt = self.start_end_to_setpoints(xlbl,xchan,xstart,xend,xsteps)
        ylbl,ychan,ypnt = self.start_end_to_setpoints(ylbl,ychan,ystart,yend,ysteps)
        zlbl,zchan,zpnt = self.start_end_to_setpoints(zlbl,zchan,zstart,zend,zsteps)

        self._scan(xlbl,xchan,xpnt,
               ylbl,ychan,ypnt,
               zlbl,zchan,zpnt,bwd,meander,xshift,retakejump)

        print
        winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

    def set(self,chan,val):
        # print2('','set',True)#set font color
        scan_str = "e.set('%s',%s)"%(chan,val)
        if chan == 'ivvi':
            for i in ivvi.get_parameter_names():
                g.set_val(i,val)
        elif chan.endswith('_rate'):
            chan0 = chan[:-5]
            delay = 30
            scan_str += ', %s ms'%delay
            if chan0 == 'ivvi':
                for i in ivvi.get_parameter_names():
                    ivvi.set_parameter_rate(i,val,delay)
            elif g.is_dac_name(chan0):
                    ivvi.set_parameter_rate(chan0,val,delay)
        else:
            g.set_val(chan,val)
        self._sendToWord(scan_str+'<return>')
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
RETAKE_TIMES=0
RETAKE_MAX_REACHED=False
LOGO = '''
%s\033[1;31m  __   ____   ___   __   __ _
%s\033[1;31m /  \ / ___) / __) / _\ (  ( \ 
%s\033[1;33m(  O )\___ \( (__ /    \/    /
%s\033[1;36m \__\)(____/ \___)\_/\_/\_)__)  \033[1;34mfor qtlab\n
'''%(tuple([' '*(TERM_WIDTH/2-17)]*4))
print2(LOGO)
ivvi = qt.instruments.get('ivvi')
delay0  = 0
