# Description

A python2 script that sends notifications or summaries of an Oxford fridge status when the fridge status changes. Messages can be sent through email, Slack, Lark (Feishu), or WeCom (WeChat Business). Triggering events can be customized in the configuration file. For Leiden fridges, see [FP_monitor.vi](https://github.com/cover-me/repository/tree/master/Leiden/1.0_190721_LV17).

The Oxford fridge stores data in a VCL file. This file is updated every 1 minute (interval can be modified). The script reads values from the newest VCL file automatically found in a specified folder.

![image](https://github.com/cover-me/repository/assets/22870592/f94444b9-55ef-488d-8e50-49968fa025a3)

# Installation

The script runs with python2. You can install python27, or download a portable version of it without installation (copy it from another computer and put it in the same folder as shown in the following picture).

![18c3c17ae8b6ff31bdeacef8ceae8b0](https://github.com/cover-me/repository/assets/22870592/c11b6d0c-2549-4d6f-bc00-e8c69cfc1b6a)

Download scripts to the fridge control computer. Configure script paths in the BAT file. Config VCL folder/email/webhook url/alert rules in config.py. Double-click the BAT file to run (or PY file to run if python27 is already registered in the operating system):

![8477eaca4b0c3680721a9151e1dd4fc](https://github.com/cover-me/repository/assets/22870592/f49bd760-abb5-47c4-84c6-49c4148db42c)


# Configure triggering events

To customize triggering events, modify the code below:

```python
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
```

The original plan was to make the controlling computer beep when the "Alarm" appeared in the message. However, this function is not implemented, and it would be annoying (in the Leiden version I implemented the beeping). In the current version, "Alarm" is used only to make the font color of the title orange in the sent message.

If the "Snapshot" appears in the message, a snapshot of sensor data will be sent after the time_in_second specified at the end of the list. The sensors are specificated with the code

```python
snapshot_list = [i for i in labels if (i.endswith('T(K)')    
    and not i.startswith('chan'))
    or i in ['P1 Tank (Bar)','P3 Still (mbar)','Dewar (mbar)','Still heater (W)']
]
```

If a message is left empty, the corresponding event is disabled.

# Further reading

One can also get readings through TCP/IP but that may be occupied for experiments (and for DR200 TCP/IP does not return all values). For the TCP/IP method, see [DR and Triton qtlab drivers](https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers), [Leiden TC_messenger](https://github.com/cover-me/repository/tree/master/Leiden/TC_messenger_2021_02_01), and [PPMS tcp-visa-server](https://github.com/cover-me/repository/tree/master/QD/tcp-visa-server).
