import glob, os
libdir = r'C:\Python24\Lib'

pypatt  = os.path.join(libdir, '*.py')
pyfiles = glob.glob(pypatt)
allsizes = []
for name in pyfiles: 
    filesize = os.path.getsize(name)
    allsizes.append((filesize, name))

print max(allsizes)
print min(allsizes)

allsizes.sort()
print allsizes[0]
print allsizes[-1]



