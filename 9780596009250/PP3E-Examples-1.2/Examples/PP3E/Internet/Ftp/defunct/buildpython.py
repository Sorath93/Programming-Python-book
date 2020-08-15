#!/usr/local/bin/python
###############################################################
# A Python script to build Python from its source code.
# Run me in directory where Python source distribution lives.
###############################################################
     
import os
version = '2.4'                                  # version to build
tarname = 'Python-%s.tgz' % version              # remote/local file name
 
print 'Unpacking...'
os.system('gzip -d '  + tarname)                 # decompress '.tgz' file
os.system('tar -xvf ' + tarname[:-4] + '.tar')   # untar '.tar' file
     
print 'Building...'
os.chdir('Python-' + version)                    # build Python itself
os.system('./configure')                         # assumes unix-style make
os.system('make')
os.system('make test')
print 'Done: see Python-%s/python.' % version
