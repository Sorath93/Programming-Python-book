About this package
==================

This is a container directory for the entire book examples package.
The PP3E directory here is a Python module package, containing all
source code examples in the book.

Add the name of the directory on your machine that contains PP3E 
(or a copy of it) to your PYTHONPATH setting or ".pth" file entry.
See PP3E/README-PP3E.txt for more details.  To run major Python 
demos from the book without such path configuration, click the 
top-level PP3E/Launch_* scripts directly.  

Note that this directory is just a dummy container, not a package
itself, and so does not require a __init__.py file -- only the PP3E
and below must have __init__.py files, because they are the package
directories listed in import statements.  For more background on 
package directory imports, see the book _Learning Python 2nd Ed__.

Also note that instead of setting your PYTHONPATH (or .pth files)
to include the directory containing the PP3E examples package root,
you can copy the PP3E package root to the site-packages subdirectory
of your Python source library (e.g., to Lib\site-packages\PP3E on
Windows).  Since this directory is automatically added to your 
import search path, this avoids the need for manual configuration,
apart from the copy itself.

This is what a setup.py distutils script would do with it, in fact,
and site-packages is the standard place where 3rd-party Python 
software is installed.  No setup.py is shipped with book examples,
though, because running a copy is no more difficult than running a 
setup.py script, and automaticaly tucking the examples away in 
site-packages was deemed a bit too magical.  Not only is their
location obscured, but because this embeds them in the Python 
install tree, they are prone to accidental erasure should a
prior version of Python be removed.  

Keeping the examples separate from the Python install tree seemed 
like a better approach for book examples, but your milage may vary.
For more details on the distutils system, consult Python's standard
manuals set, at python.org, and in your Windows Start button.


The details: a quick introduction to package imports
====================================================

This directory is simply a dummy container directory for the
PP3E examples module package.  You can copy the PP3E directory
to any other directory on your machine; the directory containing the
PP3E root does not need to be a package itself, and does not need
a __init__.py file, but must be on the module search path (current
directory, PYTHONPATH, or ".pth" file setting).  It's okay if the 
directory you copy PP3E to has other unrelated nested packages and 
modules--as long as that container directory (the one above PP3E)
is on the module search path, Python will find PP3E nested there.

Because Python packages mandate that the search path must list
a directory containing the one you wish to use in import statements,
this extra parent dir level is here just as a convenience.  Package
imports are always relative to an entry on the module search path,
sys.path within Python.

All cross-directory imports in the book examples tree are relative 
to (start at) the PP3E root directory, so you need add only the one
directory containing PP3E on your machine to PYTHONPATH (or other)
setting.  Only imports of modules in the same directory do not go
through PP3E; to import from another directory, all book examples
use the PP3E package (e.g., "from PP3E.System.Filetools...").

The extra PP3E nesting level makes book module imports unique 
across all the Python code installed on your machine--use 
either of these import forms:

    import PP3E.xxx.yyy 
    from PP3E.xxx.yyy import name

to make sure you get book examples.  The top-level root directory 
qualifier makes these paths unique, and avoids import name clashes
among both the book examples and other modules on your machine.

Without the PP3E level, imports may load from a same-named directory
or module elsewhere, depending on your search-path setting.  For 
instance, an import of a nested PP3E package like:

    import Gui.yyy

might mean anything on your computer, and depends completely 
on the order in your module search path.  Without the PP3E root, 
installing another package with a "Gui" root in the path would
mean that either the book examples or the new package would be
broken (one of the two would find the wrong directory).  Moreover,
installing the book examples on the path could break existing
packages that already expect a "Gui" dir--they might see things
nested in PP3E by mistake.  With the PP3E root scheme used, 
neither scenario is possible.

Making all cross-directory imports relative to the PP3E root
also simplifies module import search path settings: you only 
need to a single entry (PP3E's container directory) in order
to gain access to all examples in the book.

For example, you can generally import a module located anywhere
in the examples distribution by using a full path, as long as 
just the directory containing the PP3E examples root directory 
is on your module search path (e.g., the current dir, in PYTHONPATH,
or in a ".pth" file):

    C:\WINDOWS>set PYTHONPATH=C:\Download\Examples
    C:\WINDOWS>python
    >>> from PP3E.Internet.Ftp.getfile import getfile
    >>> getfile(file='index.html',
    ...         site='starship.python.net',
    ...         dir ='public_html',
    ...         user=('lutz', 'xxxxx'))
    Downloading index.html
    Download done.
    >>>
    C:\WINDOWS>dir index.html
    INDEX~1  HTM         1,369  04-28-00 10:24a index.html

Note: If you've received the examples package on a CD, you don't
have to copy PP3E elsewhere (you can simply add PP3E's container
directory in the CD to your path, or click PP3E\Launch_* scripts
without changing your path at all).  Copying to your hard drive,
however, allows Python to cache byte-code ".pyc" files for fast 
startup, and lets you change source code.

Also note: when using import to access packages, you must repeat 
the full path anytime you wish to reference any name within yyy:

    import PP3E.xxx.yyy 
    PP3E.xxx.yyy.name()

To avoid this, use from statements, as long as there is only one 
occurence of "name" among all the modules you load this way:

    from PP3E.xxx.yyy import name
    name()

The "as" extension for imports can shorte3n paths here too, again,
ads long as you don't accidentally redefine the same name twice:

    import PP3E.xxx.yyy as yyy
    yyy.name()

For more details on packages, see _Learning Python 2nd Edition_.
