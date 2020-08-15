#!/usr/local/bin/python
####################################################################### 
# Usage: sousa.py.  Fetch and play the Monty Python theme song.
# This may not work on your system as is: it requires a machine with
# Internet access, and uses audio filters on Unix and your .au player
# on Windows.  Configure playfile.py as needed for your platform.
#######################################################################
 
from PP3E.Internet.Ftp.getfile  import getfile
from PP3E.System.Media.playfile import playfile
from getpass import getpass

file = 'sousa.au'                      # default file coordinates
site = 'ftp.rmi.net'                   # monty python theme song
dir  = '.'
user = ('lutz', getpass('Pswd?'))
 
getfile(file, site, dir, user)         # fetch audio file by ftp
playfile(file)                         # send it to audio player

# import os
# os.system('getone.py sousa.au')      # equivalent command-line
