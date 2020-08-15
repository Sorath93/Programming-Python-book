#!/usr/local/bin/python
################################################################
# A Python script to download and play a media file by ftp.
# Uses getfile.py, a utility module which encapsulates ftp step.
################################################################
     
import getfile
from getpass import getpass
filename = 'lawnlake2-jan-03.jpg'
     
# fetch with utility 
getfile.getfile(file=filename,
                site='ftp.rmi.net',
                dir ='.',
                user=('lutz', getpass('Pswd?')),
                refetch=True)
     
# rest is the same
if raw_input('Open file?') in 'Yy':
    from PP3E.System.Media.playfile import playfile
    playfile(filename)
