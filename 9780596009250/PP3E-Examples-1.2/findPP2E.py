"""
Script used to lingering occurrence of "PP2E" in release 1.1 of the
examples release; the full list of files having "PP2E" in 1.1 appears
below -- although all were fixed in 1.2, all but one of these were
either extra examples that do not appear in the book, or examples that
correctly use "PP3E" in the book but not in the examples release tree;
the only example the used "PP2E" in both the book and the examples tree
was Examples\PP3E\PyDemos2.pyw, in a lable for the 'info' popup window:   
"""

import os
srcdir = 'Examples'

for (thisDir, subs, filesHere) in os.walk(srcdir):
    for filename in filesHere:
        if filename.endswith('.py') or filename.endswith('.pyw'):
            pathname = os.path.join(thisDir, filename)
            rawtext  = open(pathname, 'rb').read()
            index    = rawtext.find('PP2E')
            if index != -1:
                format = '%s [at %s]'
                print format % (pathname, index)

"""
[All "PP2E" found in 1.1:]
Examples\PP3E\PyDemos2.pyw [at 2210]                                FIXED: info popup title, bad in book
Examples\PP3E\Dstruct\TreeView\alts\treeview_left.py [at 1456]      fixed: extra example
Examples\PP3E\Dstruct\TreeView\alts\treeview_subclass.py [at 4334]  fixed: extra example
Examples\PP3E\Gui\TextEditor\textEditor.py [at 895]                 ok:    comment text
Examples\PP3E\Integrate\Extend\Stacks\exttime.py [at 139]           fixed: ok in book
Examples\PP3E\Internet\Web\PyErrata\browse.py [at 3182]             n/a:   old example
Examples\PP3E\Internet\Web\PyErrata\submit.py [at 1266]             n/a:   old example
Examples\PP3E\Internet\Web\PyErrata\AdminTools\temp\browse-alt1.py  n/a:   old example 
Examples\PP3E\PyTools\visitor_poundbang.py [at 633]                 fixed: ok in book
Examples\PP3E\PyTools\wcall_find.py [at 251]                        fixed: ok in book
Examples\PP3E\PyTools\wcall_find_patt.py [at 248]                   fixed: ok in book
Examples\PP3E\PyTools\wcall_visitor.py [at 248]                     fixed: ok in book
Examples\PP3E\System\App\apptools.py [at 236]                       fixed: extra example
Examples\PP3E\System\App\Clients\mtool3.py [at 524]                 fixed: extra example
Examples\PP3E\System\App\Clients\mtoolapp.py [at 995]               fixed: extra example
Examples\PP3E\System\App\Clients\myapp.py [at 32]                   fixed: extra example
Examples\PP3E\System\App\Clients\myapp2.py [at 32]                  fixed: extra example
Examples\PP3E\System\App\Clients\myapp4.py [at 58]                  fixed: extra example
Examples\PP3E\System\App\Clients\tools.py [at 176]                  fixed: extra example
Examples\PP3E\System\App\Clients\tools2.py [at 185]                 fixed: extra example
Examples\PP3E\System\App\Clients\unpackapp2.py [at 338]             fixed: extra example
Examples\PP3E\System\App\Kinds\interact.py [at 257]                 fixed: extra example
Examples\PP3E\System\App\Kinds\internal.py [at 251]                 fixed: extra example         
Examples\PP3E\System\App\Tests\apptest.py [at 417]                  fixed: extra example
"""
