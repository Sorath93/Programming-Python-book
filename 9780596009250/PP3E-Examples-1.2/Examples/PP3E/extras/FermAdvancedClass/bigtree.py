import sys, glob, os
if sys.platform[:3] == 'win':
    libdir = r'C:\Python24\Lib'
else:
    libdir = '/usr/lib/python24'

allsizes = []
for (currDir, subdirs, files) in os.walk(libdir):
    for filename in files:
        if filename.endswith('.py'):
            filepath = os.path.join(currDir, filename)
            filesize = os.path.getsize(filepath)
            allsizes.append((filesize, filepath))

allsizes.sort()
print len(allsizes)
print allsizes[:2]
print allsizes[-2:]
