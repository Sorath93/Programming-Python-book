##############################################################################
# objects shared by all window classes and main file: program-wide globals
##############################################################################

# used in all window, icon titles
appname  = 'PyMailGUI 2.1'       

# used for list save, open, delete; also for sent messages file
saveMailSeparator = 'PyMailGUI' + ('-'*60) + 'PyMailGUI\n'

# currently viewed mail save files; also for sent-mail file
openSaveFiles     = {}                  # 1 window per file,{name:win}

# standard library services
import sys, os, email, webbrowser
from Tkinter       import *
from tkFileDialog  import SaveAs, Open, Directory
from tkMessageBox  import showinfo, showerror, askyesno

# reuse book examples
from PP3E.Gui.Tools      import windows      # window border, exit protocols
from PP3E.Gui.Tools      import threadtools  # thread callback queue checker
from PP3E.Internet.Email import mailtools    # load,send,parse,build utilities
from PP3E.Gui.TextEditor import textEditor   # component and popup

# modules defined here
import mailconfig                            # user params: servers, fonts, etc
import popuputil                             # help, busy, passwd popup windows
import wraplines                             # wrap long message lines
import messagecache                          # rememeber already-loaded mail
import PyMailGuiHelp                         # user documentation

def printStack(exc_info):
    # debugging: show exception and stack traceback on stdout
    print exc_info[0]
    print exc_info[1]
    import traceback
    traceback.print_tb(exc_info[2], file=sys.stdout)

# thread busy counters for threads run by this GUI
# sendingBusy shared by all send windows, used by main window quit

loadingHdrsBusy = threadtools.ThreadCounter()   # only 1
deletingBusy    = threadtools.ThreadCounter()   # only 1
loadingMsgsBusy = threadtools.ThreadCounter()   # poss many
sendingBusy     = threadtools.ThreadCounter()   # poss many
