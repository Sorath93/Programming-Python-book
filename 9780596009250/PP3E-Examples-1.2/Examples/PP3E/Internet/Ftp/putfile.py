#!/usr/local/bin/python
########################################################## 
# Store an arbitrary file by ftp.  Uses anonymous 
# ftp unless you pass in a user=(name, pswd) tuple.
##########################################################
 
import ftplib                    # socket-based ftp tools
   
def putfile(file, site, dir, user=(), verbose=True):
    """
    store a file by ftp to a site/directory
    anonymous or real login, binary transfer
    """
    if verbose: print 'Uploading', file
    local  = open(file, 'rb')               # local file of same name
    remote = ftplib.FTP(site)               # connect to ftp site
    remote.login(*user)                     # anonymous or real login
    remote.cwd(dir)
    remote.storbinary('STOR ' + file, local, 1024)
    remote.quit()
    local.close()
    if verbose: print 'Upload done.'
     
if __name__ == '__main__':
    site = 'ftp.rmi.net'
    dir  = '.'
    import sys, getpass
    pswd = getpass.getpass(site + ' pswd?')                # filename on cmdline
    putfile(sys.argv[1], site, dir, user=('lutz', pswd))   # non-anonymous login
