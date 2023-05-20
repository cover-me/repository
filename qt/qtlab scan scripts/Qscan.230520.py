# A script for scans.
# Project page: https://github.com/cover-me/repository/tree/master/qt/qtlab scan scripts

import qt,timetrack,sys,os,socket,winsound,msvcrt
import IPython.core.interactiveshell as ips
import numpy as np
import data as d
from lib.file_support.spyview import SpyView
from time import time, strftime
from shutil import copyfile, rmtree
from tempfile import mkdtemp
import inspect

# overwrite the method qtlab used for checking data file count.
def _check_last_number2(self, start):
    # 10 ms for 724*3 files, tims is consumed by os.listdir

    def get_max_file_num(folder):
        if not os.path.isdir(folder):
            return 0
        # filename = basename + *_%d.dat
        num_list = [int(i.split('_')[-1][:-4]) for i in os.listdir(folder) if i.endswith('.dat')]
        if num_list:
            return max(num_list)
        else:
            return 0
            
    folder, file_pre = os.path.split(self._basename)# basename = root/cooldown/data/ + file_pre (without '_%d.dat')
    max_num = get_max_file_num(folder)

    if max_num == 0:
        head, tail = os.path.split(folder)# folder = root/cooldown/, tail = data/
        head, tail = os.path.split(head)# head = root, tail = cooldown
        cd_folders = [os.path.join(head,i,'data') for i in os.listdir(head) if i != tail]
        for i in cd_folders:
            max_num = max(max_num, get_max_file_num(i))
    
    # print time() - t0
    return max_num + 1

d.IncrementalGenerator._check_last_number = _check_last_number2

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
                
                nx, ny, nz = len(x_pts[0]), len(y_pts[0]), len(z_pts[0])
                row = nx*ny*nz
                m = np.empty((row,col))*np.nan#data matrix
                
                X = np.tile(x_pts,ny*nz)
                Y = np.tile(np.repeat(y_pts,nx,axis=1),nz)
                Z = np.repeat(z_pts,nx*ny,axis=1)
                W = np.vstack([X,Y,Z])
                m[:,:len(W)] = W.T
                
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
    A class for linear scans up to 3 dimensions, which means, 3 layers of for loops.
    Each dimension of the scan can be a combination of multiple channels, such as ['dac1','dac2','dac3'].
    '''
    def __init__(self):
        self._filename=filename
        self._datapath=datapath if datapath.endswith('\\') else (datapath+'\\')
        self._generator=d.IncrementalGenerator(self._datapath+self._filename,1)#data number generator
        self._vallabels = g.get_vallabels()#value labels, [reading1, reading2, reading3, ..]
        self._coolabels = ['','','']# coordinator labels, coordinators are set values that are not got from instruments.
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
                    xpnt,xchan,ypnt,ychan,zpnt,zchan,bwd=False):
        '''Generate the data file, spyview .meta file (only useful for spyview) and copy scan scripts.'''
        qt.Data.set_filename_generator(self._generator)
        data = qt.Data(name=self._filename)
        
        # set values are also called coordinates, read values are values
        self._coolabels = []

        for i,k,n in zip(xpnt,xchan,range(len(xchan))):
            if k in channels_to_set:
                label = channels_to_set[k][0]
            else:
                label = ''
            coolabel = '%s_(%s)'%(k,label)
            self._coolabels.append(coolabel)
            # only the first set value is added as the coordinate
            # The size information is used when loading the data for qtplot or other programs
            if n==0:
                if bwd:
                    data.add_coordinate(coolabel,size=len(i),start=i[-1],end=i[0])
                else:
                    data.add_coordinate(coolabel,size=len(i),start=i[0],end=i[-1])
            else:
                data.add_value(coolabel)

        for i,k,n in zip(ypnt,ychan,range(len(ychan))):
            if k in channels_to_set:
                label = channels_to_set[k][0]
            else:
                label = ''
            coolabel = '%s_(%s)'%(k,label)
            self._coolabels.append(coolabel)
            if n==0:
                data.add_coordinate(coolabel,size=len(i),start=i[0],end=i[-1])
            else:
                data.add_value(coolabel)
            
        for i,k,n in zip(zpnt,zchan,range(len(zchan))):     
            if k in channels_to_set:
                label = channels_to_set[k][0]
            else:
                label = ''
            coolabel = '%s_(%s)'%(k,label)
            self._coolabels.append(coolabel)
            if n==0:
                data.add_coordinate(coolabel,size=len(i),start=i[0],end=i[-1])
            else:
                data.add_value(coolabel)
        
        # reading values
        for i in self._vallabels:
            data.add_value(i)#add value labels

        data.create_file()#Create data file
        # SpyView(data).write_meta_file()#Create meta.txt file for spyview
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
        
    def _paraok_scan_shape(self,chan,pnt):
        '''Check the dimensions and lengths'''
        return (1==len(np.shape(chan))==(len(np.shape(pnt))-1) and len(chan)==len(pnt))
        
    def _paraok_scan_range(self,chan,pnt):
        '''Check if the set value in range'''
        for j,k in zip(chan,pnt):
            vmin = np.min(k)
            vmax = np.max(k)
            for val in [vmin,vmax]:
                spt = g.get_setpoint(j,val)
                if spt:
                    for instr_name, para_name, sv in spt:
                        if not g.is_in_range(instr_name, para_name, sv):
                            return False
        return True
    
    def _paraok_scan(self,xchan,xpnt,ychan,ypnt,zchan,zpnt):
        '''check whether parameters are OK for self._scan()'''
        for chan,pnt in [[xchan,xpnt],[ychan,ypnt],[zchan,zpnt]]:
            if not self._paraok_scan_shape(chan,pnt):
                print2('_scan(): Parameter shape error','red')
                sys.exit()
            if not self._paraok_scan_range(chan,pnt):
                print2('_scan(): Parameter range error','red')
                sys.exit()            

    def _paraokscan(self,xchan,xstart,xend,ychan,ystart,yend,zchan,zstart,zend):
        '''check whether parameters are OK for self.scan()'''
        isok = True
        # check if all 0d or 1d
        if not len(np.shape(xchan))==len(np.shape(xstart))== len(np.shape(xend))<2:
            isok = False
        if not len(np.shape(ychan))==len(np.shape(ystart))== len(np.shape(yend))<2:
            isok = False
        if not len(np.shape(zchan))==len(np.shape(zstart))== len(np.shape(zend))<2:
            isok = False
        # check length if one dimensional (a vector scan)
        if len(np.shape(xchan))==1 and not len(xchan)==len(xstart)==len(xend):
            isok = False
        if len(np.shape(ychan))==1 and not len(ychan)==len(ystart)==len(yend):
            isok = False
        if len(np.shape(zchan))==1 and not len(zchan)==len(zstart)==len(zend):
            isok = False
        if not isok:
            print2('scan(): Parameter error','red')
            sys.exit()
    def _scan(self,
               xchan=['xchannel'],xpnt=[[0]],
               ychan=['ychannel'],ypnt=[[0]],
               zchan=['zchannel'],zpnt=[[0]],bwd=False):
        self._paraok_scan(xchan,xpnt,ychan,ypnt,zchan,zpnt)#check parameters
        xlen = len(xchan);ylen = len(ychan);zlen = len(zchan)
        xptlen = len(xpnt[0]);yptlen = len(ypnt[0]);zptlen = len(zpnt[0])
        #start
        qt.mstart()
        g.t0 = time()
        t_scanstart = time()
        data = self._create_data(xpnt,xchan,ypnt,ychan,zpnt,zchan)# create data file, spyview metafile, copy script
        data_bwd = self._create_data(xpnt,xchan,ypnt,ychan,zpnt,zchan,bwd) if bwd else None
        data_loop = [data,data_bwd]
        counter = 0#counter for scan
        global STR_TIMEINFO
        STR_TIMEINFO = ''
        numloops = yptlen*zptlen
        dfpath = data.get_filepath()
        qclient = qtplot_client(mmap2npy=True)#only works for 1 and 2d
        qclient.set_file(dfpath,len(self._coolabels)+len(self._vallabels),xpnt,ypnt,zpnt)
        qclient.update_plot()
        dfpath_bwd = data_bwd.get_filepath() if bwd else None
        print 'File:', dfpath, '| %s'%os.path.split(dfpath_bwd)[1] if bwd else ''
        print 'Labels:', self._coolabels + self._vallabels
        print 'Scan: %d lines, %d points per line'%(numloops,xptlen)
        self.user_interrrupt = False
        ############# scan #############
        try:
            # set z channels and initialize y channels
            for iz in np.arange(zptlen):
                g.set_vals(zchan,zpnt[:,iz])
                if delay0>0:
                    g.set_vals(ychan,ypnt[:,0])
                    qt.msleep(delay0)
                # set y channels and initialize x channels
                for iy in np.arange(yptlen):
                    t0 = time()
                    g.set_vals(ychan,ypnt[:,iy])
                    if delay1>0:
                        g.set_vals(xchan,xpnt[:,0])
                        qt.msleep(delay1)

                    # sweep x channels
                    is_fwd_now = True
                    is1d = (numloops==1)
                    t1 = time()
                    for d_item in data_loop:# there may be two sets of data (if bwd=True), one for sweeping forward and the other for sweeping backward
                        if d_item:
                            if is_fwd_now==False and is1d:
                                # if 1d we want to show both forward and backward data
                                print
                                qclient.compare(data.get_data())
                                qclient.close()
                                
                                qclient = qtplot_client(mute=(zptlen!=1),mmap2npy=True)
                                qclient.set_file(dfpath_bwd,len(self._coolabels)+len(self._vallabels),xpnt[:,::-1],ypnt,zpnt)
                                qclient.update_plot()
                    
                            self._scan1d(xchan,xpnt,xptlen,xlen,d_item,is_fwd_now,ypnt[:,iy],zpnt[:,iz],is1d,qclient)
                            is_fwd_now = not is_fwd_now
                    t2 = time()
                    counter += 1
                    STR_TIMEINFO = '%.3f,%.1f'%((t2-t1)/xptlen,(t2-t0)*(numloops-counter)/60)
        ############# end scan #############
        except KeyboardInterrupt:#if one pressed ctrl+c or ctrl+e
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

    def _scan1d(self,xchan,xpnt,xptlen,xlen,d_item,is_fwd_now,y_val,z_val,is1d,qclient):#y_val=ypnt[:,iy],z_val=zpnt[:,iz]
        ix = 0 if is_fwd_now else (xptlen-1)
        index_end = xptlen-1-ix
        while -1 < ix < xptlen:
            g.set_vals(xchan,xpnt[:,ix])
            #delay before each point
            qt.msleep(delay2)
            #get xchan set values
            x_val = xpnt[:,ix]

            #take and log data
            datavalues = list(x_val)+list(y_val)+list(z_val)+g.take_data()#takes tens of ms
            d_item.add_data_point(*datavalues)#takes around 1 ms or less
            self._print_progress(1.*ix/xptlen,datavalues,is_fwd_now)
            if is_fwd_now or is1d:
                qclient.add_data(datavalues)
                qclient.update_plot()

            #change ix
            ix += 1 if is_fwd_now else -1
        d_item.new_block()

    def scan(self,
               xchan=['xchannel'],xstart=[0],xend=[0],xsteps=0,
               ychan=['ychannel'],ystart=[0],yend=[0],ysteps=0,
               zchan=['zchannel'],zstart=[0],zend=[0],zsteps=0,bwd=False):
        '''
        Each dimension can be a list of channels or a single channel, or empty.
        bwd: If True, there will be two data files. One for sweeping xchannels forward. The other one for sweeping xchannels backward.
        '''
        #check parameters
        self._paraokscan(xchan,xstart,xend,ychan,ystart,yend,zchan,zstart,zend)
        if len(np.shape(xchan))==0:# if zero dimensional
            xchan=[xchan];xstart=[xstart];xend=[xend]
        if len(np.shape(ychan))==0:
            ychan=[ychan];ystart=[ystart];yend=[yend]
        if len(np.shape(zchan))==0:
            zchan=[zchan];zstart=[zstart];zend=[zend]

        #send message to word
        print2('Scan.', 'cyan')
        print2(' Exit: ctrl+e. Pause: select any text. For channels without "maxstep", e.g. the field, press ctrl+c (IO errors may occur) then manually reset the target value.\n')
        scanStr = "e.scan(%s,%s,%s,%s, "%(xchan,xstart,xend,xsteps) if xsteps or xchan[0]!='xchannel' else ''
        scanStr += "%s,%s,%s,%s, "%(ychan,ystart,yend,ysteps) if ysteps or ychan[0]!='ychannel' else ''
        scanStr += "%s,%s,%s,%s, "%(zchan,zstart,zend,zsteps) if zsteps or zchan[0]!='zchannel' else ''
        scanStr += "bwd=True, " if bwd else ''
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
            
        self._scan(xchan,xpnt,
               ychan,ypnt,
               zchan,zpnt,bwd)
        print
        winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
        
    def set(self,chan,val):
        print2('Set.', 'cyan')
        print2(' Exit: ctrl+e. Pause: select any text. For channels without "maxstep", e.g. the field, press ctrl+c (IO errors may occur) then manually reset the target value.\n')  
        rate_str = g.get_rate(chan)
        rate_str = ', rate %s'%rate_str if rate_str else ''
        print2('Setting %s to %s%s...\n'%(chan, val, rate_str))
        scanStr = "e.set('%s',%s)%s"%(chan,val,rate_str)
        user_interrrupt = False
        try:
            g.set_vals([chan],[val])
        except KeyboardInterrupt:
            user_interrrupt = True
            print2('Interrupted by user\n','red')
            scanStr += ' (interrupted by user)'
        self._sendToWord(scanStr+'<return>')
        print
        if user_interrrupt:
            sys.exit()

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
    '''
    get readings, set outputs
    '''
    def __init__(self):
        self.t0  = time()
        self._query_list = []
        self.prcss_labels = ['t (s)']
        atomic_read = False

        # Typical value: channels_to_read = [('smu1','val','Ileak(A)'), ('lockin1','XY',['Vxx_X(V)','Vxx_Y(V)']),]
        for instr_name, para_name, label in channels_to_read:
            instr = qt.instruments.get(instr_name)

            if instr is None:
                print2('Instrument %s not exists.'%instr_name,'red')
                sys.exit()
            else:
                p = instr.get_parameters()
                if para_name not in p:
                    print2('Reading channel %s not exists.'%para_name,'red')
                    sys.exit()                    
                else:
                    if 'flag' not in inspect.getargspec(p[para_name]['get_func']).args:
                        # 'flag' is to support non-atomic reading (better than atomic reading)
                        atomic_read = True
          
            if type(label)==list:
                self._query_list.append([instr,para_name,label[0]])
                for i in list(label[1:]):
                    self._query_list.append([None,None,i])
            else:
                self._query_list.append([instr,para_name,label])

            # Clear GPIB, usb buffer, get_all
            print2('Clear buffers\n','cyan')
            insObj = instr._ins
            if hasattr(insObj,'_address'):
                if insObj._address.startswith('GPIB') or insObj._address.startswith('TCPIP'):
                    if hasattr(insObj,'_visainstrument'):
                        print 'visa_clear:\t%s'%instr_name
                        insObj._visainstrument.clear()#clear the buffer
                # elif insObj._address.startswith('USB'):
                    # if hasattr(insObj,'_visainstrument'):
                        # print 'visa_clear:\t%s'%instr_name
                        # insObj._visainstrument.clear()#clear the buffer
            if hasattr(instr,'get_all'):
                print 'get_all:\t', instr_name
                instr.get_all()
                
        if len(channels_to_read)==1:
            self.take_data = self.take_data_atomic
        elif atomic_read:
            print2('Some get_func\'s do not have argument "flag", use atomic read (slower).\n','red')
            self.take_data = self.take_data_atomic
        print

    def _check_last_pressed_key(self):
        last_key = ''
        while msvcrt.kbhit():
           last_key = msvcrt.getch()
        if last_key == '\x05':#ctrl+e(xit)
            raise KeyboardInterrupt

    def take_data_atomic(self):
        '''
        Take data atomically
        '''
        val = []
        for instr, para_name, label in self._query_list:
            if instr is not None:
                ans = instr.get(para_name)
                if type(ans) == list:
                    val += ans
                else:
                    val.append(ans)
        val += self.get_prcss(val)#add processed data
        return val
    
    def take_data(self):
        '''
        Take data non-atomically
        '''
        # flag 0 (default): write command and read respond, 1: write only, 2: read only
        val = []
        for instr, para_name, label in self._query_list:
            if instr is not None:
                instr.get(para_name, flag=1)

        for instr, para_name, label in self._query_list:
            if instr is not None:
                ans = instr.get(para_name, flag=2)
                if type(ans) == list:
                    val += ans
                else:
                    val.append(ans)
        val += self.get_prcss(val)#add processed data
        return val       

    def get_vallabels(self):
        return [i[2] for i in self._query_list] + self.prcss_labels

    def is_dac_name(self,dn):#'dn': dac name
        return len(dn)<6 and dn[0:3]=='dac' and dn[3:5].isdigit() and int(dn[3:5])<=16
        
    def is_in_range(self, instr_name, para_name, sv):
        instr = qt.instruments.get(instr_name)
        if instr:
            para = instr.get_parameters()[para_name]
            if 'minval' in para and sv < para['minval']:
                return False
            if 'maxval' in para and sv > para['maxval']:
                return False
        return True
    
    def do_set(self, setpoint_list):
        '''
        Set a list of channels simultaneously, more efficient than setting one by one (can be further improved)
        input:
            setpoint_list: a list of setpoints. [[instr_name1, para_name1, sv1], ...]
        '''
        delay = 0
        step_list = []
        pv_list = []
        delta_list = [] 
        # parepare for setting channels
        for i in setpoint_list:
            instr_name, para_name, sv = i
            instr = qt.instruments.get(instr_name)
            para = instr.get_parameters()[para_name]
            
            # check validation
            if not self.is_in_range(instr_name, para_name, sv):
                print2('Value out of range: %s, %s, %s\n'%(instr_name, para_name, sv),'red')
                sys.exit()
                
            if 'maxstep' in para:# type 1 channels, like DAC
                pv = para['value']
                if pv is None:
                    pv = instr.get(para_name)
                d = pv - sv
                step_list.append(para['maxstep'])
                pv_list.append(pv)
                delta_list.append(d)
                if delay<para['stepdelay']:
                    delay = para['stepdelay']
            else:# type 2 channels, like magnet, set them here
                step_list.append(0)
                pv_list.append(sv)
                delta_list.append(0)
                self._check_last_pressed_key()
                instr.set(para_name, sv)

        sign_list = [int(i<0)*2-1 for i in delta_list]
        
        # set type 1 channels
        while 1:
            for i in range(len(setpoint_list)):
                if delta_list[i] != 0:
                    instr_name, para_name, sv = setpoint_list[i]
                    instr = qt.instruments.get(instr_name)
                    if abs(delta_list[i])> step_list[i]:
                        pv_list[i] += sign_list[i] * step_list[i]
                        delta_list[i] += sign_list[i] * step_list[i]
                    else:
                        pv_list[i] = sv
                        delta_list[i] = 0
                    self._check_last_pressed_key()
                    instr.set(para_name, pv_list[i])
            if all(d==0 for d in delta_list):# True if delta_list is empty
                break
            else:
                qt.msleep(delay/1000.)
                
    def do_set_atomic(self, setpoint_list):
        '''
        Set a list of channels
        input:
            setpoint_list: a list of setpoints. A setpoint is like [instr_name, para_name, sv]
        '''
        for i in setpoint_list:
            instr_name, para_name, sv = i
            instr = qt.instruments.get(instr_name)
            self._check_last_pressed_key()
            instr.set(para_name,sv)

    def get_setpoint(self,chan,val):
        if chan not in channels_to_set:
            return None
        ch = channels_to_set[chan]
        if type(ch)==list:
            if len(ch)==3 and np.all([type(i)==str for i in ch]):
                # ch = [label, instrument, parameter]
                return [[ch[1],ch[2],val],]
            elif callable(ch[1]):
                # ch = [label, function]
                return ch[1](val)
        return None
        
    def set_vals(self,chan_list,val_list):
        setpoint_list = []
        for i,j in zip(chan_list,val_list):
            items = self.get_setpoint(i,j)
            if items is not None:
                setpoint_list.extend(items)
        if setpoint_list:
            self.do_set(setpoint_list)
        else:
            self._check_last_pressed_key()

    def get_rate(self,chan):
        if chan not in channels_to_set:
            return ''
        ch = channels_to_set[chan]
        if type(ch)==list:
            if len(ch)==3 and np.all([type(i)==str for i in ch]):
                # ch = [label, instrument, parameter]
                params = qt.instruments.get(ch[1]).get_parameters()
                if '%s_rate'%ch[2] in params:
                    return '%s'%qt.instruments.get(ch[1]).get('%s_rate'%ch[2])
                else:
                    maxstep = params[ch[2]]['maxstep'] if 'maxstep' in params[ch[2]] else ''
                    stepdelay = params[ch[2]]['stepdelay'] if 'stepdelay' in params[ch[2]] else ''
                    return '%s/%s'%(maxstep,stepdelay)
        return ''
    
    def get_prcss(self,val):
        p_val = [time()-self.t0]
        return p_val

def get_term_width():#get linewith of the console
    a, b = os.popen('mode con /status').read().split('\n')[4].strip().split(':')
    if a == 'Columns':
        return int(b)
    elif a== '\xc1\xd0':
        return int(b.split(' ')[-1])

def print2(s,style='',hold=False):
    stylelist = {'black':'\033[30m','red':'\033[1;31m','green':'\033[32m','yellow':'\033[33m','blue':'\033[1;34m','magenta':'\033[35m','cyan':'\033[1;36m','white':'\033[37m',
                'reset':'\033[0m','bold':'\033[1m'
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
