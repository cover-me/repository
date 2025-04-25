import os, time, struct, urllib2, json, smtplib, msvcrt, datetime, config, zlib
from collections import OrderedDict
from email.mime.text import MIMEText
import xml.etree.ElementTree as ET

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
        if data[0]==num and data[1]>0:
            return data
        else:
            return [-1,-1]
        
class dat_reader_ppms():
    def __init__(self,filename):
        self.f = open(filename,'r')
        self.labels = config.labels

    def __del__(self):
        self.f.close()
        
    def get_newest_data(self):
        newline = self.f.readline().strip()
        while newline:
            lastline = newline
            newline = self.f.readline().strip()
        try: 
            data = [float(i) if i else float("nan") for i in lastline.strip().split(',')]
        except:
            return [-1,-1]
        return data
  
class dat_reader_xls():
    def __init__(self,filename):
        self.f = open(filename,'r')
        self.labels = config.labels

    def __del__(self):
        self.f.close()
        
    def get_newest_data(self):
        newline = self.f.readline().strip()
        while newline:
            lastline = newline
            newline = self.f.readline().strip()
        try: 
            data = [float(i) if i else float("nan") for i in lastline.strip().split(',')]
        except:
            return [-1,-1]
        return data

class xlsx_reader_xs():
    def __init__(self,file_path):
        self.last_timestamp = -1
        self.file_path = file_path
        self.labels = config.labels

    # def __del__(self):
        # pass
        
    def read_file_in_zip(self, zip_file_path, target_file_path):
        with open(zip_file_path, 'rb') as zip_file:
            zip_data = zip_file.read()
        local_file_header_signature = '\x50\x4b\x03\x04'
        central_directory_signature = '\x50\x4b\x01\x02'
        offset = 0
        while True:
            local_header_index = zip_data.find(local_file_header_signature, offset)
            if local_header_index == -1:
                break
            if central_directory_signature in zip_data[local_header_index:local_header_index + 10]:
                break
            file_name_length = struct.unpack('<H', zip_data[local_header_index + 26:local_header_index + 28])[0]
            extra_field_length = struct.unpack('<H', zip_data[local_header_index + 28:local_header_index + 30])[0]
            file_name = zip_data[local_header_index + 30:local_header_index + 30 + file_name_length]
            if file_name == target_file_path:
                data_start = local_header_index + 30 + file_name_length + extra_field_length
                next_local_header = zip_data.find(local_file_header_signature, data_start)
                if next_local_header == -1:
                    data_end = len(zip_data)
                else:
                    data_end = next_local_header
                file_data = zip_data[data_start:data_end]
                return zlib.decompress(file_data,-15)
            offset = local_header_index + 1

        print "File not found"
        return None
    
    def extract_last_row_data(self, xml_str):
        if not xml_str:
            return [-1, -1]
        root = ET.fromstring(xml_str)
        prefix = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
        sheetdata = root.find(prefix+'sheetData')
        row_elements = sheetdata.findall(prefix+'row')
        
        if len(row_elements)==1:
            return None
        last_row = row_elements[-1]
        row_number = last_row.attrib['r']
        data = [row_number]
        for c_element in last_row.findall(prefix+'c'):
            data_type = c_element.attrib['t']
            if data_type == 'inlineStr':
                t_element = c_element.find('.//%st'%prefix)
                value = t_element.text
            elif data_type == 'n':
                v_element = c_element.find(prefix+'v')
                value = float(v_element.text)
            else:
                value = None
            if value == 0:
                value = float("nan")
            data.append(value)
        return data
        
    def get_newest_data(self):
        target_file_path = "xl/worksheets/sheet1.xml"
        file_content = self.read_file_in_zip(self.file_path, target_file_path)
        data = self.extract_last_row_data(file_content)
        if self.last_timestamp == data[1]:
            return [-1, -1]
        else:
            self.last_timestamp = data[1]
            return data

class alarmer():
    def __init__(self):
        self.rules = config.rules
        # print self.rules
        self.firsttime = True
        self.lastmsg = ''
        self.next_snapshot_time = []
        self.next_snapshot_periodic = self.get_next_periodic()

    def alarm(self,data):
        msg = ''
        status_changed = False
        for i in self.rules:# self.rules is a dictionary
            # rl: [0 val_low,1 val_high,2 msg_low,3 msg_high,4 status_init,5 delay_snapshot]
            rl = self.rules[i]
            data_name = i.split(':')[0]
            if data_name in data:
                val = data[data_name]
                status = rl[4]
                if val > rl[1]:# value is too high
                    status = True
                    if rl[4] != status:
                        msg += '%s Value: %s\n'%(rl[3],val)
                        status_changed = True
                elif val < rl[0]:# value is too low
                    status = False
                    if rl[4] != status:
                        msg += '%s Value: %s\n'%(rl[2],val)
                        status_changed = True
                rl[4] = status
                if 'Snapshot' in msg and not self.firsttime:
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

        print '%-25s\t%-10g\t%s\t%s'%(rule_name,val,val_low,val_high),
        print status_string,
        print '\t%d%d-%d%d\n'%('Alarm' in msg_low,'Alarm' in msg_high,'Snapshot' in msg_low,'Snapshot' in msg_high),

    def snap_shot(self,data,force=False):
        if force:
            msg = '\n'.join(['%s: %s'%(i,data[i]) for i in config.snapshot_list])
            self.send('%s snapshot [sent manually]'%config.fridge_name,msg)
        else:
            t = time.time()
            if any([t >= i for i in self.next_snapshot_time]):
                msg = '\n'.join(['%s: %s'%(i,data[i]) for i in config.snapshot_list])
                self.send('%s snapshot'%config.fridge_name,msg)
                self.next_snapshot_time = [i for i in self.next_snapshot_time if t < i]
                
            if t > self.next_snapshot_periodic:
                msg = '\n'.join(['%s: %s'%(i,data[i]) for i in config.snapshot_list])
                self.send('%s snapshot [sent monthly]'%config.fridge_name,msg)
                self.next_snapshot_periodic = self.get_next_periodic()
                
    def get_next_periodic(self):
        '''
        Get next datetime for periodic notification
        '''
        dt = datetime.datetime.now()
        # 1st day of nextmonth
        dt_next = (dt.replace(day=1,hour=12,minute=0,second=0,microsecond=0) + datetime.timedelta(days=32)).replace(day=1)
        
        wdy = dt_next.weekday()
        if wdy <= 1:
            dt_next += datetime.timedelta(days=8-wdy)
        else:
            dt_next += datetime.timedelta(days=15-wdy)
        ts_next = time.mktime(dt_next.timetuple())
        return ts_next
    
    def get_next_snapshot_time(self):
        ts = min(self.next_snapshot_time + [self.next_snapshot_periodic])
        return datetime.datetime.fromtimestamp(ts)

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

    def send_lark(self,title,msg):
        if msg:
            title_color = 'orange' if 'Alarm' in msg else 'black'
            title = '<font color="%s">%s</font>'%(title_color,title)
            body = {"tag": "div", "text": {"content": '%s\n<font color="grey">%s</font>\n%s'%(title,time.strftime("%Y-%m-%d %H:%M:%S"),msg), "tag": "lark_md"}}
            data = json.dumps({"msg_type": "interactive", "card": {"elements": [body]}})

            url = config.url
            req = urllib2.Request(url)
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, data)
            self.lastmsg = '\n----------------\nMessage sent to lark:\n%s'%msg + '\nResponse:\n' + response.read()

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
        elif config.method == 'lark':
            self.send_lark(title,msg)
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
timesleep = 301
last_line_number = -1# line number in oxford, timestamp in ppms.
num_files_opened = 0
try:
    while True:
        os.system('cls')
        print '====================\n%s status monitor\n====================\n\npress ctrl + e to exit, ctrl + p to send a snapshot of the fridge status, ctrl + t to send a test message. Flag: Whether "Alarm" in message1/2, whether "Snapshot" in message1/2.\nData is fetched every %s seconds from'%(config.fridge_name,timesleep),
        
        if last_line_number < 0:
            # find the newest data file
            path_list = [os.path.join(folder, i) for i in os.listdir(folder) if i.endswith('xlsx')]
            paths_and_mtimes = [(i, os.path.getmtime(i)) for i in path_list]
            paths_and_mtimes.sort(key=lambda x: x[1], reverse=True)
            filename = paths_and_mtimes[0][0]
            vr = xlsx_reader_xs(filename)# chenge to dat_reader_ppms if for PPMS
            num_files_opened += 1
            
        print '%s. Counter: %s. Next snapshot time: %s.'%(filename, num_files_opened, alm.get_next_snapshot_time())
        
        data = vr.get_newest_data()
        line_number = data[1]# data[1] is the current line number in oxford, timestamp in ppms or xs.
        if line_number == -1:
            last_line_number = -1
            continue
        else:
            last_line_number = line_number
        print "\n%s\n\n#%s\n%-25s\t%-10s\t%s\t%s\t%s\t%s"%(time.strftime("%Y-%m-%d %H:%M:%S"),line_number,'Name','PV','A1','A2','Status','Flag')
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
