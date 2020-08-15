#!/usr/local/bin/python
###############################################################
# A Python script to download and build Python's source code.
# Uses ftplib, the ftp protocol handler which uses sockets.
# Ftp runs on 2 sockets (one for data, one for control--on
# ports 20 and 21) and imposes message text formats, but the 
# Python ftplib module hides most of this protocol's details.
# Note: Python's filename and directory are prone to change.
###############################################################
     
import os
nonpassive    = False                       # force active mode ftp for server?
unpack_source = True                        # run gzip, tar commands to unpack?
build_source  = False                       # run unix-like build commands too?
version       = '2.4'                       # version to download
tarname       = 'Python-%s.tgz' % version   # remote/local file name
 
print 'Connecting...'
from ftplib import FTP                      # socket-based ftp tools
localfile  = open(tarname, 'wb')            # where to store download
connection = FTP('ftp.python.org')          # connect to ftp site
connection.login()                          # default is anonymous login
connection.cwd('pub/python/' + version)     # xfer 1k at a time to localfile
if nonpassive:                              # force active ftp if servr requires
    connection.set_pasv(False)
     
print 'Downloading...'
connection.retrbinary('RETR ' + tarname, localfile.write, 1024)
connection.quit()
localfile.close()

if unpack_source:
    print 'Unpacking...'                            # requires gzip,tar progs
    os.system('gzip -d '  + tarname)                # decompress .tgz to .tar
    os.system('tar -xvf ' + tarname[:-4]+'.tar')    # extract tar arcive

if build_source:
    print 'Building...'                             # requires unix-like tools
    os.chdir('Python-' + version)                   # build Python itself
    os.system('./configure')                        # assumes unix-style make
    os.system('make')
    os.system('make test')
    print 'Done: see Python-%s/python.' % version
