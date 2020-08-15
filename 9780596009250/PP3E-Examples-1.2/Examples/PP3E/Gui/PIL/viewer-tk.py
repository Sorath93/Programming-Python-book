#######################################################
# show one image with standard Tkinter photo object
# as is this handles gif files, but not jpeg images
# image file name listed in command line, or default
# use a Canvas instead of Label for scrolling, etc.
#######################################################

import os, sys
from Tkinter import *                    # use standard Tkinter photo object
                                         # gif works, but jpg requires pil
imgdir  = 'images'
imgfile = 'newmarket-uk-2.gif'
if len(sys.argv) > 1:                    # cmdline argument given?
    imgfile = sys.argv[1]
imgpath = os.path.join(imgdir, imgfile)

win = Tk()
win.title(imgfile)
imgobj = PhotoImage(file=imgpath)        # display photo on a Label
Label(win, image=imgobj).pack()
print imgobj.width(), imgobj.height()    # show size in pixels before destroyed
win.mainloop()
