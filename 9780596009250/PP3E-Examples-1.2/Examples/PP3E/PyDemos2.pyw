################################################################################
# PyDemos2.pyw
# Programming Python, 2nd and 3rd Edition (PP3E), 1999--2006
# Version 2.0, March '06: add source-code file viewer buttons, new demos
# (PyPhoto, PyMailGUI2), spawn locally-running web server for browser-based
# demos, window icons, and probably other things I've forgotten :-).
#
# Launch major Python+Tk GUI examples from the book, in a platform-neutral way.
# This file also serves as an index to major program examples, though many book
# examples aren't GUI-based, and so aren't listed here (e.g., see the Cygwin
# gcc makefiles in the Integration directory for C integration code pointers).
# Also see:
#
# - PyGadgets.py, a simpler script for starting programs in non-demo mode
#   that you wish to use on a regular basis 
# - PyGadgets_bar.pyw, which creates a button bar for starting all PyGadgets
#   programs on demand, not all at once 
# - Launcher.py for starting programs without environment settings--finds
#   Python, sets PYTHONPATH, etc.
# - Launch_*.py for starting PyDemos and PyGadgets with Launcher.py--run these
#   for a quick look
# - LaunchBrowser.py for running example web pages with an automatically
#   located web browser
# - README-PP3E.txt, for general examples information
#
# This program tries to start a locally running web server and web browser 
# automatically, for web-based denmos.  Additional program comments
# were moved to file PyDemos.doc.txt
################################################################################

import sys, time, os, glob, launchmodes
from Tkinter import *

# -live loads root pages from server so CGIs run, -file loads local files
InternetMode = '-live'

################################################################################
# start building main gui windows
################################################################################

from PP3E.Gui.Tools.windows import MainWindow    # a Tk with icon, title, quit
from PP3E.Gui.Tools.windows import PopupWindow   # same but Toplevel, diff quit
Root = MainWindow('PP3E Demos 2.0')

# build message window
Stat = PopupWindow('PP3E demo info')
Stat.protocol('WM_DELETE_WINDOW', lambda:0)    # ignore wm delete

Info = Label(Stat, text = 'Select demo',
             font=('courier', 20, 'italic'), padx=12, pady=12, bg='lightblue')
Info.pack(expand=YES, fill=BOTH)

################################################################################
# add launcher buttons with callback objects
################################################################################

from PP3E.Gui.TextEditor.textEditor import TextEditorMainPopup

# demo launcher class
class Launcher(launchmodes.PortableLauncher):    # use wrapped launcher class
    def announce(self, text):                    # customize to set GUI label
        Info.config(text=text)

def viewer(sources):
    for filename in sources:
        TextEditorMainPopup(Root, filename)      # as popup in this process

def demoButton(name, what, doit, code):
    rowfrm = Frame(Root)
    rowfrm.pack(side=TOP, expand=YES, fill=BOTH)

    b = Button(rowfrm, bg='navy', fg='white', relief=RIDGE, border=4)
    b.config(text=name, width=20, command=Launcher(what, doit))
    b.pack(side=LEFT, expand=YES, fill=BOTH)

    b = Button(rowfrm, bg='beige', fg='navy')
    b.config(text='code', command=(lambda: viewer(code)))
    b.pack(side=LEFT, fill=BOTH)

# some imported module source files could be determined
# but we can't know where to stop on the import chains 

################################################################################
# Tkinter GUI demos - some use network connections
################################################################################

demoButton(name='PyEdit',        
           what='Text file editor',                            # edit myself
           doit='Gui/TextEditor/textEditor.py PyDemos2.pyw',   # assume in cwd
           code=['Gui/Tools/guimaker.py',                      # show viewer
                 'Gui/TextEditor/textEditor.py'])

demoButton(name='PyView',        
           what='Image slideshow, plus note editor',
           doit='Gui/SlideShow/slideShowPlus.py Gui/gifs',
           code=['Gui/Texteditor/textEditor.py',
                 'Gui/SlideShow/slideShowPlus.py',
                 'Gui/SlideShow/slideShow.py'])

demoButton(name='PyDraw',                    
           what='Draw and move graphics objects', 
           doit='Gui/MovingPics/movingpics.py Gui/gifs',
           code=['Gui/MovingPics/movingpics.py']) 

demoButton(name='PyTree',                              
           what='Tree data structure viewer',
           doit='Dstruct/TreeView/treeview.py',
           code=['Dstruct/TreeView/treeview.py',
                 'Dstruct/TreeView/treeview_wrappers.py',
                 'Dstruct/Classics/btree.py',
                 'Lang/Parser/parser2.py'])

demoButton(name='PyClock',                             
           what='Analog/digital clocks',
           doit='Gui/Clock/clockStyles.py Gui/gifs',
           code=['Gui/Tools/windows.py',
                 'Gui/Clock/clockStyles.py',
                 'Gui/Clock/clock.py'])   

demoButton(name='PyToe',     
           what='Tic-tac-toe game (AI)',
           doit='Ai/TicTacToe/tictactoe.py',
           code=['Ai/TicTacToe/tictactoe.py',
                 'Ai/TicTacToe/tictactoe_lists.py'])

demoButton(name='PyForm',                              # view in-memory dict
           what='Persistent table viewer/editor',      # or cwd shelve of class
           doit='Dbase/TableBrowser/formgui.py',       # 0=do not reinit shelve
          #doit='Dbase/TableBrowser/formtable.py  shelve 0 pyformData-1.5.2', 
          #doit='Dbase/TableBrowser/formtable.py  shelve 1 pyformData',
           code=['Dbase/testdata.py',
                 'Dbase/TableBrowser/formgui.py',
                 'Dbase/TableBrowser/formtable.py'])

demoButton(name='PyCalc',    
           what='Calculator, plus extensions',
           doit='Lang/Calculator/calculator_plusplus.py',
           code=['Lang/Calculator/calculator_plusplus.py',
                 'Lang/Calculator/calculator_plus_ext.py',
                 'Lang/Calculator/calculator_plus_emb.py',
                 'Lang/Calculator/calculator.py'])

demoButton(name='PyFtp',
           what='Python+Tk ftp clients',
           doit='Internet/Ftp/PyFtpGui.pyw',
           code=['Internet/Ftp/PyFtpGui.pyw',
                 'Internet/Ftp/getfilegui.py',
                 'Internet/Ftp/putfilegui.py',
                 'Internet/Ftp/getfile.py',
                 'Internet/Ftp/putfile.py',
                 'Internet/Sockets/form.py'])

# caveat: PyPhoto requires PIL to be installed: show note
demoButton(name='PyPhoto',    
           what='PIL thumbnail image viewer',
           doit='Gui/PIL/pyphoto1.py Gui/PIL/images',     # script, image dir
           code=['PyDemos-pil-note.txt',
                 'Gui/PIL/viewer_thumbs.py',
                 'Gui/PIL/pyphoto1.py'])

# get pymailgui source files
locat  = 'Internet/Email'
locat2 = locat + '/PyMailGui'
saved  = '%s/SavedMail/savemany.txt %s/SavedMail/savefew.txt' % (locat2, locat2)
source = glob.glob(locat + '/PyMailGui/*.py') # 9 source files here + __init__
source+= glob.glob(locat + '/mailtools/*.py') # 4 source files here + __init__

demoButton(name='PyMailGUI2',  
           what='Python+Tk pop/smtp email client',          # open on save file
           doit='%s/PyMailGui2.py %s' % (locat2, saved),
           code=(['Gui/Texteditor/textEditor.py',
                  'Gui/Tools/windows.py',
                  'Gui/Tools/threadtools.py'] + source) )

################################################################################
# web-based demos - PyInternet opens many smaller demos
################################################################################

# get pymailcgi source files - not incl mailtools!
pymailcgifiles = (['Internet/Web/PyMailCgi/pymailcgi.html'] +
                  glob.glob('Internet/Web/PyMailCgi/cgi-bin/*.py'))  # 11 .py

if InternetMode == '-file':
    pagepath = os.getcwd() + '/Internet/Web'
    
    demoButton('PyMailCGI2',
               'Browser-based pop/smtp email interface',
               'LaunchBrowser.pyw -file %s/PyMailCgi/pymailcgi.html' % pagepath,
               pymailcgifiles)

    demoButton('PyInternet',
               'Internet-based demo launcher page',
               'LaunchBrowser.pyw -file %s/PyInternetDemos.html' % pagepath,
               ['Internet/Cgi-Web/PyInternetDemos.html'])

else:
    def startLocalWebServers():
        """
        on Windows succeeds silently if server already listening
        on the port; caveat: should only run 1 server per port;
        global per-process flag won't fix: the servers live on
        """
        launchmodes.PortableLauncher('server80',
            'Internet/Web/webserver.py Internet/Web')()
        launchmodes.PortableLauncher('server8000',
            'Internet/Web/webserver.py Internet/Web/PyMailCgi 8000')()

    site = 'localhost:%s'
    startLocalWebServers()  # run webserver on port 80 and 8000 on localhost
    print 'servers started' 

    # PyErrata removed in 3rd Ed
    
    demoButton('PyMailCGI2',
               'Browser-based pop/smtp email interface',
               'LaunchBrowser.pyw -live pymailcgi.html '+ (site % 8000),
               pymailcgifiles)

    demoButton('PyInternet',
               'Main Internet demos launcher page',
               'LaunchBrowser.pyw -live PyInternetDemos.html ' + (site % 80),
               ['LaunchBrowser.pyw',
                'launchmodes.py',
                'Launcher.py',
                'Internet/Web/PyInternetDemos.html'])

#To try: bind mouse entry events to change info text when over a button
#See also: site http://starship.python.net/~lutz/PyInternetDemos.html

################################################################################
# toggle info message box font once a second
################################################################################

def refreshMe(info, ncall):
    slant = ['normal', 'italic', 'bold', 'bold italic'][ncall % 4]
    info.config(font=('courier', 20, slant))
    Root.after(1000, (lambda: refreshMe(info, ncall+1)) )

################################################################################
# unhide/hide status box on info clicks
################################################################################

Stat.iconify()
def onInfo():
    if Stat.state() == 'iconic':
        Stat.deiconify()
    else:
        Stat.iconify()  # was 'normal'

################################################################################
# popup a few web link buttons if connected
################################################################################

radiovar = StringVar() # use a global

def onLinks():
    popup = PopupWindow('PP3E web site links')
    links = [("Book", 
                   'LaunchBrowser.pyw -live about-pp.html www.rmi.net/~lutz'),
             ("Python",   
                   'LaunchBrowser.pyw -live index.html www.python.org'),
             ("O'Reilly", 
                   'LaunchBrowser.pyw -live index.html www.oreilly.com'),
             ("Author",   
                   'LaunchBrowser.pyw -live index.html www.rmi.net/~lutz')]

    for (name, command) in links:
        callback = Launcher((name + "'s web site"), command)
        link = Radiobutton(popup, text=name, command=callback)
        link.config(relief=GROOVE, variable=radiovar, value=name)
        link.pack(side=LEFT, expand=YES, fill=BOTH)
    Button(popup, text='Quit', command=popup.destroy).pack(expand=YES,fill=BOTH)

    if InternetMode != '-live':
        from tkMessageBox import showwarning
        showwarning('PP3E Demos', 'Web links require an Internet connection')

################################################################################
# finish building main gui, start event loop
################################################################################

Button(Root, text='Info',  command=onInfo).pack(side=TOP, fill=X)
Button(Root, text='Links', command=onLinks).pack(side=TOP, fill=X)
Button(Root, text='Quit',  command=Root.quit).pack(side=BOTTOM, fill=X)
refreshMe(Info, 0)  # start toggling
Root.mainloop()
