from Tkinter import *
root = Tk()
root.title('Ni')

import random
colors = ['navy', 'red', 'black', 'green']

def printit():
    color = random.choice(colors)
    a.config(bg=color)
    print 'spam'
    popup = Toplevel()
    Button(popup, text='Shrubbery', font=('times', 50),
           command=popup.destroy).pack()

a = Button(root, text='Spam', command=printit)
a.config(fg='white', bg='navy', font=('courier', 30))
b = Button(root, text='Close', command=root.quit)
a.pack(expand=YES, fill=BOTH)
b.pack()
root.mainloop()
