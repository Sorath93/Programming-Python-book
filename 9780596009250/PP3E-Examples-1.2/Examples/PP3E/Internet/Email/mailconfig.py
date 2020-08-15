###############################################################################
# user configuration settings for various email programs (pymail version);
# email scripts get their server names and other email config options from
# this module: change me to reflect your machine names, sig, and preferences;
###############################################################################

#------------------------------------------------------------------------------
# (required for load, delete) POP3 email server machine, user 
#------------------------------------------------------------------------------

popservername  = 'pop.earthlink.net'    # or pop.rmi.net
popusername    = 'pp3e'                 # pp3e@earthlink.net

#------------------------------------------------------------------------------
# (required for send) SMTP email server machine name
# see Python smtpd module for a smtp server class to run locally;
# note: your isp may require that you be directy connected to their system:
# I can email through earthlink on dialup, but cannot via comcast cable
#------------------------------------------------------------------------------

smtpservername = 'smtp.comcast.net'     # or 'smtp.mindspring.com', 'localhost' 

#------------------------------------------------------------------------------
# (optional) personal information used by PyMailGUI to fill in edit forms;
# if not set, does not fill in initial form values;
# sig  -- can be a triple-quoted block, ignored if empty string;
# addr -- used for initial value of "From" field if not empty,
# no longer tries to guess From for replies--varying success;
#------------------------------------------------------------------------------

myaddress   = 'pp3e@earthlink.net'
mysignature = '--your signature'     # '--Mark Lutz  (http://www.rmi.net/~lutz)'

#------------------------------------------------------------------------------
# (may be required for send) SMTP user/password if authenticated
# set user to None or '' if no login/authenticaion is required
# set pswd to name of a file holding your smtp password, or an
# empty string to force programs to ask (in a console, or gui)
#------------------------------------------------------------------------------

smtpuser  = None                           # per your isp
smtppasswdfile  = ''                       # set to '' to be asked

#------------------------------------------------------------------------------
# (optional) name of local one-line text file with your pop
# password; if empty or file cannot be read, pswd is requested when first
# connecting; pswd not encrypted: leave this empty on shared machines;
#------------------------------------------------------------------------------

poppasswdfile  = r'c:\temp\pymailgui.txt'      # set to '' to be asked

#------------------------------------------------------------------------------
# (optional) local file where sent messages are saved;
#------------------------------------------------------------------------------

sentmailfile   = r'.\sentmail.txt'             # . means in current working dir

#------------------------------------------------------------------------------
# (optional) local file where pymail saves pop mail;
#------------------------------------------------------------------------------

savemailfile   = r'c:\temp\savemail.txt'       # not used in PyMailGUI: dialog

#end
