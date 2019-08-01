import os, time, struct, urllib2, json
from collections import OrderedDict

class vcl_reader():
    def __init__(self,filename):
        self.f = open(filename,'rb')
    def __del__(self):
        self.f.close()
    def get_newest_data(self):
        '''
        LineSize(bytes) LineNumber Time(secs) PressureM1Condense(Bar) PressureM3Tank(Bar) PressureFPSafety(Bar) Still (mbar) Forepump (mbar) Dewar (mbar) Input Water Temp Output Water Temp Helium Temp Oil Temp Motor Current 4K Head X55749 t(s) 4K Head X55749 T(K) 4K Head X55749 R(Ohm) 4K Plate X55750 t(s) 4K Plate X55750 T(K) 4K Plate X55750 R(Ohm) Still t(s) Still T(K) Still R(Ohm) 100mK Plate t(s) 100mK Plate T(K) 100mK Plate R(Ohm) M/C X55751 t(s) M/C X55751 T(K) M/C X55751 R(Ohm) M/C RuO2 t(s) M/C RuO2 T(K) M/C RuO2 R(Ohm) Mag Top X48230 t(s) Mag Top X48230 T(K) Mag Top X48230 R(Ohm) Mag Bottom X52698 t(s) Mag Bottom X52698 T(K) Mag Bottom X52698 R(Ohm) 70K Head PT100 t(s) 70K Head PT100 T(K) 70K Head PT100 R(Ohm) 70K Plate PT100 t(s) 70K Plate PT100 T(K) 70K Plate PT100 R(Ohm) chan[10] t(s) chan[10] T(K) chan[10] R(Ohm) chan[11] t(s) chan[11] T(K) chan[11] R(Ohm) chan[12] t(s) chan[12] T(K) chan[12] R(Ohm) chan[13] t(s) chan[13] T(K) chan[13] R(Ohm) chan[14] t(s) chan[14] T(K) chan[14] R(Ohm) chan[15] t(s) chan[15] T(K) chan[15] R(Ohm) Still heater (W) chamber heater (W)
        '''
        num = 512
        self.f.seek(-num,2)
        data = struct.unpack('d'*(num/8),self.f.read(num))
        return data

class alarmer():
    def __init__(self):
        self.rules = {"PTout":[44,45,'PT out<44','Alarm! PT out>45',True],"PT_I":[15,20,'Alarm! PT is off','PT is on',True]}#last element is the status, for details see alarm()
        print self.rules
        self.firsttime = True
        self.lastmsg = ''

    def alarm(self,data):
        msg = ''
        status_changed = False
        for i in self.rules:
            if i in data:
                rl = self.rules[i]
                print i,'\t%s\t%s\t%s'%(data[i],rl[0],rl[1]),
                status = rl[4]
                if data[i] > rl[1]:
                    status = True
                    if rl[4] != status:
                        msg += rl[3] + '\n'
                elif data[i] < rl[0]:
                    status = False
                    if rl[4] != status:
                        msg += rl[2] + '\n'
                print '\t+' if status else '\t-'
                if rl[4] != status:
                    rl[4] = status
                    status_changed = True
        if self.firsttime:
            status_changed = False
            self.firsttime = False
        if status_changed:
            self.send(msg)
            self.adjust_volumn_max()
        print self.lastmsg
        if 'Alarm' in msg:
            self.beep()
            
    def send(self,msg):
        if msg:
            msg = '_DR200 status changed_\nAt %s\n%s'%(time.strftime("%d-%m-%Y %H:%M:%S"),msg)
            url = ''
            data = json.dumps({'text':msg})
            req = urllib2.Request(url)
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, data)
            self.lastmsg = '\n----------------\nMessage sent to Slack:\n%s'%msg + '\nSlack response:\n' + response.read()
            
        
        
    def adjust_volumn_max(self):
        pass
    
    def beep(self):
        pass
                 
folder = r''
filename = folder+sorted(os.listdir(folder))[-1]
vr = vcl_reader(filename)
alm = alarmer()
timesleep = 61
try:
    while True:
        os.system('cls')
        print '====================\nDR200 status monitor\n====================\n\npress ctrl + c to exit.\nData are obtained every %s seconds from'%timesleep,
        print filename
        data = vr.get_newest_data()#pulse tube data, in out He oil current
        print "\n%s\n\n#%d\nName\tPV\tA1\tA2\tStatus"%(time.strftime("%Y-%m-%d %H:%M:%S"),data[1])
        ptdata = OrderedDict(zip(['PTin','PTout','PThe','PToil','PT_I'],data[9:14]))
        alm.alarm(ptdata)
        time.sleep(61)
except KeyboardInterrupt:
    pass
os.system('pause')