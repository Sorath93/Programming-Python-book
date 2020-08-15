# find biggest file in a dir

import glob, os, sys
if sys.platform[:3] == 'win':
    pydir = r'\Python24\Lib'
else:
    pydir = '/usr/lib/python'

allsizes = []
pyfile = glob.glob(os.path.join(pydir, '*.py'))
for pyfile in pyfile:
    pysize = os.path.getsize(pyfile)
    allsizes.append((pysize, pyfile))

allsizes.sort()
print allsizes[:2]
print allsizes[-2:]
