#!/bin/env python 
###############################################################################
# use ftp to copy (download) all files from a single directory at a remote
# site to a directory on the local machine; run me periodically to mirror
# a flat ftp site directory to a your ISP account;  set user to 'anonymous'
# to do anonymous ftp;  we could use try to skip file failures, but the ftp
# connection is likely closed if any files fail;  we could also try to
# reconnect with a new FTP instance before each transfer: connects once now;
# if failures, try setting nonpassive for active ftp, or disable firewalls;
# this also depends on a working FTP server, and possibly its load policies.
###############################################################################

import os, sys, ftplib
from getpass   import getpass
from mimetypes import guess_type

nonpassive = False                        # passive ftp on by default in 2.1+
remotesite = 'home.rmi.net'               # download from this site
remotedir  = '.'                          # and this dir (e.g., public_html)
remoteuser = 'lutz'
remotepass = getpass('Password for %s on %s: ' % (remoteuser, remotesite))
localdir   = (len(sys.argv) > 1 and sys.argv[1]) or '.'
cleanall   = raw_input('Clean local directory first? ')[:1] in ['y', 'Y']

print 'connecting...'
connection = ftplib.FTP(remotesite)                 # connect to ftp site
connection.login(remoteuser, remotepass)            # login as user/password
connection.cwd(remotedir)                           # cd to directory to copy
if nonpassive:                                      # force active mode ftp
    connection.set_pasv(False)                      # most servers do passive

if cleanall:
    for localname in os.listdir(localdir):          # try to delete all locals
        try:                                        # first to remove old files
            print 'deleting local', localname
            os.remove(os.path.join(localdir, localname))
        except:
            print 'cannot delete local', localname

count = 0                                           # download all remote files
remotefiles = connection.nlst()                     # nlst() gives files list
                                                    # dir()  gives full details
for remotename in remotefiles:
    mimetype, encoding = guess_type(remotename)     # eg ('text/plain', 'gzip')
    mimetype  = mimetype or '?/?'                   # may be (None, None)
    maintype  = mimetype.split('/')[0]              # .jpg ('image/jpeg', None')

    localpath = os.path.join(localdir, remotename) 
    print 'downloading', remotename, 'to', localpath,
    print 'as', maintype, encoding or ''
    if maintype == 'text' and encoding == None:
        # use ascii mode xfer
        localfile = open(localpath, 'w')
        callback  = lambda line: localfile.write(line + '\n')
        connection.retrlines('RETR ' + remotename, callback)
    else:
        # use binary mode xfer
        localfile = open(localpath, 'wb')
        connection.retrbinary('RETR ' + remotename, localfile.write)
    localfile.close()
    count += 1

connection.quit()
print 'Done:', count, 'files downloaded.' 
