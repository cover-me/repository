#200311
import os,re
import numpy as np
class transMatrix():#calculate traslation 3d matrix for image alignment
    def __init__(self,p11,p_markers,suffix,period):
        self.p11 = p11#center position of area 1.11,2.11,3.11,4.11
        self.p_markers = p_markers#relative position of markers to the area center.
        self.suffix = suffix#suffix of .tif names. for example, 'a' for 1.11a.tif
        self.prd = period#period of repeated patterns in um
    def toLandmarks(self,lmStr):
        '''convert landmark string to sorted landmark coords'''
        lmList = map(float,lmStr.replace('[','').replace(']','').split(','))
        if len(lmList) != 8:
            print 'Warning! Numbers of landmarks should be 4!'
        lmList = np.resize(lmList,(4,2))
        # sort lmList to left-top (LT), RT, LB, RB
        lmList = lmList[np.argsort(-lmList[:, 1])]
        if lmList[0,0]>lmList[1,0]:
            lmList[0:2] = lmList[1::-1]#reverse the order
        if lmList[2,0]>lmList[3,0]:
            lmList[2:4] = lmList[:1:-1]#reverse the order
        return lmList
    def toGdsMNCenter(self,tifName):
        '''calculate center position of an area by .tif file names'''
        pInt = [int(tifName[i])-1 for i in [0,2,3]] # 'm.nl' -> [m-1,n-1,l-1]
        p = np.array(self.p11[pInt[0]])+np.array([0,self.prd[0]])*pInt[1]+np.array([self.prd[1],0])*pInt[2] # center positon of mn.l
        return p
    def toGdsMarks(self,tifName):
        '''return four sorted cross marker positions by .tif name'''
        p = self.toGdsMNCenter(tifName)
        return p + self.p_markers
    def to100umWA(self,tifName):#100 um working area
        x,y = self.toGdsMNCenter(tifName)
        return [x-50,y-50,x+50,y+50]
    def _toTransMatrix(self,marks):# modified from Zhaoen's PKout
        '''marker: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]], calculate trans matrix for this marker'''
        m = np.ones([4,3])# 3d mark positions [[x1,y1,1],[x2,y2,2],...]
        m[:,0:2] = marks
        M = np.matrix(m[:3,:]).T#[[x1,x2,x3],[y1,y2,y3],[1,1,1]], now M*(1,0,0)=p1 (frist point),M*(0,1,0)=p2 ,M*(0,0,1)=p3
        V_p4 = m[3]#[x4,y4,1]
        V = M.I.dot(V_p4)#so that M*V = V_p4
        A = M*np.matrix(np.diagflat(V))#now we have A*[1,1,1] = V_p4, and lines A*[100],[010],[001] intersect with plane [001] at p1,p2,p3, A is the transform Matrix for ldMarks
        return A
    def toMatrix(self,ldMarks,gdsMarks):# modified from Zhaoen's PKout
        '''calculate trans matrix'''
        A = self._toTransMatrix(ldMarks)
        B = self._toTransMatrix(gdsMarks)
        return np.array(B*(A.I))
    def updateMatrix(self,lysFilePath,newName=True):
        '''update the lys file with new matrix'''
        if lysFilePath.endswith('.lys') and os.path.exists(lysFilePath):
            f = open(lysFilePath,'r')
            newlines = []
            for i in f:
                newlines.append(i)
                if i.strip().startswith("<annotations>"):
                    break
            for i in f:
                m = None
                if self.suffix+".tif" in i:
                    m = re.search(".*(matrix=[^;]*).*landmarks=([^;]*).*([\d._]{4})"+self.suffix+"\.tif",i)
                if m:
                    print "Update matrix for " + m.group(3) + self.suffix + ".tif"
                    ldMarks = self.toLandmarks(m.group(2))#land markers
                    gdsMarks = self.toGdsMarks(m.group(3))#ideal markers in gds files
                    mtx =  self.toMatrix(ldMarks,gdsMarks)# matrix for .lys file
                    s = 'matrix='+np.array2string(mtx,separator=',')[1:-1].replace(',\n','').replace('[','(').replace(']',')').replace(' ','')
                    newlines.append(i.replace(m.group(1),s))
                else:
                    newlines.append(i)
            f.close()
            fNewPath = lysFilePath.replace('.lys','_mtx.lys') if newName else lysFilePath
            f = open(fNewPath,'w')
            f.writelines(newlines)
            f.close()
            print 'Matrix updated to %s.'%fNewPath
        else:
            print 'Update matrix error! "%s" is not a .lys file or file not exists.'%lysFilePath

class imgMarkers():#find markers on images
    def __init__(self,ptn,suffix,addLandMarker=False):
        period = ptn[3] if len(ptn)>3 else [-100,100]
        self.tm = transMatrix(ptn[1],ptn[2],suffix,period)
        self.addLandMarker = addLandMarker
        if addLandMarker:
            global plt,mpimg,filters,measure,canny,morphology,hough_line,convolve2d,ndi,median
            import matplotlib.pyplot as plt
            import matplotlib.image as mpimg
            from skimage import filters,measure
            from skimage.feature import canny
            from skimage import morphology
            from skimage.transform import hough_line
            from scipy.signal import convolve2d
            from scipy import ndimage as ndi
            from skimage.filters.rank import median
    def open(self,imgpath):
        '''update self.img'''
        self.img = mpimg.imread(imgpath)[:,:,0]#r,g,b are the same in these files
    def filter1(self):
        '''transform self.img to binary, method 1'''
        img = self.img
        img = ndi.gaussian_filter(img,img.shape[1]/2048.)
        bins = 20
        hist,bin_edges = np.histogram(img,bins)
        hist_thresh = np.size(img)/bins*2
        thresh = 127
        for i in range(10):
            temp = np.nonzero(hist>hist_thresh)[0]
            if len(temp):
                thresh = bin_edges[temp[-1]+1]
                break
            else:
                hist_thresh = hist_thresh/2
        print 'binary threshold: %d,'%thresh,
        img = img > thresh
        img = img*1 #bool to int
        A = convolve2d(img,[[1,1,1],[1,0,1],[1,1,1]],'same')
        img[A>4] = 1
        img = img>0.5 #int to bool
        img = morphology.remove_small_objects(img, np.size(img)/7000)
        self.img = img
    def filter2(self):
        '''transform self.img to binary, method 2'''
        img = self.img
        img = canny(img, sigma=1.5)
        img = ndi.binary_fill_holes(img)
        img = morphology.remove_small_objects(img, 50)
        self.img = img
    # def _getCrossCenter(self,x0,dx,x,y):
        # h0 = 0
        # x0 = x0+dx
        # for i in range(10):
            # temp = y[np.where(abs(x-x0)<1.5)]
            # if len(temp)>1:
                # h1 = (temp.max()+temp.min())/2.
                # if abs(h1-h0)<3.:
                    # h0 = (h1+h0)/2.
                    # return h0
                # h0 = h1
            # x0 = x0+dx  
    # def getCrossCenter(self,contour):
        # '''contours=[[y1,x1],[y2,x2],....]'''
        # y,x = np.transpose(contour)
        # h_left = self._getCrossCenter(x.min(),5,x,y)
        # h_right = self._getCrossCenter(x.max(),-5,x,y)
        # w_top = self._getCrossCenter(y.max(),-5,y,x)
        # w_bottom = self._getCrossCenter(y.min(),5,y,x)
        # if all((h_left,h_right,w_top,w_bottom)):
            # return ((w_top+w_bottom)/2.,(h_left+h_right)/2.)
    def _removeLonelyDots(self,a):
        n = convolve2d(a,[[1,1,1],[1,0,1],[1,1,1]],'same')
        a[n<3] = 0
        n1 = convolve2d(a,[[1,0,1],[0,0,0],[1,0,1]],'same')
        n = convolve2d(a,[[1,1,1],[1,0,1],[1,1,1]],'same')
        a[(n<3)|(n==3)&(n1!=1)] =0
        return a        
    def getCrossCenters(self,plotResults=False):
        '''find cross centers from binarized self.img'''
        img = self.img
        img = morphology.skeletonize(img)#transform to skeleton
        areas = measure.regionprops(measure.label(img,connectivity=2))
        centers=[]#all object centers
        for i in range(len(areas)):
            m1,n1,m2,n2 = areas[i].bbox
            img[m1:m2,n1:n2]=self._removeLonelyDots(img[m1:m2,n1:n2])
            if np.any(img[m1:m2,n1:n2]):
                c = ndi.measurements.center_of_mass(img[m1:m2,n1:n2])
                centers.append(np.array(c)+[m1,n1])
        if plotResults:
            plt.imshow(np.ma.masked_where(img==0, img))#show the skeleton
        M,N = [i/2. for i in img.shape]
        cc = {}#four cross centers
        for i in centers:
            loc = 'l' if i[1]<N else 'r'
            loc += 't' if i[0]<M else 'b'
            if (loc not in cc) or np.linalg.norm(i-[M,N])>np.linalg.norm(cc[loc]-[M,N]):
                cc[loc] = i
        if plotResults:
            for i in cc:
                plt.plot(cc[i][1],cc[i][0],'co')
        return cc
    def plotContours(self):
        img = self.img
        contours = measure.find_contours(img, 0.5, fully_connected="high")
        #contours = [measure.approximate_polygon(c, tolerance=1) for c in contours]
        for c in contours:
            plt.plot(c[:, 1], c[:, 0], linewidth=1,color='magenta')
            #center = getCrossCenter(c)
            #if center:
                #plt.plot(center[0],center[1],'bo')
        img = ndi.binary_fill_holes(img)
        self.img = img
    def updateLys(self,lysFilePath):
        '''Update .tif annotations to lys, if suffix is empty, old annotations will be removed.'''
        addLandMarker = self.addLandMarker
        if lysFilePath.endswith('.lys') and os.path.exists(lysFilePath):
            f = open(lysFilePath,'r')
            lines = f.readlines()
            f.close()
            newlines = []
            parseerror = True
            for i in lines:
                if self.tm.suffix:
                    if i.strip().startswith('</annotations>'):
                        parseerror = False
                        break
                    newlines.append(i)
                else:
                    newlines.append(i)
                    if i.strip()=='<annotations>':
                        parseerror = False
                        break
            if parseerror:
                print 'Parse .lys file error.'
                return ''
            fns = [i for i in os.listdir(os.getcwd()) if i.endswith(self.tm.suffix+'.tif') and len(i)==8+len(self.tm.suffix)]#file names
            k = 0
            kk = 0
            for i in fns:
                lmstr = ''
                print '%s imported.'%i
                if addLandMarker:
                    self.open(i)
                    print 'Searching for cross markers...',
                    self.filter1()
                    cc = self.getCrossCenters()
                    imy, imx = [(temp0558-1)/2. for temp0558 in self.img.shape]
                    if len(cc) == 4:
                        kk += 1
                        lm = [np.array(cc[temp0558])[::-1]*[1,-1]+[-imx,imy] for temp0558 in ['lt','rt','lb','rb']]#landmarks
                        lmstr = 'landmarks=%s;'%np.array2string(np.ndarray.flatten(np.array(lm)),separator=',')
                        print 'Successed!\n'
                    else:
                        print ' Failed (only find %d cross markers)'%len(cc)
                mtx = self.tm.toGdsMNCenter(i)
                newlines.append('''<annotation>
<class>img::Object</class>
<value>color:matrix=(0.05,0,%s)(0,0.05,%s)(0,0,1);min_value=0;max_value=255;is_visible=true;z_position=1;brightness=0;contrast=0;gamma=1;red_gain=1;green_gain=1;blue_gain=1;%scolor_mapping=[0,'#000000';1,'#ffffff';];file='%s'</value>
</annotation>'''%(mtx[0],mtx[1],lmstr,i))
                k = k+1
            newlines.append('</annotations></view></session>')
            if addLandMarker:
                lysFilePath = lysFilePath.replace('.lys','_tifsmart.lys')
            else:
                lysFilePath = lysFilePath.replace('.lys','_tif.lys')
            f = open(lysFilePath,'w')
            f.writelines(newlines)
            f.close()
            if self.tm.suffix:
                tempstr = 'Old .tif annotations was included as suffix is not empty.'
            else:
                tempstr = 'Old .tif annotations was not included since suffix = "".'
            print '\n%d files have been imported to %s. %d of them have landmarkers. %s'%(k,lysFilePath,kk,tempstr)
            return lysFilePath
        else:
            print 'Import .tif error! "%s" is not a .lys file or file not exists.'%lysFilePath
    def test(self,plotResults=True):
        if plotResults:
            plt.imshow(self.img,cmap=plt.cm.gray)
        self.filter1()
        self.plotContours()
        print '\nlocation of centers:', self.getCrossCenters(plotResults)
        if plotResults:
            plt.show()

def choose_pattern(k=-1):
    patterns = [('Global backgate, cross markers',[[1050,2550],[1750,2450],[950,1850],[1650,1750]],[[-7.976,7.976],[8.024,7.976],[-7.976,-8.024],[8.024,-8.024]]),
            ('Grenoble 60 nm, crosses markers',[[1050,2550],[1750,2450],[950,1850],[1650,1750]],[[1020.25-1050,2579.75-2550],[1079.75-1050,2579.75-2550],[1020.25-1050,2520.25-2550],[1079.75-1050,2520.25-2550]]),
            ('Grenoble 60 nm, gate corners',[[1050,2550],[1750,2450],[950,1850],[1650,1750]],[[1231.87200-1250,2463.78200-2450],[1268.12800-1250,2463.72000-2450],[1231.87600-1250,2436.28100-2450],[1268.12400-1250,2436.21900-2450]]),
            ('Grenoble 60 nm, gate joint',[[1050,2550],[1750,2450],[950,1850],[1650,1750]],[[1046.375-1050,2552.904-2550],[1053.625-1050,2552.843-2550],[1046.370-1050,2547.145-2550],[1053.625-1050,2547.085-2550]]),
            ('BG1-3_60nm_1905, outer crosses',[[5050,5850]],[[5015.05-5050,5885-5850],[5085.05-5050,5885-5850],[5015.05-5050,5815-5850],[5085.05-5050,5815-5850]],[-200,200]),
            ('BG1-3_60nm_1905, gate corners',[[5050,5850]],[[5033.58900-5050,5862.16700-5850],[5066.41900-5050,5862.22700-5850],[5033.58900-5050,5838.16700-5850],[5066.41900-5050,5838.22700-5850]],[-200,200]),
            ('BG1-3_60nm_1905, gate joint',[[5050,5850]],[[5044.22400-5050,5851.60700-5850],[5055.78400-5050,5851.66700-5850],[5044.22400-5050,5848.72700-5850],[5055.78400-5050,5848.78700-5850]],[-200,200]),
            ]
    if k in range(len(patterns)):
        return patterns[k]
    for k in range(len(patterns)):
        print "%03d\t"%(k)+patterns[k][0].replace(',','\t')
    k = -1
    while k<0 or k>len(patterns)-1:
        k = input("Choose your pattern: ")
    print
    return patterns[k]

def choose_suffix(s=''):
    s = raw_input("Suffix for file names: ")
    print "Your .tif files' names: m.nl%s.tif"%s
    print
    return s

def choose_path(s=''):
    while not os.path.isdir(s) or (os.path.isfile('sample.lys')):
        s = raw_input("where is your folder containing sample.lys: ")
    print
    return s
