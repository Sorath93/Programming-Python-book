"""
fetch a web page or ftp file, escape for it embedding in HTML;
functions here become Zope external methods and may be invoked
by URLs or other Zope objects, but can be used outside Zope too
"""

import urllib, ftplib, StringIO, cgi

def fetchWebPage(self, url, sizelimit=None):
    """
    fetch reply from a web page url
    will also work for ftp:// urls, script parameters
    """
    site = urllib.urlopen(url)
    text = site.read()
    if not sizelimit: sizelimit = len(text)
    return cgi.escape(text[:sizelimit])

def fetchFtpFile(self, host, directory, file, userinfo=(), sizelimit=None):
    """
    fetch a file from an ftp site
    assume binary mode, anonymous"
    """
    buff = StringIO.StringIO()
    site = ftplib.FTP(host)
    site.login(*userinfo)
    site.cwd(directory)
    site.retrbinary('RETR ' + file, buff.write)
    site.quit()
    text = buff.getvalue()
    if not sizelimit: sizelimit = len(text)
    return cgi.escape(text[:sizelimit])

def selftest():
    X = '-'*40
    import getpass
    login = raw_input('user?'), getpass.getpass('pswd?')
    print fetchWebPage(None, 'http://www.python.org', 193), X
    print fetchFtpFile(None, 'home.rmi.net', '.', 'mytrain.html', login, 72), X
    print fetchWebPage(None, 'http://www.rmi.net/~lutz/mytrain.html', 72), X

if __name__ == '__main__': selftest()
