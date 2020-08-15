#!/usr/local/bin/python
###############################################################
# A Python script to download and play a media file by FTP.
# Uses ftplib, the ftp protocol handler which uses sockets.
# Ftp runs on 2 sockets (one for data, one for control--on
# ports 20 and 21) and imposes message text formats, but the 
# Python ftplib module hides most of this protocol's details.
# Note: change to fetch file from a site you have access to.
###############################################################
     
import os, sys
from getpass import getpass

nonpassive  = False                           # force active mode ftp for server?
filename    = 'lawnlake2-jan-03.jpg'          # file to be downloaded
dirname     = '.'                             # remote directory to fetch from
sitename    = 'ftp.rmi.net'                   # ftp site to contact
userinfo    = ('lutz', getpass('Pswd?'))      # use () for anonymous
if len(sys.argv) > 1: filename = sys.argv[1]  # file name on command-line?
 
print 'Connecting...'
from ftplib import FTP                      # socket-based ftp tools
localfile  = open(filename, 'wb')           # local file to store download
connection = FTP(sitename)                  # connect to ftp site
connection.login(*userinfo)                 # default is anonymous login
connection.cwd(dirname)                     # xfer 1k at a time to localfile
if nonpassive:                              # force active ftp if servr requires
    connection.set_pasv(False)
    
print 'Downloading...'
connection.retrbinary('RETR ' + filename, localfile.write, 1024)
connection.quit()
localfile.close()

if raw_input('Open file?') in 'Yy':
    from PP3E.System.Media.playfile import playfile
    playfile(filename)
