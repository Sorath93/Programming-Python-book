#!/bin/env python 
##############################################################################
# use ftp to upload all files from a local dir to a remote site/directory;
# this version reuses downloader's functions, to avoid code redundandcy;
##############################################################################

import os
from downloadflat_modular import configTransfer, connectFtp, isTextKind

def cleanRemotes(cf, connection):
    """
    try to delete all remote files first to remove garbage
    """
    if cf.cleanall:
        for remotename in connection.nlst():          # remote dir listing
            try:                                      # remote file delete
                print 'deleting remote', remotename
                connection.delete(remotename)           
            except:                                     
                print 'cannot delete remote', remotename

def uploadAll(cf, connection):
    """
    upload all files to remote site/dir per cf config
    listdir() strips dir path, any failure ends script
    """
    localfiles = os.listdir(cf.localdir)            # listdir is local listing
    for localname in localfiles:
        localpath = os.path.join(cf.localdir, localname) 
        print 'uploading', localpath, 'to', localname, 'as',
        if isTextKind(localname):
            # use text mode xfer
            localfile = open(localpath, 'r')
            connection.storlines('STOR ' + localname, localfile)
        else:
            # use binary mode xfer
            localfile = open(localpath, 'rb')
            connection.storbinary('STOR ' + localname, localfile)
        localfile.close()
    connection.quit()
    print 'Done:', len(localfiles), 'files uploaded.'

if __name__ == '__main__':
    cf = configTransfer()
    conn = connectFtp(cf)
    cleanRemotes(cf, conn)
    uploadAll(cf, conn)
