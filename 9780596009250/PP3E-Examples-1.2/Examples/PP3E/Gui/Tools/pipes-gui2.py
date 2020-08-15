from Tkinter import *
from PP3E.Gui.Tools.guiStreams import redirectedGuiShellCmd

def launch():
    redirectedGuiShellCmd('python -u pipes-nongui.py')

window = Tk()
Button(window, text='GO!', command=launch).pack()
window.mainloop()
