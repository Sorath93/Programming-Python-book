import glob, sys, os, pprint
allsizes = []
for srcdir in sys.path:
    pypatt  = os.path.join(srcdir, '*.py')
    pyfiles = glob.glob(pypatt)
    for filename in pyfiles:
        pysize = os.path.getsize(filename)
        allsizes.append((pysize, filename))

allsizes.sort()
pprint.pprint(allsizes[:3])
pprint.pprint(allsizes[-3:])

