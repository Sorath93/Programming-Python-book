##################################################################
# count lines in all source files in tree; os.path.walk version
##################################################################

import os, sys
allLines = allFiles = 0
allExts  = ['.py', '.pyw', '.cgi', '.html', '.c', '.cxx', '.h', '.i']
allSums = dict.fromkeys(allExts, 0)

def sum(dir, file, ext):
    global allFiles, allLines
    print file
    fname = os.path.join(dir, file)
    lines = open(fname).readlines()
    allFiles += 1                                     # or all = all + 1
    allLines += len(lines)
    allSums[ext] += 1

def wc(ignore, dir, fileshere):
    for file in fileshere:
        for ext in allExts:
            if file.endswith(ext):                    # or f[-len(e):] == e
                sum(dir, file, ext)
                break

if __name__ == '__main__':
    os.path.walk(sys.argv[1], wc, None)               # cmd arg=root dir
    print '-'*80
    print 'Files=>', allFiles, 'Lines=>', allLines
    print allSums
