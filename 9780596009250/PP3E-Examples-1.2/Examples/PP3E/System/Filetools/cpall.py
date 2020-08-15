############################################################################
# Usage: "python cpall.py dirFrom dirTo".
# Recursive copy of a directory tree.  Works like a "cp -r dirFrom/* dirTo" 
# unix command, and assumes that dirFrom and dirTo are both directories.  
# Was written to get around fatal error messages under Windows drag-and-drop
# copies (the first bad file ends the entire copy operation immediately), 
# but also allows for coding customized copy operations.  May need to
# do more file type checking on Unix: skip links, fifos, etc.  
############################################################################
     
import os, sys
verbose = 0
dcount = fcount = 0
maxfileload = 500000
blksize = 1024 * 100
     
def cpfile(pathFrom, pathTo, maxfileload=maxfileload):
    """
    copy file pathFrom to pathTo, byte for byte
    """
    if os.path.getsize(pathFrom) <= maxfileload:
        bytesFrom = open(pathFrom, 'rb').read()   # read small file all at once
        open(pathTo, 'wb').write(bytesFrom)       # need b mode on Windows
    else:
        fileFrom = open(pathFrom, 'rb')           # read big files in chunks
        fileTo   = open(pathTo,   'wb')           # need b mode here too 
        while 1:
            bytesFrom = fileFrom.read(blksize)    # get one block, less at end
            if not bytesFrom: break               # empty after last chunk
            fileTo.write(bytesFrom)
     
def cpall(dirFrom, dirTo):
    """
    copy contents of dirFrom and below to dirTo
    """
    global dcount, fcount
    for file in os.listdir(dirFrom):                      # for files/dirs here
        pathFrom = os.path.join(dirFrom, file)
        pathTo   = os.path.join(dirTo,   file)            # extend both paths
        if not os.path.isdir(pathFrom):                   # copy simple files
            try:
                if verbose > 1: print 'copying', pathFrom, 'to', pathTo
                cpfile(pathFrom, pathTo)
                fcount = fcount+1
            except:
                print 'Error copying', pathFrom, 'to', pathTo, '--skipped'
                print sys.exc_info()[0], sys.exc_info()[1]
        else:
            if verbose: print 'copying dir', pathFrom, 'to', pathTo
            try:
                os.mkdir(pathTo)                          # make new subdir
                cpall(pathFrom, pathTo)                   # recur into subdirs
                dcount = dcount+1
            except:
                print 'Error creating', pathTo, '--skipped'
                print sys.exc_info()[0], sys.exc_info()[1]
     
def getargs():
    try:
        dirFrom, dirTo = sys.argv[1:]
    except:
        print 'Use: cpall.py dirFrom dirTo'
    else:
        if not os.path.isdir(dirFrom):
            print 'Error: dirFrom is not a directory'
        elif not os.path.exists(dirTo):
            os.mkdir(dirTo)
            print 'Note: dirTo was created'
            return (dirFrom, dirTo)
        else:
            print 'Warning: dirTo already exists'
            if dirFrom == dirTo or (hasattr(os.path, 'samefile') and
                                    os.path.samefile(dirFrom, dirTo)):
                print 'Error: dirFrom same as dirTo'
            else:
                return (dirFrom, dirTo)
     
if __name__ == '__main__':
    import time
    dirstuple = getargs()
    if dirstuple: 
        print 'Copying...'
        start = time.time()
        cpall(*dirstuple)
        print 'Copied', fcount, 'files,', dcount, 'directories',
        print 'in', time.time() - start, 'seconds'
