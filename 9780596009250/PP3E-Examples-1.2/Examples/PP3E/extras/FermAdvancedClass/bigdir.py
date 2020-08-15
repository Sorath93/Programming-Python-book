import os, sys
if sys.platform[:3] == 'win':
    stdlib = r'C:\Python24\Lib'
else:
    stdlib = '/usr/lib/python2.3'

allsizes = []
for (thisDir, subsHere, filesHere) in os.walk(stdlib):
    for filename in filesHere:
        if filename.endswith('.py'):
            filepath = os.path.join(thisDir, filename)
            filesize = os.path.getsize(filepath)
            allsizes.append((filesize, filepath))

allsizes.sort()
print allsizes[:3]
print allsizes[-3:]
