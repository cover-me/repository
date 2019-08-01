from pkt import transMatrix, imgMarkers, choose_pattern, choose_path, choose_suffix
import numpy as np
import os,sys
from time import sleep

args = sys.argv[1:]
os.system("cls")
strg = '### PKout 3! Quick import your .tif files! ###\n'
print strg
ptn = choose_pattern()
os.chdir(choose_path())
sffx = choose_suffix()

fns = [i for i in os.listdir(os.getcwd())]
os.system("cls")
print strg
print "your data is in \"%s\""%os.getcwd()
print "%s .tif file(s) found\n"%(len([i for i in fns if i.endswith('.tif')]))

imark = imgMarkers(ptn,sffx)
imark.updateLys('sample.lys')
print
sleep(12)
