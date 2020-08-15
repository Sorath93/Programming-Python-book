###############################################################################
# PyMailGui 2.1 - A Python/Tkinter email client.
# A client-side Tkinter-based GUI interface for sending and receiving email.
#
# See the help string in PyMailGuiHelp2.py for usage details, and a list of 
# enhancements in this version.  Version 2.0 is a major rewrite.  The changes
# from 2.0 (July '05) to 2.1 (Jan '06) were quick-access part buttons on View
# windows, threaded loads and deletes of local save-mail files, and checks for
# and recovery from message numbers out-of-synch with mail server inbox on
# deletes, index loads, and message loads.
#
# This file implements the top-level windows and interface.  PyMailGui uses 
# a number of modules that know nothing about this GUI, but perform related 
# tasks, some of which are developed in other sections of the book.  The
# mailconfig module is expanded for this program.
#
# Modules defined elsewhere and reused here:
#
# mailtools (package):
#    server sends and receives, parsing, construction     (client-side chapter)
# threadtools.py
#    thread queue manangement for GUI callbacks           (gui tools chapter)
# windows.py
#    border configuration for top-level windows           (gui tools chapter)
# textEditor.py
#    text widget used in mail view windows, some popups   (gui programs chapter)
#
# Generally useful modules defined here:
#
# popuputil.py
#    help and busy windows, for general use
# messagecache.py
#    a cache that keeps track of mail already loaded
# wraplines.py
#    utility for wrapping long lines of messages
# mailconfig.py
#    user configuration parameters: server names, fonts, etc.
#
# Program-specific modules defined here:
#
# SharedNames.py
#    objects shared between window classes and main file
# ViewWindows.py
#    implementation of view, write, reply, forward windows
# ListWindows.py
#    implementation of mail-server and local-file list windows
# PyMailGuiHelp.py
#    user-visible help text, opened by main window bar
# PyMailGui2.py
#    main, top-level file (run this), with main window types
###############################################################################

import mailconfig, sys
from SharedNames import appname, windows
from ListWindows import PyMailServer, PyMailFile


###############################################################################
# Top-level window classes
# View, Write, Reply, Forward, Help, BusyBox all inherit from PopupWindow
# directly: only usage;  askpassword calls PopupWindow and attaches;  order
# matters here!--PyMail classes redef some method defaults in the Window
# classes, like destroy and okayToExit: must be leftmost;  to use
# PyMailFileWindow standalone, imitate logic in PyMailCommon.onOpenMailFile;
###############################################################################

# uses icon file in cwd or default in tools dir
srvrname = mailconfig.popservername or 'Server'

class PyMailServerWindow(PyMailServer, windows.MainWindow):
    def __init__(self):
        windows.MainWindow.__init__(self, appname, srvrname)
        PyMailServer.__init__(self)

class PyMailServerPopup(PyMailServer, windows.PopupWindow):
    def __init__(self):
        windows.PopupWindow.__init__(self, appname, srvrnane)
        PyMailServer.__init__(self)

class PyMailServerComponent(PyMailServer, windows.ComponentWindow):
    def __init__(self):
        windows.ComponentWindow.__init__(self)
        PyMailServer.__init__(self)

class PyMailFileWindow(PyMailFile, windows.PopupWindow):
    def __init__(self, filename):
        windows.PopupWindow.__init__(self, appname, filename)
        PyMailFile.__init__(self, filename)


###############################################################################
# when run as a top-level program: create main mail-server list window
###############################################################################

if __name__ == '__main__':
    rootwin = PyMailServerWindow()              # open server window
    if sys.argv > 1:
        for savename in sys.argv[1:]:
            rootwin.onOpenMailFile(savename)    # open save file windows (demo)
        rootwin.lift()                          # save files loaded in threads
    rootwin.mainloop()
