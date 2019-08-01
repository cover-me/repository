import sys
import os
import win32com.client
# TEST = False
# if TEST:
    # import pythoncom
try:
    word = win32com.client.GetActiveObject('word.application')
    worddoc = word.ActiveDocument
    if len(sys.argv)>1:
        cend = worddoc.Content.End
        worddoc.Content.InsertAfter(sys.argv[1])
        print "toWord: %s"%sys.argv[1]
        if len(sys.argv) > 2:
            try:
                styleNum = int(sys.argv[2])#number can be found on https://msdn.microsoft.com/en-us/library/bb237495(v=office.12).aspx
                rng = worddoc.Range(cend-1,cend-1+len(sys.argv[1]))
                if styleNum < -1:
                    rng.Style = styleNum
                elif styleNum > 13:
                    rng.Font.Size = styleNum
                elif styleNum == 0:
                    rng.InlineShapes.AddHorizontalLineStandard()
            except:
                pass
    # if TEST:
        # print "Before release: %d"%pythoncom._GetInterfaceCount()
    rng = None
    worddoc = None
    word = None#release com objects, https://mail.python.org/pipermail/python-win32/2005-August/003661.html
    # if TEST:
        # print "After release: %d"%pythoncom._GetInterfaceCount()
except:
    print "toWord: No word file has been opened."