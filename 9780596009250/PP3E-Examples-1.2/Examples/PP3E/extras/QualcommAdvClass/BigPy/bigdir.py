import glob, sys, os
if sys.platform[:3] == 'win':
    libdir = r'C:\Python24\Lib'
else:
    libdir = '/usr/lib/python'

##allsizes = []
##filepatt = os.path.join(libdir, '*.py')
##for filename in glob.glob(filepatt):
##    filesize = os.path.getsize(filename)
##    allsizes.append((filesize, filename))

filepatt = os.path.join(libdir, '*.py')
allsizes = [(os.path.getsize(filename), filename)
            for filename in glob.glob(filepatt)]

allsizes.sort()    
print 'Small', allsizes[:3]
print 'Large', allsizes[-3:]
