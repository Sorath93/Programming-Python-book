import sys, glob, os, pprint

allsizes = []
for pydir in sys.path:
    pypatt  = os.path.join(pydir, '*.py')
    pyfiles = glob.glob(pypatt)
    for filename in pyfiles:
        print filename
        filesize = os.path.getsize(filename)
        allsizes.append((filesize, filename))

allsizes.sort()
print 'Small'
pprint.pprint(allsizes[:3])
print 'Large'
pprint.pprint(allsizes[-3:])

