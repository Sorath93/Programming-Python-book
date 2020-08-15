"""
test all programs in a given directory
looking for regressions in their output
"""

import os, sys, glob
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
    output = pipe.read()
    
    basename = os.path.split(filename)[1]
    outname  = os.path.splitext(basename)[0] + '.txt'
    outpath  = os.path.join(testdir, outputsub, outname)

    if not os.path.exists(outpath) or regenerate:
        open(outpath, 'w').write(output)
        print 'Created:', outname
    else:
        expected = open(outpath).read()
        if output == expected:
            print 'Passed:', filename
        else:
            print 'Failed:', filename
        
    
