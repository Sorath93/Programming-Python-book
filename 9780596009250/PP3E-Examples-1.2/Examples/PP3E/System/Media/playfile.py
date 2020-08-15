#!/usr/local/bin/python
################################################################################ 
# Try to play an arbitrary media file.  This may not work on your system as is;
# audio files use filters and command-lines on Unix, and filename associations
# on Windows via the start command (i.e., whatever you have on your machine to
# run .au files--an audio player, or perhaps a web browser).  Configure and
# extend as needed.  As a last resort, always tries to launch a web browser with
# Python webbrowser module (like LaunchBrowser.py).  See also: Lib/audiodev.py.
# playknownfile assumes you know what sort of media you wish to open; playfile
# tries to determine media type automatically using Python mimetypes module.
################################################################################

import os, sys

helpmsg = """
Sorry: can't find a media player for '%s' on your system!
Add an entry for your system to the media player dictionary
for this type of file in playfile.py, or play the file manually.
"""

def trace(*args):
    print ' '.join(args)   # with spaces between

################################################################################
# player techniques: generic and otherwise: extend me
################################################################################

class MediaTool: 
    def __init__(self, runtext=''):
        self.runtext = runtext

class Filter(MediaTool):
    def run(self, mediafile, **options):
        media  = open(mediafile, 'rb')             
        player = os.popen(self.runtext, 'w')        # spawn shell tool
        player.write(media.read())                  # send to its stdin

class Cmdline(MediaTool):
    def run(self, mediafile, **options):
        cmdline = self.runtext % mediafile          # run any cmd line
        os.system(cmdline)                          # use %s for filename

class Winstart(MediaTool):                          # use windows registry
    def run(self, mediafile, wait=False):           # or os.system('start file')
        if not wait:                                # allow wait for curr media
            os.startfile(mediafile)
        else:
            os.system('start /WAIT ' + mediafile)

class Webbrowser(MediaTool):
    def run(self, mediafile, **options):                 # open in web browser
        import webbrowser                                # find browser, no wait
        fullpath = os.path.abspath(mediafile)            # file:// needs abs dir
        webbrowser.open_new('file://%s' % fullpath)      # open media file

################################################################################
# media- and platform-specific policies: change me, or pass one in 
##############################################################################

# map platform to player: change me!

audiotools = {
    'sunos5':  Filter('/usr/bin/audioplay'),             # os.popen().write()
    'linux2':  Cmdline('cat %s > /dev/audio'),           # on zaurus, at least
    'sunos4':  Filter('/usr/demo/SOUND/play'),
    'win32':   Winstart()                                # startfile or system 
   #'win32':   Cmdline('start %s')
    }

videotools = {
    'linux2':  Cmdline('tkcVideo_c700 %s'),              # zaurus pda
    'win32':   Winstart(),                               # avoid dos popup
    }

imagetools = {
    'linux2':  Cmdline('zimager %s/%%s' % os.getcwd()),  # zaurus pda
    'win32':   Winstart(),
    }

# map mimetype of filenames to player tables

mimetable = {'audio': audiotools,                        # add text: PyEdit?
             'video': videotools,                      
             'image': imagetools}

################################################################################
# top-level interfaces
################################################################################

def trywebbrowser(mediafile, helpmsg=helpmsg):
    """
    try to open a file in a web browser
    """
    trace('trying browser', mediafile)                         # last resort
    try:
        player = Webbrowser()
        player.run(mediafile)
    except:
        print helpmsg % mediafile                              # nothing worked

def playknownfile(mediafile, playertable={}, **options):
    """
    play media file of known type: uses platform-specific
    player objects, or spawns a web browser if nothing for
    this platform; pass in a media-specific player table
    """
    if sys.platform in playertable:
        playertable[sys.platform].run(mediafile, **options)    # specific tool
    else:
        trywebbrowser(mediafile)                               # general scheme

def playfile(mediafile, mimetable=mimetable, **options):
    """
    play media file of any type: uses mimetypes to guess
    media type and map to platform-specific player tables;
    spawn web browser if media type unknown, or has no table
    """
    import mimetypes
    (contenttype, encoding) = mimetypes.guess_type(mediafile)     # check name
    if contenttype == None or encoding is not None:               # can't guess
        contenttype = '?/?'                                       # poss .txt.gz
    maintype, subtype = contenttype.split('/', 1)                 # 'image/jpeg'
    if maintype in mimetable:
        playknownfile(mediafile, mimetable[maintype], **options)  # try table
    else:
        trywebbrowser(mediafile)                                  # other types

###############################################################################
# self-test code
###############################################################################

if __name__ == '__main__':
    # media type known
    playknownfile('sousa.au', audiotools, wait=True)
    playknownfile('ora-pp2e.jpg', imagetools, wait=True)
    playknownfile('mov10428.mpg', videotools, wait=True)
    playknownfile('img_0276.jpg', imagetools)
    playknownfile('mov10510.mpg', mimetable['video'])

    # media type guessed
    raw_input('Stop players and press Enter')
    playfile('sousa.au', wait=True)                       # default mimetable
    playfile('img_0268.jpg')
    playfile('mov10428.mpg' , mimetable)                  # no extra options
    playfile('calendar.html')                             # default web browser
    playfile('wordfile.doc')
    raw_input('Done')                                     # stay open if clicked
