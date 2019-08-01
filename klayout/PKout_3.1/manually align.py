from pkt import transMatrix, imgMarkers, choose_pattern, choose_path, choose_suffix
import numpy as np
import os,sys
from time import sleep

args = sys.argv[1:]
os.system("cls")
strg = '### PKout 3! Align figures with your markers! ###\n'
print strg
ptn = choose_pattern()
os.chdir(choose_path())
sffx = choose_suffix()

period = ptn[3] if len(ptn)>3 else [-100,100]
tm = transMatrix(ptn[1],ptn[2],sffx,period)
print 'updating matrix...'
tm.updateMatrix('sample.lys')
print
sleep(12)



