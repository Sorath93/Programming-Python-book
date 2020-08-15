import glob, os
libdir = r'C:\Python24\Lib'

savedata = open('data.txt', 'w')
allsizes = []
for (dir, subshere, fileshere) in os.walk(libdir):
    for file in fileshere:
        if file.endswith('.py'):
            fullpath = os.path.join(dir, file)    
            filesize = os.path.getsize(fullpath)
            allsizes.append((filesize, fullpath))
            savedata.write(str((filesize, fullpath)))

print min(allsizes)
print max(allsizes)

allsizes.sort()
print allsizes[0]
print allsizes[-1]
