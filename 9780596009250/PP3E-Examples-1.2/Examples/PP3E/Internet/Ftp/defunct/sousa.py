#!/usr/local/bin/python
####################################################################### 
# Usage: sousa.py.  Fetch and play the Monty Python theme song.
# This may not work on your system as is: it requires a machine with
# Internet access, and uses audio filters on Unix and your .au player
# on Windows.  Configure playfile.py as needed for your platform.
#######################################################################
 
import os, sys
from PP3E.Internet.Ftp.getfile  import getfile
from PP3E.System.Media.playfile import playfile

file = 'sousa.au'                # default file coordinates
site = 'ftp.python.org'          # monty python theme song
dir  = 'pub/python/misc'
 
getfile(file, site, dir)         # fetch audio file by ftp
playfile(file)                   # send it to audio player
