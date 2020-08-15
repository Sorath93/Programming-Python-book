#!/usr/local/bin/python
###################################################################
# A Python script to download a file by FTP by its URL string.
# use higher-level urllib instead of ftplib to fetch file;
# urllib supports ftp, http, and gopher protocols, and local files;
# urllib also allows downloads of html pages, images, text, etc.;
# see also Python html/xml parsers for web pages fetched by urllib;
###################################################################
     
import os, getpass
import urllib                            # socket-based web tools
filename = 'lawnlake2-jan-03.jpg'        # remote/local file name
password = getpass.getpass('Pswd?')
 
remoteaddr = 'ftp://lutz:%s@ftp.rmi.net/%s;type=i' % (password, filename)
print 'Downloading', remoteaddr
     
# this works too:
# urllib.urlretrieve(remoteaddr, filename)
    
remotefile = urllib.urlopen(remoteaddr)     # returns input file-like object
localfile  = open(filename, 'wb')           # where to store data locally
localfile.write(remotefile.read())
localfile.close()
remotefile.close()
