##################################################################
# count lines in all source files in tree; visitor class version
##################################################################

import sys
from wcall import allExts
from PP3E.PyTools.visitor import FileVisitor

class WcAll(FileVisitor):
    def __init__(self):
        FileVisitor.__init__(self)
        self.allLines = self.allFiles = 0
        self.allSums  = dict.fromkeys(allExts, 0)

    def sum(self, fname, ext):
        print fname
        lines = open(fname).readlines()
        self.allFiles += 1
        self.allLines += len(lines)
        self.allSums[ext] += 1

    def visitfile(self, filepath):
        self.fcount += 1
        for ext in allExts:
            if filepath.endswith(ext):
                self.sum(filepath, ext)
                break

if __name__ == '__main__':
    walker = WcAll()
    walker.run(sys.argv[1])
    print 'Visited %d files and %d dirs' % (walker.fcount, walker.dcount)
    print '-'*80
    print 'Files=>', walker.allFiles, 'Lines=>', walker.allLines
    print walker.allSums
