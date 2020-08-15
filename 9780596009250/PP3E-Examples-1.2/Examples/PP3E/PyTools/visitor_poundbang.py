##########################################################################
# change all "#!...python" source lines at the top of scripts to either 
# commandline arg or changeToDefault, in all files in all dirs at and 
# below the dir where run; could skip binary filename extensions too, 
# but works ok; this version changes all #! first lines that name python,
# and so is more accurate than a simple visitor_replace.py run;
##########################################################################

"""
Run me like this, to convert all scripts in the book 
examples tree, and redirect/save messages to a file:
C:\...\PP3E>python PyTools\visitor_poundbang.py 
                           #!\MyPython24\python > out.txt
"""

import sys
from PP3E.PyTools.visitor import FileVisitor    # reuse the walker classes
changeToDefault = '#!\Python24\python'          # used if no cmdline arg

class PoundBangFixer(FileVisitor):
    def __init__(self, changeTo=changeToDefault):
        FileVisitor.__init__(self)
        self.changeTo = changeTo
        self.clist    = []
    def visitfile(self, fullname):
        FileVisitor.visitfile(self, fullname)
        try:
            lines = open(fullname, 'r').readlines()
            if (len(lines) > 0        and
                lines[0][0:2] == '#!' and                # or lines[0].startswith() 
                'python' in lines[0]                     # or lines[0].find() != -1
                ):
                lines[0] = self.changeTo + '\n'
                open(fullname, 'w').writelines(lines)
                self.clist.append(fullname)
        except:
            print 'Error translating %s -- skipped' % fullname
            print '...', sys.exc_info()

if __name__ == '__main__':
    if raw_input('Are you sure?') != 'y': sys.exit()
    if len(sys.argv) == 2: changeToDefault = sys.argv[1]
    walker = PoundBangFixer(changeToDefault)
    walker.run()
    print 'Visited %d files and %d dirs,' % (walker.fcount, walker.dcount),
    print 'changed %d files' % len(walker.clist)
    for fname in walker.clist: print fname
