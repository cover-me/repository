# What this program does
![image](https://user-images.githubusercontent.com/22870592/154365834-43d2517a-876d-4b45-80cd-a23801a71f74.png)

# How does it work

## Emulate a TCP/IP virtual instrument

https://github.com/cover-me/tcp-visa-server

## Get control references from another LabVIEW VI or EXE

By default, LabVIEW opens a TCP server that can be accessed by another LabVIEW program. That makes it possible to programmably control a labVIEW VI or EXE which is not allowed to be modified. For EXE files, there is usually an INI with the same name in the same folder. The TCP port number can be found in that INI file ("server.tcp.port=****").

Firt we get the referece to the front panel with IP address (127.0.0.1 if on the same computer) and the port number:

![image](https://user-images.githubusercontent.com/22870592/154369875-d6ba2150-f33e-4377-a9a3-efa3525c17ab.png)

Then we get references to all the controls we need:

![image](https://user-images.githubusercontent.com/22870592/154368794-a770f468-6308-405b-ad55-45ad1725798c.png)

Get/set controls in the data-processing sub VI:

![image](https://user-images.githubusercontent.com/22870592/154368903-3e633cff-96ae-4cad-937a-7c58e17fc10b.png)


The diagram of the toppest VI:

![image](https://user-images.githubusercontent.com/22870592/154368966-edef506d-8f3b-406f-a277-924c4246e62f.png)
