import os, time, struct, urllib2, json, smtplib, msvcrt
from collections import OrderedDict
from email.mime.text import MIMEText

class vcl_reader():
    def __init__(self,filename):
        self.f = open(filename,'rb')

        # To find labels, open a VCL file and search for "This is the standard comments block", keep replacing NUL NUL (\0) with NUL, then replace NUL with ', '  
        # DR200 LineSize(bytes) LineNumber Time(secs) PressureM1Condense(Bar) PressureM3Tank(Bar) PressureFPSafety(Bar) Still (mbar) Forepump (mbar) Dewar (mbar) Input Water Temp Output Water Temp Helium Temp Oil Temp Motor Current 4K Head X55749 t(s) 4K Head X55749 T(K) 4K Head X55749 R(Ohm) 4K Plate X55750 t(s) 4K Plate X55750 T(K) 4K Plate X55750 R(Ohm) Still t(s) Still T(K) Still R(Ohm) 100mK Plate t(s) 100mK Plate T(K) 100mK Plate R(Ohm) M/C X55751 t(s) M/C X55751 T(K) M/C X55751 R(Ohm) M/C RuO2 t(s) M/C RuO2 T(K) M/C RuO2 R(Ohm) Mag Top X48230 t(s) Mag Top X48230 T(K) Mag Top X48230 R(Ohm) Mag Bottom X52698 t(s) Mag Bottom X52698 T(K) Mag Bottom X52698 R(Ohm) 70K Head PT100 t(s) 70K Head PT100 T(K) 70K Head PT100 R(Ohm) 70K Plate PT100 t(s) 70K Plate PT100 T(K) 70K Plate PT100 R(Ohm) chan[10] t(s) chan[10] T(K) chan[10] R(Ohm) chan[11] t(s) chan[11] T(K) chan[11] R(Ohm) chan[12] t(s) chan[12] T(K) chan[12] R(Ohm) chan[13] t(s) chan[13] T(K) chan[13] R(Ohm) chan[14] t(s) chan[14] T(K) chan[14] R(Ohm) chan[15] t(s) chan[15] T(K) chan[15] R(Ohm) Still heater (W) chamber heater (W)
        # Triton 'LineSize(bytes), LineNumber, Time(secs), P2 Condense (Bar), P1 Tank (Bar), P5 ForepumpBack (Bar), P3 Still (mbar), P4 TurboBack (mbar), Dewar (mbar), Input Water Temp, Output Water Temp, Helium Temp, Oil Temp, Motor Current, PT1 Plate t(s), PT1 Plate T(K), PT1 Plate R(Ohm), PT2 Plate t(s), PT2 Plate T(K), PT2 Plate R(Ohm), Still t(s), Still T(K), Still R(Ohm), 100mK Plate t(s), 100mK Plate T(K), 100mK Plate R(Ohm), MC RuO2 t(s), MC RuO2 T(K), MC RuO2 R(Ohm), MC cernox t(s), MC cernox T(K), MC cernox R(Ohm), chan[6] t(s), chan[6] T(K), chan[6] R(Ohm), chan[7] t(s), chan[7] T(K), chan[7] R(Ohm), chan[8] t(s), chan[8] T(K), chan[8] R(Ohm), chan[9] t(s), chan[9] T(K), chan[9] R(Ohm), chan[10] t(s), chan[10] T(K), chan[10] R(Ohm), chan[11] t(s), chan[11] T(K), chan[11] R(Ohm), Magnet t(s), Magnet T(K), Magnet R(Ohm), Still heater (W), chamber heater (W), IVC sorb heater (W), turbo current(A), turbo power(W), turbo speed(Hz), turbo motor(C), turbo bottom(C)'.split(', ')   
        # Triton_XL, there are two Input/Output Water Temps (this model has two PTs), made the seconds to Input/Onput Water Temp2
        self.labels = ['LineSize(bytes)', 'LineNumber', 'Time(secs)', 'P2 Condense (Bar)', 'P1 Tank (Bar)', 'P5 ForepumpBack (Bar)', 'P3 Still (mBar)', 'P4 TurboBack (mBar)', 'Dewar (mBar)', 'Input Water Temp', 'Output Water Temp', 'Oil Temp', 'Helium Temp', 'Motor Current', 'Low Pressure', 'High Pressure', 'PT2 Head T(K)', 'PT2 Head R(Ohm)', 'PT2 Plate T(K)', 'PT2 Plate R(Ohm)', 'Still Plate T(K)', 'Still Plate R(Ohm)', 'Cold Plate T(K)', 'Cold Plate R(Ohm)', 'MC Plate Cernox old T(K)', 'MC Plate Cernox old R(Ohm)', 'PT1 Head old T(K)', 'PT1 Head old R(Ohm)', 'PT1 Plate old T(K)', 'PT1 Plate old R(Ohm)', 'MC Plate RuO2 old T(K)', 'MC Plate RuO2 old R(Ohm)', 'MC Plate Cernox T(K)', 'MC Plate Cernox R(Ohm)', 'PT1 Head  T(K)', 'PT1 Head  R(Ohm)', 'PT1 Plate T(K)', 'PT1 Plate R(Ohm)', 'MC Plate RuO2 T(K)', 'MC Plate RuO2 R(Ohm)', 'Magnet T(K)', 'Magnet R(Ohm)', 'Still heater (W)', 'chamber heater (W)', 'IVC sorb heater (W)', 'Input Water Temp2', 'Output Water Temp2', 'Oil Temp2', 'Helium Temp2', 'Motor Current2', 'Low Pressure2', 'High Pressure2', 'turbo current(A)', 'turbo power(W)', 'turbo speed(Hz)', 'turbo motor(C)', 'turbo bottom(C)']

    def __del__(self):
        self.f.close()
        
    def get_newest_data(self):
        num = 456# dr200:512, triton:488, tritonXL:456 (see logging -> log file information for the file-size change)
        self.f.seek(-num,2)# 2 means seeking from the end
        data = struct.unpack('d'*(num/8),self.f.read(num))
        return data

class alarmer():
    def __init__(self):
        self.rules = OrderedDict([
                        ("Output Water Temp",[32,34,'PT1 out<31','Alarm! PT1 out>33',True]),
                        ("Output Water Temp2",[29,31,'PT2 out<28','Alarm! PT2 out>30',True]),
                        ("Motor Current",[10,15,'Alarm! PT1 is off','PT1 is on',True]),
                        ("Motor Current2",[10,15,'Alarm! PT2 is off','PT2 is on',True]),
                        # ("P2 Condense (Bar)",[5,6,'P2 Condense<5','P2 Condense>6',True]),
                        ("Cold Plate T(K)",[5,10,'Cold plate<5 K','Cold plate>10 K',True]),
                        ])# the last element is status, see alarm()
        print self.rules
        self.firsttime = True
        self.lastmsg = ''

    def alarm(self,data):
        msg = ''
        status_changed = False
        for i in self.rules:
            if i in data:
                rl = self.rules[i]
                print '%-20s\t%-10s\t%s\t%s'%(i,data[i],rl[0],rl[1]),
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
            
    def send_slack(self,msg,test):
        if msg:
            msg = '_DR200 status changed_\nAt %s\n%s'%(time.strftime("%Y-%m-%d %H:%M:%S"),msg)
            url = ''
            data = json.dumps({'text':msg})
            req = urllib2.Request(url)
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, data)
            self.lastmsg = '\n----------------\nMessage sent to Slack:\n%s'%msg + '\nSlack response:\n' + response.read()

    def send_wechat(self,msg,test):
        if msg:
            title_color = 'warning' if 'Alarm' in msg else 'comment'
            msg = '<font color="%s">**Triton XL status changed**</font>\n%s\n%s'%(title_color,time.strftime("%Y-%m-%d %H:%M:%S"),msg)
            url = ''
            data = json.dumps({"msgtype":"markdown","markdown":{"content":msg}})
            req = urllib2.Request(url)
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, data)
            self.lastmsg = '\n----------------\nMessage sent to Slack:\n%s'%msg + '\nSlack response:\n' + response.read()

    def send_email(self,msg,test):
        if msg:
            msg = 'Top-loading fridge update\nAt %s\n%s'%(time.strftime("%Y-%m-%d %H:%M:%S"),msg)
            if test:
                msg = 'This is a test email from top-loading fridge messenger. It is sent to check if the program is running well. \n%s'%time.strftime("%Y-%m-%d %H:%M:%S")
            
            recipients = ['r1@gmail.com','r2@outlook.com']
            email = 'youremail@mail.com'
            password = 'yourpassword'
            host = "smtp.xxx.com"
            port = '123'

            body = MIMEText(msg)
            body['Subject'] = 'Top-loading fridge update'
            if test:
                body['Subject'] = '[Test email] ' + body['Subject']
            body['From'] = email
            body['To'] = ", ".join(recipients)

            s = smtplib.SMTP(host,port)
            s.ehlo()
            # s.starttls()
            # s.ehlo()
            s.login(email,password)
            s.sendmail(email,recipients,body.as_string())
            s.quit()
            
            self.lastmsg = '\n----------------\nMessage sent to %s:\n%s'%(body['To'],msg)
    
    def send(self,msg,test=False):
        self.send_wechat(msg,test)
        
    def adjust_volumn_max(self):
        pass
    
    def beep(self):
        pass
        
    def _check_last_pressed_key(self):
        last_key = ''
        while msvcrt.kbhit():
           last_key = msvcrt.getch()
        if last_key == '\x14':#ctrl+t(est)
            print 'Sending the test message...'
            self.send('This is a test message sent by a user manually :-p. The status did not change.',test=True)
            print 'Sent.'
        elif last_key == '\x05':#ctrl+e(xit)
            raise KeyboardInterrupt
            
folder = 'data\\'
filename = folder+sorted(os.listdir(folder))[-1]
vr = vcl_reader(filename)
alm = alarmer()
timesleep = 61
try:
    while True:
        os.system('cls')
        print '====================\nTriton status monitor\n====================\n\npress ctrl + e to exit. ctrl + t to send a test message. \nData is fetched every %s seconds from'%timesleep,
        print filename
        data = vr.get_newest_data()
        print "\n%s\n\n#%d\n%-20s\t%-10s\t%s\t%s\t%s"%(time.strftime("%Y-%m-%d %H:%M:%S"),data[1],'Name','PV','A1','A2','Status')# data[1] is the current line number
        ptdata = OrderedDict(zip(vr.labels,data))
        alm.alarm(ptdata)
        for i in range(timesleep):
            alm._check_last_pressed_key()
            time.sleep(1)

except KeyboardInterrupt:
    pass
# print "\nNow you can close the window."
# os.system('pause')
