# find biggest file in a tree

import os, sys
if sys.platform[:3] == 'win':
    pydir = r'\Python24\Lib'
else:
    pydir = '/usr/lib/python'

allsizes = []
for (thisDir, subsHere, filesHere) in os.walk(pydir):
    for file in filesHere:
        if file.endswith('.py'):
            fullpath = os.path.join(thisDir, file)
            fullsize = os.path.getsize(fullpath)
            allsizes.append((fullsize, fullpath))

allsizes.sort()
print allsizes[:2]
print allsizes[-2:]
