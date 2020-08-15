##################################################################
# count lines in all source files in tree; find patterns version
##################################################################

import sys
from wcall import allExts
from PP3E.PyTools.find import find

allLines = allFiles = 0
allSums  = dict.fromkeys(allExts, 0)

def sum(fname, ext):
    global allFiles, allLines
    print fname
    lines = open(fname).readlines()
    allFiles += 1
    allLines += len(lines)
    allSums[ext] += 1

for ext in allExts:
    files = find('*' + ext, sys.argv[1])
    for file in files:
        sum(file, ext)

print '-'*80
print 'Files=>', allFiles, 'Lines=>', allLines
print allSums
