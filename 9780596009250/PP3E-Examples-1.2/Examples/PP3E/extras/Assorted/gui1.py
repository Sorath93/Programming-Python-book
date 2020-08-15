from Tkinter import *
import random
from tkMessageBox import showerror
colors = ['red', 'navy', 'green', 'orange', 'brown']

def handler():
    lab.config(text='goodbye')

def popup():
    win = Toplevel()
    lab = Label(win, text='Popup', font=('courier bold', 30))
    lab.pack(expand=YES, fill=BOTH)
    color = random.choice(colors)
    lab.config(bg=color)
    win.title('SPAM')

def dialogs():
    showerror(title='Bad!', message='Ouch...')

main = Tk()
lab = Label(main, text='Hello')
btn = Button(main, text='Press', command=handler)
bt2 = Button(main, text='Spam', command=popup)
bt3 = Button(main, text='Quit', command=dialogs)
lab.pack(side=TOP, expand=YES, fill=BOTH)
btn.pack(side=LEFT, expand=YES, fill=X)
bt2.pack(side=LEFT, expand=YES, fill=X)
bt3.pack(side=LEFT, expand=YES, fill=X)
lab.config(fg='white', bg='black')
main.title('Gui1')
mainloop()
