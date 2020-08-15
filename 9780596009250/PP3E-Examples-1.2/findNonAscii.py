"""
Script used to detect non-ASCII characters in Python source files; these
generate syntax errors as of Python 2.5; most came from cut-and-pastes;
the following files had this issue in examples release 1.1 and were
fixd 1.2 (the first of these made PyMailGUI fail in Python 2.5):

Examples\PP3E\Gui\Tools\threadtools.py [at 504, chr –, ord 150]
Examples\PP3E\Internet\Web\cgi-bin\languages.py [at 631, chr —, ord 151]
Examples\PP3E\Preview\make_db_files.py [at 266, chr –, ord 150]
Examples\PP3E\PyTools\fixnames_all.py [at 500, chr —, ord 151]
Examples\PP3E\System\Processes\fork-count.py [at 217, chr —, ord 151]
"""

import os
srcdir = 'Examples'
ascii  = range(2 ** 7)           # char codes 0..127, else error in 2.5

for (thisDir, subs, filesHere) in os.walk(srcdir):
    for filename in filesHere:
        if filename.endswith('.py') or filename.endswith('.pyw'):
            pathname = os.path.join(thisDir, filename)
            rawtext  = open(pathname, 'rb').read()
            for (index, char) in enumerate(rawtext):
                if ord(char) not in ascii:
                    format = '%s [at %s, chr %s, ord %s]'
                    print format % (pathname, index, char, ord(char))
print 'Finished'

