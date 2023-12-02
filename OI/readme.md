# Description

This script send notifications via Slack, email, or WeCom (WeChat Business) when the status of an Oxford fridge changes. For Leiden fridges, see [FP_monitor.vi](https://github.com/cover-me/repository/tree/master/Leiden/1.0_190721_LV17).

Oxford fridge stores data in a VCL file. This file is updated every 1 minute (the interval can be modified). The script get values from the newest VCL file automatically found in the folder specified.

# How to use

This script runs with python 2. You can install python27, or download a portable version of it (copy it from another computer, put it in the same folder as shown in the following picture).

![image](https://user-images.githubusercontent.com/22870592/188307704-0bac3dc7-2562-4462-ab9f-5e28f00b614a.png)


Download scripts to the fridge control computer. Configure script paths in .bat. Config VCL folder/email/webhook url/alert rules in config.py (the screenshot above shows an older version without config.py). Double-click the BAT file to run (or PY file if python27 is already registered in the operating system):

![image](https://user-images.githubusercontent.com/22870592/188307143-53172023-e463-459c-820f-3b241a067b44.png)

# Further reading

One can also get readings through TCP/IP but that may be occupied for experiments (and for DR200 TCP/IP does not return all values). For the TCP/IP method, see [DR and Triton qtlab drivers](https://github.com/cover-me/repository/tree/master/qt/qtlab%20new%20drivers), [Leiden TC_messenger](https://github.com/cover-me/repository/tree/master/Leiden/TC_messenger_2021_02_01), and [PPMS tcp-visa-server](https://github.com/cover-me/repository/tree/master/QD/tcp-visa-server).
