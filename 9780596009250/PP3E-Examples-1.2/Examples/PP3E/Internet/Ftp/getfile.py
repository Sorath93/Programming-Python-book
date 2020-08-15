#!/usr/local/bin/python
#########################################################################
# Fetch an arbitrary file by ftp.  Anonymous ftp unless you pass a
# user=(name, pswd) tuple. Self-test ftps a test file and site.
#########################################################################
 
from ftplib  import FTP          # socket-based ftp tools
from os.path import exists       # file existence test

def getfile(file, site, dir, user=(), verbose=True, refetch=False):
    """
    fetch a file by ftp from a site/directory
    anonymous or real login, binary transfer
    """
    if exists(file) and not refetch:
        if verbose: print file, 'already fetched'
    else:
        if verbose: print 'Downloading', file
        local = open(file, 'wb')                # local file of same name
        try:
            remote = FTP(site)                  # connect to ftp site
            remote.login(*user)                 # anonymous=() or (name, pswd)
            remote.cwd(dir)
            remote.retrbinary('RETR ' + file, local.write, 1024)
            remote.quit()
        finally:
            local.close()                       # close file no matter what
        if verbose: print 'Download done.'      # caller handles exceptions
     
if __name__ == '__main__':
    from getpass import getpass
    file = 'lawnlake2-jan-03.jpg'
    dir  = '.'                 
    site = 'ftp.rmi.net'       
    user = ('lutz', getpass('Pswd?'))
    getfile(file, site, dir, user)  
