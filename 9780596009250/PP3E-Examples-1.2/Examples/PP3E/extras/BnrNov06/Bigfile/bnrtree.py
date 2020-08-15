import sys, os, pprint

allsizes = []
visited  = {}

for pydir in sys.path:
    for (thisDir, subsHere, filesHere) in os.walk(pydir):
        absdir = os.path.normcase(thisDir)
        absdir = absdir.upper()
        if absdir in visited:
            continue
        visited[absdir] = True
        for filename in filesHere:
            if filename.endswith('.py'):
                pypath = os.path.join(thisDir, filename)
                print pypath
                filesize = os.path.getsize(pypath)
                allsizes.append((filesize, pypath))

allsizes.sort()
print 'Small'
pprint.pprint(allsizes[:3])
print 'Large'
pprint.pprint(allsizes[-3:])

