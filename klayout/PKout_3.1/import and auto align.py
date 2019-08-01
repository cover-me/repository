from pkt import imgMarkers, choose_pattern, choose_path, choose_suffix
import os,sys
from time import sleep

args = sys.argv[1:]
os.system("cls")
strg = '### PKout 3! Auto find cross markers and align! ###\n'
print strg
if 'test' in args:
    ptn = choose_pattern(0)
    imark = imgMarkers(ptn,'',addLandMarker=True)
    imark.open(r'test.tif')
    imark.test()
    sys.exit(0)
ptn = choose_pattern()
os.chdir(choose_path())
sffx = choose_suffix()

fns = [i for i in os.listdir(os.getcwd())]
os.system("cls")
print strg
print "Your files are in \"%s\""%os.getcwd()
print "%s .tif file(s) found\n"%(len([i for i in fns if i.endswith('.tif')]))
print "Use pattern: %s"%ptn[0]

imark = imgMarkers(ptn,sffx,addLandMarker=True)
imark.updateLys('sample.lys')
print
imark.tm.updateMatrix('sample_tifsmart.lys',newName=False)
print
sleep(12)
