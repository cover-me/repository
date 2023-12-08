import os, time, struct, urllib2, json, smtplib, msvcrt
from collections import OrderedDict
from email.mime.text import MIMEText
import config

class vcl_reader():
    def __init__(self,filename):
        self.f = open(filename,'rb')
        self.labels = config.labels

    def __del__(self):
        self.f.close()
        
    def get_newest_data(self):
        num = config.num# number of bytes per row
        self.f.seek(-num,2)# 2 means seeking from the end
        data = struct.unpack('d'*(num/8),self.f.read(num))
        return data

class alarmer():
    def __init__(self):
        self.rules = config.rules
        # print self.rules
        self.firsttime = True
        self.lastmsg = ''
        self.next_snapshot_time = []

    def alarm(self,data):
        msg = ''
        status_changed = False
        for i in self.rules:
            # rl: [0 val_low,1 val_high,2 msg_low,3 msg_high,4 status_init,5 delay_snapshot]
            rl = self.rules[i]
            data_name = i.split(':')[0]
            if data_name in data:
                val = data[data_name]
                status = rl[4]
                if val > rl[1]:
                    status = True
                    if rl[4] != status:
                        msg += rl[3] + '\n'
                elif val < rl[0]:
                    status = False
                    if rl[4] != status:
                        msg += rl[2] + '\n'
                if rl[4] != status:
                    rl[4] = status
                    status_changed = True
                if 'Snapshot' in msg:
                    delay = rl[5]
                    self.next_snapshot_time.append(time.time() + delay)
                self.print_status(i,val,rl,status)

        if self.firsttime:
            status_changed = False
            self.firsttime = False
        if status_changed and msg.strip() != '':
            self.send('%s status changed'%config.fridge_name,msg)
        print self.lastmsg
        if 'Alarm' in msg:
            self.beep()
    
    def print_status(self,rule_name,val,rule,status):
        val_low, val_high, msg_low, msg_high, status_init = rule[:5]
        if msg_low == '':
            val_low = '-'
        if msg_high == '':
            val_high = '-'

        if (status==False and 'Alarm' in msg_low) or (status==True and 'Alarm' in msg_high):
            status_string = 'Alarm!!!'
        elif 'Alarm' in msg_low or 'Alarm' in msg_high:
            status_string = '\t--->' if status else '\t<---'
        else:
            status_string = '\t->' if status else '\t<-'

        print '%-20s\t%-15s\t%s\t%s'%(rule_name,val,val_low,val_high),
        print status_string,
        print '\t%d%d-%d%d\n'%('Alarm' in msg_low,'Alarm' in msg_high,'Snapshot' in msg_low,'Snapshot' in msg_high),

    def snap_shot(self,data,force=False):
        if force:
            msg = '\n'.join(['%s: %s'%(i,data[i]) for i in config.snapshot_list])
            self.send('%s snapshot [sent by someone manually]'%config.fridge_name,msg)
        else:
            t = time.time()
            if any([t >= i for i in self.next_snapshot_time]):
                msg = '\n'.join(['%s: %s'%(i,data[i]) for i in config.snapshot_list])
                self.send('%s snapshot'%config.fridge_name,msg)
                self.next_snapshot_time = [i for i in self.next_snapshot_time if t < i]

    def send_slack(self,title,msg):
        if msg:
            msg = '_%s_\n%s\n%s'%(title,time.strftime("%Y-%m-%d %H:%M:%S"),msg)
            url = config.url
            data = json.dumps({'text':msg})
            req = urllib2.Request(url)
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, data)
            self.lastmsg = '\n----------------\nMessage sent to Slack:\n%s'%msg + '\nResponse:\n' + response.read()

    def send_wechat(self,title,msg):
        if msg:
            title_color = 'warning' if 'Alarm' in msg else 'comment'
            msg = '<font color="%s">**%s**</font>\n%s\n%s'%(title_color,title,time.strftime("%Y-%m-%d %H:%M:%S"),msg)
            url = config.url
            data = json.dumps({"msgtype":"markdown","markdown":{"content":msg}})
            req = urllib2.Request(url)
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, data)
            self.lastmsg = '\n----------------\nMessage sent to Qi-Ye-Wei-Xin:\n%s'%msg + '\nResponse:\n' + response.read()

    def send_email(self,title,msg):
        if msg:
            msg = '%s\n%s\n%s'%(title,time.strftime("%Y-%m-%d %H:%M:%S"),msg)
            recipients = config.recipients
            email = config.email
            password = config.password
            host = config.host
            port = config.port

            body = MIMEText(msg)
            body['Subject'] = title
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
    
    def send(self,title,msg):
        if config.method == 'wechat':
            self.send_wechat(title,msg)        
        elif config.method == 'slack':
            self.send_slack(title,msg)
        elif config.method == 'email':
            self.send_email(title,msg)
        
    def adjust_volume_to_max(self):
        pass
    
    def beep(self):
        pass
        
    def _check_last_pressed_key(self,data):
        last_key = ''
        while msvcrt.kbhit():
           last_key = msvcrt.getch()
        if last_key == '\x14':#ctrl+t(est)
            print 'Sending the test message...'
            self.send('%s [Test]'%config.fridge_name,'This is a test message sent by a user manually :-p. The status did not change.')
            print 'Sent.'
        if last_key == '\x10':#ctrl+sna(p)shot
            print 'Sending the snapshot...'
            self.snap_shot(data,force=True)
            print 'Sent.'
        elif last_key == '\x05':#ctrl+e(xit)
            raise KeyboardInterrupt

folder = config.folder

alm = alarmer()
timesleep = 61
last_line_number = -1
num_files_opened = 0
try:
    while True:
        os.system('cls')
        print '====================\n%s status monitor\n====================\n\npress ctrl + e to exit, ctrl + p to send a snapshot of the fridge status, ctrl + t to send a test message. Flag: Whether "Alarm" in message1/2, whether "Snapshot" in message1/2.\nData is fetched every %s seconds from'%(config.fridge_name,timesleep),
        
        if last_line_number < 0:
            filename = folder+sorted(os.listdir(folder))[-1]
            vr = vcl_reader(filename)
            num_files_opened += 1

        print '%s. Counter: %s.'%(filename, num_files_opened)
        data = vr.get_newest_data()
        line_number = data[1]
        if last_line_number == line_number:
            last_line_number = -1
            next
        else:
            last_line_number = line_number
        print "\n%s\n\n#%d\n%-20s\t%-10s\t%s\t%s\t%s\t%s"%(time.strftime("%Y-%m-%d %H:%M:%S"),line_number,'Name','PV','A1','A2','Status','Flag')# data[1] is the current line number
        ptdata = OrderedDict(zip(vr.labels,data))
        alm.alarm(ptdata)
        alm.snap_shot(ptdata)
        for i in range(timesleep):
            alm._check_last_pressed_key(ptdata)
            time.sleep(1)

except KeyboardInterrupt:
    pass
# print "\nNow you can close the window."
# os.system('pause')
