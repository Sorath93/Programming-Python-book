import sys, os
if sys.platform[:3] == 'win':
    libdir = r'C:\Python24\Lib'
else:
    libdir = '/usr/lib/python'

allsizes = []
for (thisDir, subsHere, filesHere) in os.walk(libdir):
   for filename in filesHere:
       if filename.endswith('.py'):
           filepath = os.path.join(thisDir, filename)
           filesize = os.path.getsize(filepath)
           allsizes.append((filesize, filepath))

allsizes.sort()    
print 'Small', allsizes[:3]
print 'Large', allsizes[-3:]
