###############################################################################
# PyaMailGUI user configuration settings.
# Email scripts get their server names and other email config options from
# this module: change me to reflect your machine names, sig, and preferences.
# Warning: PyMailGUI won't run without most variables here: make a backup copy!
# Notes: could get some settings from the command line too, and a configure
# dialog would be better, but this common module file suffices for now.
###############################################################################

##to test with the book's email account
popservername  = 'pop.earthlink.net'
popusername    = 'pp3e'
smtpservername = 'smtp.comcast.net'


#------------------------------------------------------------------------------
# (required for load, delete) POP3 email server machine, user 
#------------------------------------------------------------------------------

#popservername = '?Please set your mailconfig.py attributes?'
#popusername   = 'yourid'

#popservername  = 'pop.rmi.net'            # or starship.python.net, 'localhost'
#popusername    = 'lutz'                   # password fetched or asked when run

#popservername  = 'pop.mindspring.com'     # yes, I have a few email accounts
#popusername    = 'lutz4'

#popservername  = 'pop.yahoo.com'
#popusername    = 'for_personal_mail'

#popservername  = 'pop.earthlink.net'   # pp3e@earthlink.net
#popusername    = 'pp3e'


#------------------------------------------------------------------------------
# (required for send) SMTP email server machine name
# see Python smtpd module for a smtp server class to run locally;
# note: your isp may require that you be directy connected to their system:
# I can email through earthlink on dialup, but cannot via comcast cable
#------------------------------------------------------------------------------

#smtpservername = 'your.server.com'         # smtp.comcast.net, smtp.mindspring.com 

#------------------------------------------------------------------------------
# (may be required for send) SMTP user/password if authenticated
# set user to None or '' if no login/authenticaion is required
# set pswd to name of a file holding your smtp password, or an
# empty string to force programs to ask (in a console, or gui)
#------------------------------------------------------------------------------

smtpuser  = None                           # per your isp
smtppasswdfile  = ''                       # set to '' to be asked

#------------------------------------------------------------------------------
# (optional) PyMailGUI: name of local one-line text file with your pop
# password; if empty or file cannot be read, pswd is requested when first
# connecting; pswd not encrypted: leave this empty on shared machines;
# PyMailCGI always asks for pswd (runs on a possibly remote server);
#------------------------------------------------------------------------------

poppasswdfile  = r'c:\temp\pymailgui.txt'      # set to '' to be asked

#------------------------------------------------------------------------------
# (optional) personal information used by PyMailGui to fill in edit forms;
# if not set, does not fill in initial form values;
# sig  -- can be a triple-quoted block, ignored if empty string;
# addr -- used for initial value of "From" field if not empty,
# no longer tries to guess From for replies--varying success;
#------------------------------------------------------------------------------

myaddress   = 'pp3e@earthlink.net'    # lutz@rmi.net
mysignature = '--your name'           # --Mark Lutz  (http://www.rmi.net/~lutz)

#------------------------------------------------------------------------------
# (optional) local file where sent messages are saved;
# PyMailGUI 'Open' button allows this file to be opened and viewed
# don't use '.' form if may be run from another dir: eg, pp3e demos
#------------------------------------------------------------------------------

#sentmailfile   = r'.\sentmail.txt'             # . means in current working dir

#sourcedir    = r'C:\Mark\PP3E-cd\Examples\PP3E\Internet\Email\PyMailGui\'
#sentmailfile = sourcedir + 'sentmail.txt'

# determine auto from one of my source files
import wraplines, os
mysourcedir   = os.path.dirname(os.path.abspath(wraplines.__file__))
sentmailfile  = os.path.join(mysourcedir, 'sentmail.txt')
                               
#------------------------------------------------------------------------------
# (optional) local file where pymail saves pop mail;
# PyMailGUI insead asks for a name with a popup dialog
#------------------------------------------------------------------------------

savemailfile   = r'c:\temp\savemail.txt'       # not used in PyMailGui: dialog

#------------------------------------------------------------------------------
# (optional) customize headers displayed in PyMailGUI list and view windows;
# listheaders replaces default, viewheaders extends it; both must be tuple of
# strings, or None to use default hdrs;
#------------------------------------------------------------------------------

listheaders = ('Subject', 'From', 'Date', 'To', 'X-Mailer')
viewheaders = None   # ('Bcc',)

#------------------------------------------------------------------------------
# (optional) PyMailGUI fonts and colors for text server/file message list
# windows, message content view windows, and view window attachment buttons;
# use ('family', size, 'style') for font; 'colorname' or hexstr '#RRGGBB' for
# color (background, foreground);  None means use defaults;  font/color of
# view windows can also be set interactively with texteditor's Tools menu;
#------------------------------------------------------------------------------

listbg   = 'indianred'         # None, 'white', '#RRGGBB' (see setcolor example)
listfg   = 'black'
listfont = ('courier', 9, 'bold')       # None, ('courier', 12, 'bold italic')
                                        # use fized-width font for list columns
viewbg     = '#dbbedc'
viewfg     = 'black'
viewfont   = ('courier', 10, 'bold')
viewheight = 24                         # max lines for height when opened 

partfg   = None
partbg   = None

# see Tk color names: aquamarine paleturqoise powderblue goldenrod burgundy ....

#listbg = listfg = listfont = None
#viewbg = viewfg = viewfont = viewheight = None      # to use defaults
#partbg = partfg = None

#------------------------------------------------------------------------------
# (optional) column at which mail's original text should be wrapped for view,
# reply, and forward;  wraps at first delimiter to left of this position;
# composed text is not auto-wrapped: user or recipient's mail tool must wrap
# new text if desired; to disable wrapping, set this to a high value (1024?);
#------------------------------------------------------------------------------

wrapsz = 100

#------------------------------------------------------------------------------
# (optional) control how PyMailGUI opens mail parts in the GUI;
# for view window Split actions and attachment quick-access buttons;
# if not okayToOpenParts, quick-access part buttons will not appear in
# the gui, and Split saves parts in a directory but does not open them;
# verifyPartOpens used by both Split action and quick-access buttons:
# all known-type parts open automatically on Split if this set to False;
# verifyHTMLTextOpen used by web browser open of HTML main text part:
#------------------------------------------------------------------------------

okayToOpenParts    = True      # open any parts/attachments at all?
verifyPartOpens    = False     # ask permission before opening each part?
verifyHTMLTextOpen = False     # if main text part is HTML, ask before open?

#------------------------------------------------------------------------------
# (optional) the maximum number of quick-access mail part butttons to show
# in the middle of view windows; after this many, a "..." button will be
# displayed, which runs the "Split" action to extract additional parts; 
#------------------------------------------------------------------------------

maxPartButtons = 8             # how many part buttons in view windows

#end
