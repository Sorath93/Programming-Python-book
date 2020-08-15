############################################################################
# Usage: "python diffall.py dir1 dir2".  recursive tree comparison:
# report unique files that exist in only dir1 or dir2,
# report files of same name in dir1 and dir2 with differing contents,
# report instances of same name but different type in dir1 and dir2,
# and do the same for all subdirectories of the same names in and below
# dir1 and dir2;  summary of diffs appears at end of output, but search
# redirected output for "DIFF" and "unique" strings for further details;
# new: limit reads to 1M for large files, catch same name=file/dir;
############################################################################
     
import os, dirdiff
blocksize = 1024 * 1024  # up to 1M per read
     
def intersect(seq1, seq2):
    commons = []                     # items in seq1 and seq2
    for item in seq1:                # or use new set() object 
        if item in seq2:
            commons.append(item)
    return commons
     
def comparedirs(dir1, dir2, diffs, verbose=False):
    # compare filename lists
    print '-'*20
    if not dirdiff.comparedirs(dir1, dir2):
        diffs.append('unique files at %s - %s' % (dir1, dir2))

    print 'Comparing contents'
    names1 = os.listdir(dir1)
    names2 = os.listdir(dir2)
    common = intersect(names1, names2)
    missed = common[:]
     
    # compare contents of files in common
    for name in common:
        path1 = os.path.join(dir1, name)
        path2 = os.path.join(dir2, name)
        if os.path.isfile(path1) and os.path.isfile(path2):
            missed.remove(name)
            file1 = open(path1, 'rb')
            file2 = open(path2, 'rb')
            while True:
                bytes1 = file1.read(blocksize)
                bytes2 = file2.read(blocksize)
                if (not bytes1) and (not bytes2):
                    if verbose: print name, 'matches'
                    break
                if bytes1 != bytes2:
                    diffs.append('files differ at %s - %s' % (path1, path2))
                    print name, 'DIFFERS'
                    break
     
    # recur to compare directories in common
    for name in common:
        path1 = os.path.join(dir1, name)
        path2 = os.path.join(dir2, name)
        if os.path.isdir(path1) and os.path.isdir(path2):
            missed.remove(name)
            comparedirs(path1, path2, diffs, verbose)

    # same name but not both files or dirs?
    for name in missed:
        diffs.append('files missed at %s - %s: %s' % (dir1, dir2, name))
        print name, 'DIFFERS'

     
if __name__ == '__main__':
    dir1, dir2 = dirdiff.getargs()
    mydiffs = []
    comparedirs(dir1, dir2, mydiffs, True)     # changes mydiffs in-place
    print '='*40                               # walk, report diffs list
    if not mydiffs:
        print 'No diffs found.'
    else:
        print 'Diffs found:', len(mydiffs)
        for diff in mydiffs: print '-', diff
