------------------------------------------------------------------------------
PP3E\README-PP3E.txt
Examples distribution package for _Programming Python, 3rd Edition_

[Do not move this file: Launcher uses it to find the examples root.]

Note: this edition's examples are being made available for download on 
the book's web page on oreilly.com, instead of on an enclosed book CD.   
This policy allows for much more dynamic updates, and avoids any
platform-specific formatting issues.  Given the pervasiveness of 
high-speed Internet access, book CDs are much less common than they 
were when earlier editions of this book were published.

Additionally, related packages such as Python itself are available
for free on the web; please search to find their most recent versions
to install.  This policy was adopted very late in the project, so if
you find any lingering references to a book CD, please read this as 
meaning this examples distribution package available on the web.

This file's contents:

Preface.
1. Running Program Demos
   1A. The easy way: quick-start demos
   1B. The quick guide to installing Python
   1C. Running demos manually
   1D. More about PyDemos and PyGadgets
   1E. More about the Internet Demos
2. Directory Organization
3. Configuration Details
4. Utilities: File Line-end and Permission Conversions
   4A. Converting DOS end-of-line format
   4B. Fixing read-only file permissions
   4C. Other tree maintenance tools
5. Getting Python
6. Updates


------------------------------------------------------------------------------
Preface
------------------------------------------------------------------------------

This file describes how to use the source-code distribution
for the book Programming Python 3rd Edition--all the files in 
and below this directory.

It shows how to run programs, configure your environment, convert files
from DOS to UNIX line-feed format, and install Python.  You need to read
only the first few sections to start running code, but because the 
examples distribution is itself a fairly sophisticated Python software 
system, its structure is worth describing here.

The directory containing this file, named PP3E, has source-code for all
examples in the book.  Examples can be run right from the book's examples
distribution package, or copied to your machine.  To copy to your machine,
copy the entire PP3E directory tree to some directory on your computer, 
and add the name of the directory containing PP3E to your module search 
path (i.e., you PYTHONPATH shell setting, ".pth" files, etc.).

Alternatively, copy the PP3E directory tree to the site-packages folder
in your Python source library (e.g., C:\Python24\Lib\site-packages on 
Windows for Python 2.4).  Because this directory is automatically 
searched on imports, copying here makes PYTHONPATH settings unnecessary.
For more on this, see the distutils note in the ..\README.txt file, one
level up in this tree.

Some scripts can be run without path configuration: see the Launch_* 
scripts description below.  Unless noted otherwise, most filenames in 
this document refer to files in the PP3E directory.



------------------------------------------------------------------------------
1. Running Program Demos
------------------------------------------------------------------------------

This section explains how to run Python demos in this package.


1A. The easy way: quick-start demos
-----------------------------------
If you want to see some Python demos right away, and have access
to an installed Python with the Tkinter extension, you can run
one of the following demo scripts immediately:

    Launch_PyDemos.pyw          (starts the main demo laucher bar)
    Launch_PyGadgets.py         (starts standard utilities)
    Launch_PyGadgets_bar.pyw    (starts a utilities launcher toolbar)
    LaunchBrowser.py            (opens examples index in web browser)

These scripts only require that Python is installed first.  You don't
need to configure your environment first or tweak a Config/setup-pp
file to run them, and they may be run right off the example package (e.g., 
by clicking in them in Windows explorer).  LaunchBrowser will work if 
it can find a web browser on your machine, even if you don't have a 
live Internet link (though some Internet examples' features won't work
completely without a live connection).

Depending on your platform, you can start the scripts above by either:

(1) Double-clicking on the scripts' file names in your file explorer, or
(2) Running the scripts from your system command-line prompt.

The first technique is usually easiest; since Python automatically 
registers itself to open ".py" Python files when installed on Windows,
it just works.  To use the second scheme:

- Start a system command-line shell interface (e.g. a MS-DOS command
  console box on Windows, an xterm window on Linux)
- At the command-line prompt, go to the PP3E examples directory where 
  the files reside (e.g., type  a "cd C:\myexamplesdir\PP3E" command)
- At the command-line prompt, type one of the following commands:

    python Launch_PyDemos.pyw
    python Launch_PyGadgets.py
    python Launch_PyGadgets_bar.pyw
    python LaunchBrowser.py

You may need to replace 'python' with the full path to your Python
program if it is not in a directory already on your PATH setting (for
2.4, it is probably at C:\Python24\python on Windows).

All three of these Launch_* scripts are self-configuring.  They assume 
you have already installed Python (they're written in Python, afterall), 
but they automatically locate your Python program and examples root 
directory, and configure the Python module and system search paths as 
needed to run the book examples.  The Launch scripts should work both 
straight off the example package, or after copying the examples directory
to your hard drive; see comments in file Launcher.py for more details.


1B. The quick guide to installing Python
----------------------------------------
To run Python demos on your machine, you first need a Python interpreter.
On Windows, if there is no Python on your computer (check the Programs
entry in your Start button), there is a fully executable Python with Tk GUI 
support available at www.python.org.  It's packaged as a self-installer
program, so it's essentially just a double-click to install.  In more detail, 
here is the Python installation procedure: 

(1) Fetch the Windows installer for Python at the "Downloads" like at 
    www.python.org; for 2.4/2.5 releases, it's a ".msi" self-installer.
(2) Navigate to downloaded installer file, unless your browser prompts
    you to open it immediately after the download. 
(3) Open the installer, or double-click on the "*.msi" file you fetched
    (the self-install program)
(4) Answer 'yes', 'next', 'default', or 'continue' to all the questions
    you will be asked while the installer runs (that is, a default install).
    Tk GUI support is automaticaly installed along with Python.

Once that's finished, you have a Python on your box; you can tell because
there will be Python intry in the programs menu in your Start button.  Now,
go click on the Launch_PyDemos.pyw file icon in the example package's 
top-level Examples\PP3E directory to start some Python demos right away.
When you're ready, read on in this file to find out how to configure your
environment permanently, for faster start-ups.

On Mac OS X, UNIX and Linux, you probably already have a Python 
installed (it comes standard on Macs and most Linux), but you can also
install Python from Linux RPM files, or build Python from its source code 
packages available at www.python.org.  To build from the source, ungzip,
untar, config, and make.  LInux users: if your Python does not have Tk
GUI support preinstalled, try a "yum tkinter" command to fetch it.

Note that although the book's examples were only verified to run under 
Python 2.4 and 2.5, the latest Python is generally the best Python: you
can always fetch the current release from www.python.org.  If newer
release break examples over time, patches will be posted at the book's
update pages, and within this examples distribution package.


1C. Running demos manually
--------------------------
You can also run the demo scripts by typing these command lines, after 
cd'ing to the PP3E directory where your example files reside:

    Config\setup-pp.bat     (or "source Config\setup-pp.csh" on Linux)
    python PyDemos.pyw      (start main demo bar interface)

Or one of these:
    python PyGadgets.py
    python PyGadgets_bar.pyw

You'll want to change some of the settings in setup-pp.bat to reflect
directories on your own machine, and may want to invoke setup-pp.bat
in your C:\autoexec.bat so its settings are always available (for 
Linux users: make that setup-pp.csh and your ~/.cshrc instead).  The
advantage of this scheme is that it avoids the search and configuration 
steps performed by the Launch_* scripts mentioned above, and so may
start a bit faster.

PyDemos starts an interface from which you can run many of the 
larger GUI-based examples that appear in the book.  Since most 
of the examples are scattered throughout the PP2E subdirectories,
this file also serves as a quick locator for major GUI examples.
In this 3rd Edition, PyDemos also has buttons which pop up the 
source code files for its example programs in text edit windows.

Another top-level script, PyGadgets.py can be started similarly; 
it runs a handful of programs in non-demo mode.  Its relative,
PyGadgets_bar.pyw pops up a button bar to start gadgets on demand.
You can find screen shots of these demo programs in action in the 
book's Preface.

The Internet examples on the PyDemos bar are started with the 
LaunchBrowser.py script, which tries to also find a web browser
on your machine; see that script for more details.  If you start
LaunchBrowser.py directly, it brings up the PyInternetDemos.html
root page by opening a local file on your machine.  In general, 
here are the major top-level programs in the PP3E directory:

PyDemos2.pyw
    Button bar for starting and viewing major GUI and Web examples 
PyGadgets.py
    Starts programs in non-demo mode for regular use 
PyGadgets_bar.pyw
    Button bar for starting PyGadgets programs on demand 
Launcher.py
    To start programs without environment settings--finds 
    Python, sets PYTHONPATH, spawns Python programs
Launch_*.py*
    Start PyDemos and PyGadgets with Launcher.py--run these 
    for a quick look without manual configuration
LaunchBrowser.py 
    Opens example web pages with an automatically-located web
    browser, either live on the net, or local web page files

Please note that all of the launcher and demo scripts are written to be
portable, but they have only been tested on Windows and Linux at this 
time.  Tk also works on the Mac (classic, and OSX on both Aqua and X),
and Python runs on almost every platform in existence.  These scripts may
require minor changes on some platforms, and may need to be configured a
bit for unique machine set-ups; see the system interfaces part of the 
text for background details and source code listings.


1D. More about PyDemos and PyGadgets
------------------------------------
Among other things, PyDemos lets you start a clock, calculator, image
viewer, drawing tool, text-editor, slideshow, and N-across game, all 
coded in Python.  It also source code view buttons, and includes buttons
which attempt to start a web browser and server automatically for the 
major Internet example start pages.  See file PyDemos.pyw for more 
details about the launcher, and see the book for more details about the
demo programs.

Depending on your system's configuration, you may also be able to
run the PyDemos.pyw file by double-clicking on it in your system's
file browser.  If you can't make it work using a command-line or
double click, you may need to load one of the "Config\setup" files 
first, to set the module search path; see the "Configuration" section 
below and file PyDemos.pyw for details.  

To make the demos easily accessible, you can also drag out a 
double-clickable shortcut to PyDemos.pyw (or Launch_PyDemos.pyw) onto
your Windows desktop (shortcuts work on other platforms as well, though
this is very platform specific).  The PyGadgets script starts a subset 
of the programs the PyDemos can; PyGadgets starts programs for real use,
not demonstration.


1E. More about the Internet Demos
---------------------------------
Finally, if you don't have a Python with Tkinter installed (or don't
have Python at all, for that matter), you may also run the book's 
browser-based Internet examples.  In this 3rd Edition, these examples
are not maintained at a web site, but may be run by launching a web 
server locally on your machine.  See the server-side scripting chapter
in the book for details.  

The PyDemos script attempts to spawn a locally running web server coded
in Python, to handle page requests from a spawned web browser.  To
diable this, see the '-file' and '-live' switches in the script's code.

It is possible to upload the book's web examples to a remote site, 
provided there is a web server there which supports Python-coded CGI
scripts.  Among other things, the web-based book examples include CGI
tutorial scripts and an email client.  

Naturally, many examples in the book aren't GUI or browser-based; see 
the text and PP3E directory for additional example files, C extension
build scripts, and so on.



------------------------------------------------------------------------------
2. Directory Organization
------------------------------------------------------------------------------

The example files in this distribution are organized by major topics
in the book (one directory for Internet code, one for System examples,
and so on).  The subdirectories within each topics directory usually 
correspond to a particular section or chapter in the book (e.g., the
Internet\Sockets directory contains Network Scripting chapter code).
See the "*.txt" files at the top of subdirectories for more pointers.
There is also a top-level PyTools directory in PP3E, which contains
Python scripts used to manage the entire tree (described ahead).

Most example tree directories are module packages, to allow qualified
cross-directory imports.  __init__.py files identify a containing 
directory as a Python module package, and so allow it to be listed in a
script's import statements.  In fact, the entire examples distribution 
is one module package, to make it easy for examples to specify modules 
used elsewhere in the book, and to avoid filename clashes with other 
Python code on your system.  

In general, imports in all examples either refer to a file in the same 
directory as the importer, or are fully-qualified package import paths 
rooted at PP3E.  For instance, if an example in PP3E\Integrate\Extend
uses a module defined in PP3E\Gui, it runs an import of one of these 
forms: 

in PP3E\Integrate\Extend\somefile.py:
    import PP3E.Gui.somemodule
    from   PP3E.Gui.somemodule import name

Your code outside the examples tree can do likewise to reuse example code.
No book tree directories other than PP3E are added to the module search path
setting (e.g., PYTHONPATH, ".pth" files).  This is by design: although adding
nested subdirectories may allow simpler imports like:

    import Gui.somemodule
    import somemodule

this would also cause potential name clashes if you install another 
package with a "Gui" package directory or "somemodule" name--either the 
book examples or that other package would find the wrong code.  This 
would  also make the search path, and its configuration, more complex.

By placing all book examples under the PP3E directory, and making all
cross-directory imports relative to this root, such module name clashes
are avoided.  Because of this structure, the examples directory is fairly
self-contained, but the module search path must generally include the  
name of the directory containing the PP3E directory. 

See also file ..\README-root.txt (that is, in the parent directoy of PP3E)
for more details on Python package imports.



------------------------------------------------------------------------------
3. Configuration Details
------------------------------------------------------------------------------

Because the PP3E examples directory is used as a module package library 
by various programs, you will eventually want to set your PYTHONPATH (or 
".pth" file entries) to find it correctly in the module search path.  
Here's what I used while developing the book:

  Config\setup-pp.bat: 
    On MS-Windows, you can run setup-pp.bat from your c:\autoexec.bat file, 
    to setup the Python module search path.  On NT and later, you may also be 
    able to set these variables in the system settings dialog (see below).
    Change PP3EHOME to the directory containing the PP3E examples directory.
    This adds only one directory to PYTHONPATH (the one containing PP3E).

  Config\setup-pp.csh:
    The equivalent of setup-pp.bat, but for Unix and Linux systems.
    Add it to or run it from your .login or .cshrc file to make these
    settings always available. Note that you may need to first translate
    this to your system shell's syntax (if you don't use csh), and might
    need to convert to Unix line-ends; see this file for details.

  Config\setup-pp-embed.csh
    Extra path settings which may need to be source'd on Linux and UNIX 
    platforms to get the Python-in-C embedding examples to work (required 
    for embedding examples only: setup-pp.csh is sufficient for all others).

  Config\autoexec.bat (copy of my A:\autoexec.bat on Windows)
  Config\.cshrc       (copy of my ~/.cshrc on Linux)
    Top-level system configuration files I use on my Windows and Linux
    machines.  They invoke setup-pp* files on system start-up; .cshrc adds
    a few extra setting on Linux.  Use, copy, and tweak as appropriate.

  Launch_*
  LaunchBrowser.py:
    These Python scripts are used to start book examples even if you have 
    not configured one of the setup-pp files yet; they automatically find
    paths and configure PYTHONPATH, and locate a web browser on your 
    machine.  They are an option to the Config files; see above for details.

The settings in the setup-pp files are not necessarily the only ways
to configure the module search path.  In general, you can either 
be more specific in PYTHONPATH, or in package qualifier lists 
within programs.  In some cases, the choice is arbitrary, since 
I've added __init__.py files at multiple levels in a directory 
path, but be careful about adding PP3E subdirectpries to your
PYTHONPATH--it can lead to name clases with other installed files.

I should add that the browser-based internet examples show up in
the PP3E\Internet\Web directory in this distribution, but they can
also live in a top-level account directory on a server machine.
You can run the CGI script examples out of the PP3E directory 
itself, but only if you start a webbrowser listening on "localhost"
and running out of the Web directory (see the preview and
server-side scripting chapters for a script which can do this).  
Otherwise, some extra copying and configuration will be needed, 
due to the special requirements of CGI scripts. The 
PP3E\Internet\Web directory here could be uploaded to the 
public_html directory on some server machines, for instance.

Speaking of which: I used (at least) 3 platforms to develop the 
examples in this book.  For instance, Tkinter examples were developed
on Windows XP and later run on Linux, Python/C integration code was 
developed on Red Hat Linux, and Internet work was done on Linux and 
other Unix server machines.  

(For this 3rd Edition, I used Windows for almost everything, with Cygwin
for C and Unix-based examples, and a Python-coded and locally-running web
server for web examples; a Zaurus Linux PDA was employed occasionally).

Your configuration details will probably vary, but should be similar; 
PYTHONPATH works the same on all Pythons.  On some platforms, though, 
there are other ways to set the search path.  Here are a few 
platform-specific hints:

Windows port
    The Windows port allows the Windows registry to be used, in addition 
    to setting PYTHONPATH in DOS.  On recent versions of Windows, rather 
    than changing C:\autoexec.bat and rebooting, you can may also set your
    path by selecting the Control Panel, picking the System icon, clicking
    on the Advanced/Environment Settings tab, and typing PYTHONPATH and 
    the path you want (e.g., C:\mypythondir) in the resulting dialog box.
    Such settings are permanent, just like autoexec.bat, and are picked
    up the next time you start a Python session or script.

Jython
    Under Jython, the Java implementation of Python, the path may take 
    the form of -Dpath command-line arguments on the Java command used 
    to launch a program, or python.path assignments in Java registry files. 
    See Jython documentation for more details.



------------------------------------------------------------------------------
4. Utilities: File Line-end and Permission Conversions
------------------------------------------------------------------------------

This section describes some useful utilities in PP3E\PyTools.


4A. Converting DOS end-of-line format
-------------------------------------
For simplicity, I am no longer shipping two copies of the examples tree 
(one in MS-DOS \r\n line-end format, one in Unix \n line-end format).  
Instead, the examples package contains a single copy of the tree in 
MS-DOS format, along with a portable Python script for converting all 
text files in the tree to and from Unix line-end format automatically.

See the Systems chapter for background details on the format difference.
You probably don't care because most text editors do the right thing with
either form, with a few notable exceptions.  If these files look like 
one long line on Windows or if you see odd characters at the end of lines
under UNIX/Linux, you can convert all the text files in this distribution
to one or the other format all at once, by doing this:

1) Install Python if you haven't already (described easrlier)
2) Copy the PP3E root directory to your hard-drive
3) Double-click on the copied file PP3E\tounix.py in a file explorer

   or
   3) cd to the copied PP3E root directory in a console/shell
   4) Type command "python PyTools/fixeoln_all.py tounix"
      or
   4) Type command "python tounix.py" (this simply runs fixeoln_all.py)

Change "tounix" to "todos" in all of the above to convert to MS-DOS 
end-of-line format instead.  The fixeoln_all.py script runs a find to 
locate all text files and converts those that need to be converted to
the target linefeed format.  It can be run over and over without 
problems--it converts only files and lines that need conversion, so
it won't trash files already in the target format.

Also note that files run as executable programs (using the #! trick)
or installed on web servers sometimes must be converted from DOS
to Unix line-feed format to work properly (this may vary a bit).
If in doubt, always run the tounix.py conversion utility over the 
whole examples tree as described above, after copying it onto a 
Unix or Linux machine.


4B. Fixing read-only file permissions
-------------------------------------
If you copy the examples off of a CD-ROM using standard Windows 
drag-and-drop, they may be stored on your hard drive with read-only
persmission settings on some platforms (since that's what they are
marked as on the CD).  That makes it difficult to edit and change them
on your machine.  If your files are not writeable after copying off
a CD, bring up a DOS console box (or equivalent), go to the top
level PP3E example directory in your hard-drive copy (with a cd 
command), and type either of these command lines:

    python towriteable.py
    python PyTools\fixreadonly-all.py

You may also double-click towriteable (it runs fixreadonly-all).
This automatically makes all example files in the distribution's
directory tree writeable.  You have to install Python before running 
this Python script, of course.  See the system examples chapters for 
more details on how this script does its work.  On Unix and Linux, you 
can also fix permissions with a "find" command that does a "chmod" 
to each file, but the Python script above is more portable.


4C. Other tree maintenance tools
--------------------------------
In general, there are a handful of commonly-useful utilities in 
the PP3E\PyTools subdirectory of this distribution:

  fixeoln_all.py: 
     Described above: Convert to/from Unix-style line terminators, so 
     you can use standard text file editors on the target platform.

  fixreadonly-all.py
     Described above: Make all files in a tree writeable again if a 
     drag-and-drop copy marks them as read-only.

  cleanpyc-py.py
     Remove all '*.pyc' byte-code files in a directory tree. 
     Useful for cleaning up before shipping source code files,
     and for removing old .pyc files left from a prior Python
     release (in case they are no longer forward compatible, and
     in case the book examples ship with any lurking pyc files).
     Run like this in PP3E dir: python PyTools\cleanpyc-py.py

  fixnames_all.py
     Tries to repair file names that became all upper-case in 
     transit.  You shouldn't need it (old DOS-style names in this 
     distribution were fixed with this script awhile ago), but 
     if you ever do, you know where to look.  By convention, 
     simple files in the distribution start with a lower case 
     letter; directories start with an upper case.

  search_all.py
     Find all files in the examples distribution containing a 
     given string, portably.  Related tools: see scripts for 
     comparing and copying directory trees in the System examples
     directory; see scripts for installing CGI scripts and fixing
     the site name in web examples in the Internet directory; see
     PyTools\visitor_edit.py to automatically edit matched files.

  renamer.py: 
     Change file names to lower case in one dir, in order to avoid 
     case-sensitive file system issues; you may also need to change
     import statements if you do this, and should  probably use the
     newer script tree-wide fixnames_all.py instead.



-------------------------------------------------------------------------------
5. Getting Python
-------------------------------------------------------------------------------

If you have access to an already-installed Python, skip this 
section.  If not, you can find the latest Python release at 
the Downloads link at www.python.org.  Here is a quick overview 
of what to get, and where to get it:

- If you're using a MS-Windows machine, I recommend the standard
  Python+Tk package currently available at www.python.org, for this
  book.  It's a self-installing executable that you simply download
  and double-click to install.  This package includes the latest
  Python release, the Tkinter GUI extension (and all required Tcl/Tk
  components), the IDLE development GUI, DBM file support, 
  and standard extensions.
  
  If you'll be using Windows-specific extensions (e.g., COM), you 
  will probably want to install the PyWin32 extension package too
  (formerly known as win32all, and sometimes inaccurately called 
  PythonWin); it includes Windows-specific tools that supplement the 
  standard Windows Python install, and is also available via a link 
  or search at www.python.org.  See the Downloads link at the top of
  www.python.org for both Windows packages.  It's possible to build 
  Python from its source code on Windows, but I won't describe how here.

  Finally, you can also find both Python and the Windows extensions
  in other distributions, such as the ActivePython distribution 
  available from ActiveState (see www.activestate.com for details).
  ActiveState also provides additional Windows tools for Python.

- If you're using a Linux machine, chances are that Python is 
  already availble on your system.  It may or may not have Tkinter
  support, though.  If you need to add Tkinter, try fetching the 
  latest Python Linux RPM from www.python.org (see the Downloads 
  link at the top of that page).  Then, run the appropriate 'rpm'
  command on your machine to install.  You can also fetch the full
  Python source-code package from www.python.org, ungzip, untar,
  and build with 'config' and 'make' commands.  You'll probably
  want to edit Python's Modules/Setup to enable the Tkinter 
  extension and re-make too.  See the Extending chapter for details.
  Alternatively, try a "yum tkinter" command to install the GUI 
  support, provided you have this.

- If you're on a Unix machine, the usual install procedure is to
  fetch and build the full source-code distribution, as described
  above for Linux.

- If you're on a Macintosh OS X machine, you already have an
  installed Python.  Tkinter support may or may not be present;
  if not, consult www.python.org to find the extension download.
  In most cases, when I describe configuration for UNIX, it applies
  to your machine as well.  Tkinter may be run on Aqua or X-windows
  on the Mac.

- If you're using a class Mac, please see the Mac-specific information
  at www.python.org (sorry; I don't use a Mac, so I'm not inclined
  to tell you how you should).  

- If you're on other platforms, see www.python.org too; chances are 
  you'll want to build from the source dustribution, but there other 
  packages and documentation for various platforms at Python's web site
  (e.g., PalmOS, PocketPC, Zaurus, Amiga, DOS, OS/2, etc.).  Ports for
  devices such as handhelds and game consoles are available via links
  or searches at www.python.org.  Additionally, you can find a Python 
  for Nokia cellphones and their Symbian OS, Ipods, and more; as always,
  Goggle.com is your first resource.



------------------------------------------------------------------------------
6. Updates
------------------------------------------------------------------------------

Watch for updates, supplements, and patches, at this site:

    http://www.rmi.net/~lutz/about-pp3e.html

O'Reilly's page forn this book will also track book errata:

    http://www.python.org
    http://www.oreilly.com

Changes to this examples distribution package for bugs, enhancements,
or changes required for new Python releases, will be logged in the 
Updates.txt files two level up in this tree.

Happy Pythoneering,

--Mark Lutz, September 2006

