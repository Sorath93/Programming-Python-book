#!/usr/local/bin/python
################################################################
# A Python script to download and build Python's source code.
# Uses getfile.py, a utility module which encapsulates ftp step.
################################################################
     
import getfile
version = '2.4'                         # version to download
tarname = 'Python-%s.tgz' % version     # remote/local file name
     
# fetch with utility 
getfile.getfile(tarname, 'ftp.python.org', 'pub/python/' + version)
     
# rest is the same
execfile('buildPython.py')
