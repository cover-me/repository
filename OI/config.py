from collections import OrderedDict

fridge_name = 'Top Loading'
folder = ''# folder of vcl files

# To find the labels, open a VCL file and search for "This is the standard comments block", keep replacing NUL NUL (\0) with NUL, then replace NUL with ', '  

# DR200 
# LineSize(bytes) LineNumber Time(secs) PressureM1Condense(Bar) PressureM3Tank(Bar) PressureFPSafety(Bar) Still (mbar) Forepump (mbar) Dewar (mbar) Input Water Temp Output Water Temp Helium Temp Oil Temp Motor Current 4K Head X55749 t(s) 4K Head X55749 T(K) 4K Head X55749 R(Ohm) 4K Plate X55750 t(s) 4K Plate X55750 T(K) 4K Plate X55750 R(Ohm) Still t(s) Still T(K) Still R(Ohm) 100mK Plate t(s) 100mK Plate T(K) 100mK Plate R(Ohm) M/C X55751 t(s) M/C X55751 T(K) M/C X55751 R(Ohm) M/C RuO2 t(s) M/C RuO2 T(K) M/C RuO2 R(Ohm) Mag Top X48230 t(s) Mag Top X48230 T(K) Mag Top X48230 R(Ohm) Mag Bottom X52698 t(s) Mag Bottom X52698 T(K) Mag Bottom X52698 R(Ohm) 70K Head PT100 t(s) 70K Head PT100 T(K) 70K Head PT100 R(Ohm) 70K Plate PT100 t(s) 70K Plate PT100 T(K) 70K Plate PT100 R(Ohm) chan[10] t(s) chan[10] T(K) chan[10] R(Ohm) chan[11] t(s) chan[11] T(K) chan[11] R(Ohm) chan[12] t(s) chan[12] T(K) chan[12] R(Ohm) chan[13] t(s) chan[13] T(K) chan[13] R(Ohm) chan[14] t(s) chan[14] T(K) chan[14] R(Ohm) chan[15] t(s) chan[15] T(K) chan[15] R(Ohm) Still heater (W) chamber heater (W)

# Triton 
labels = 'LineSize(bytes), LineNumber, Time(secs), P2 Condense (Bar), P1 Tank (Bar), P5 ForepumpBack (Bar), P3 Still (mbar), P4 TurboBack (mbar), Dewar (mbar), Input Water Temp, Output Water Temp, Helium Temp, Oil Temp, Motor Current, PT1 Plate t(s), PT1 Plate T(K), PT1 Plate R(Ohm), PT2 Plate t(s), PT2 Plate T(K), PT2 Plate R(Ohm), Still t(s), Still T(K), Still R(Ohm), 100mK Plate t(s), 100mK Plate T(K), 100mK Plate R(Ohm), MC RuO2 t(s), MC RuO2 T(K), MC RuO2 R(Ohm), MC cernox t(s), MC cernox T(K), MC cernox R(Ohm), chan[6] t(s), chan[6] T(K), chan[6] R(Ohm), chan[7] t(s), chan[7] T(K), chan[7] R(Ohm), chan[8] t(s), chan[8] T(K), chan[8] R(Ohm), chan[9] t(s), chan[9] T(K), chan[9] R(Ohm), chan[10] t(s), chan[10] T(K), chan[10] R(Ohm), chan[11] t(s), chan[11] T(K), chan[11] R(Ohm), Magnet t(s), Magnet T(K), Magnet R(Ohm), Still heater (W), chamber heater (W), IVC sorb heater (W), turbo current(A), turbo power(W), turbo speed(Hz), turbo motor(C), turbo bottom(C)'.split(', ')

# Triton_XL, there are two Input/Output Water Temps (this model has two PTs), made the seconds to Input/Onput Water Temp2
# labels = ['LineSize(bytes)', 'LineNumber', 'Time(secs)', 'P2 Condense (Bar)', 'P1 Tank (Bar)', 'P5 ForepumpBack (Bar)', 'P3 Still (mBar)', 'P4 TurboBack (mBar)', 'Dewar (mBar)', 'Input Water Temp', 'Output Water Temp', 'Oil Temp', 'Helium Temp', 'Motor Current', 'Low Pressure', 'High Pressure', 'PT2 Head T(K)', 'PT2 Head R(Ohm)', 'PT2 Plate T(K)', 'PT2 Plate R(Ohm)', 'Still Plate T(K)', 'Still Plate R(Ohm)', 'Cold Plate T(K)', 'Cold Plate R(Ohm)', 'MC Plate Cernox old T(K)', 'MC Plate Cernox old R(Ohm)', 'PT1 Head old T(K)', 'PT1 Head old R(Ohm)', 'PT1 Plate old T(K)', 'PT1 Plate old R(Ohm)', 'MC Plate RuO2 old T(K)', 'MC Plate RuO2 old R(Ohm)', 'MC Plate Cernox T(K)', 'MC Plate Cernox R(Ohm)', 'PT1 Head  T(K)', 'PT1 Head  R(Ohm)', 'PT1 Plate T(K)', 'PT1 Plate R(Ohm)', 'MC Plate RuO2 T(K)', 'MC Plate RuO2 R(Ohm)', 'Magnet T(K)', 'Magnet R(Ohm)', 'Still heater (W)', 'chamber heater (W)', 'IVC sorb heater (W)', 'Input Water Temp2', 'Output Water Temp2', 'Oil Temp2', 'Helium Temp2', 'Motor Current2', 'Low Pressure2', 'High Pressure2', 'turbo current(A)', 'turbo power(W)', 'turbo speed(Hz)', 'turbo motor(C)', 'turbo bottom(C)']

# PPMS
# labels = ['Comment','Time Stamp (sec)','Temperature (K)','Magnetic Field (Oe)','System Pres (Torr)','Chamber Status (code)','Temperature Status (code)','Field Status (code)','Cryostat Status (code)','Control Therm (ID)','Sample Therm (ID)','Block Temp (K)','Neck Temp (K)','High Neck Temp (K)','Control Temp (K)','1st Stage Temp (K)','2nd Stage Temp (K)','Magnet Temp (K)','Impedance Temp (K)','Pot Liquid level (%)','Block Power (W)','Neck Heater Power (W)','High Neck Heater Power (W)','1st Stage Heater Power (W)','2nd Stage Heater Power (W)','Magnet Voltage (V)','Impedance Heater Power (W)','Pot Power (W)','CFE Flow (SCCM)','Pump Flow (uncal SCCM)','Tank Pressure (Torr)','Annulus Pressure (Torr)','Compressor State (code)']
# snapshot_list = ['Temperature (K)','Magnetic Field (Oe)','System Pres (Torr)','Block Temp (K)','Neck Temp (K)','High Neck Temp (K)','1st Stage Temp (K)','2nd Stage Temp (K)','Magnet Temp (K)','Pot Liquid level (%)','Block Power (W)','Impedance Heater Power (W)','Pot Power (W)','CFE Flow (SCCM)','Pump Flow (uncal SCCM)','Tank Pressure (Torr)','Annulus Pressure (Torr)','Compressor State (code)']

snapshot_list = [i for i in labels if (i.endswith('T(K)')    
    and not i.startswith('chan'))
    or i in ['P1 Tank (Bar)','P3 Still (mbar)','Dewar (mbar)','Still heater (W)']
]

# dr200:512, triton:488, tritonXL:456 (see logging -> log file information for the file-size change)
num = 488

# [0 val_low,1 val_high,2 msg_low,3 msg_high,4 status_init,5 delay_snapshot]
# 5 can be empty, it is used only if a msg containing "Snapshot" is added to the queue
rules = OrderedDict([
    ("Output Water Temp",[27,29,'PT water out<27','Alarm! PT water out>29',False]),
    ("Output Water Temp:2",[10,12,'Alarm! PT water out<10','',True]),
    ("Motor Current",[10,10.1,'Alarm! PT is off','PT is on',True]),
    ("MC RuO2 T(K)",[0.05,10,'MC < 0.05 K. Snapshot will be sent in 2 hours.','',True,3600*2]),
    ("Magnet T(K):1",[280,285,'','Magnet > 285 K. Snapshot will be sent in 2 hours.',True,3600*2]),
    ("Magnet T(K):2",[5,10,'Magnet < 5 K','',True]),
    ("Magnet T(K):3",[80,85,'Magnet < 80 K','Magnet > 85 K',True]),
    #("Dewar (mbar)",[5e-3,1,'OVC < 5e-3 mbar','OVC > 1 mbar',True]),
])

method = 'wechat'# wechat, slack, or email

url = ''

recipients = ['r1@gmail.com','r2@outlook.com']
email = 'youremail@mail.com'
password = 'yourpassword'
host = "smtp.xxx.com"
port = '123'
