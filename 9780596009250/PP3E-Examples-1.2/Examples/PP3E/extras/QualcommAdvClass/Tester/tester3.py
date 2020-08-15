"""
test all programs in a given directory
looking for regressions in their output
use tmpfiles and filecmp to be more robust
"""

import os, sys, glob, filecmp
testdir = os.curdir
regenerate = False
try:
    testdir = sys.argv[1]
    regenerate = sys.argv[2]
except:
    pass

scriptsub = 'scripts'
outputsub = 'outputs'

testpatt = os.path.join(testdir, scriptsub, '*.py')
for filename in glob.glob(testpatt):
    command = '%s %s' % (sys.executable, filename)
    pipe = os.popen(command)
    basename = os.path.split(filename)[1]
    outname  = os.path.splitext(basename)[0] + '.txt'
    outpath  = os.path.join(testdir, outputsub, outname)

    tempname = outpath + '.tmp'
    tempfile = open(tempname, 'wb')
    while True:
        bytes = pipe.read(1024)
        if not bytes: break
        tempfile.write(bytes)
    tempfile.close()

    if not os.path.exists(outpath) or regenerate:
        if os.path.exists(outpath): os.remove(outpath)
        os.rename(tempname, outpath)
        print 'Created:', outname
    else:
        if filecmp.cmp(tempname, outpath):  
            print 'Passed:', filename
        else:
            print 'Failed:', filename
        os.remove(tempname)    
