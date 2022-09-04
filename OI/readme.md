This script runs with python 2, using build-in modules only. You can install python27, or download a portable version of it (and put it in the same folder as the script as shown by the following picture).

![image](https://user-images.githubusercontent.com/22870592/188307704-0bac3dc7-2562-4462-ab9f-5e28f00b614a.png)


Configure file paths in the BAT file, VCL folder/email/webhook url/alert rules in the PY file, and double-click the BAT file to run (or PY file if python27 is registered in the operating system):

![image](https://user-images.githubusercontent.com/22870592/188307143-53172023-e463-459c-820f-3b241a067b44.png)

Oxford fridge stores data in a VCL file. This file is updated every 1 minute. The script get values from the newest VCL file in the folder specified in the PY file. One can also get readings via a TCP/IP port but that one may be occupied for experiments (and for DR200 it does not contain all values).

