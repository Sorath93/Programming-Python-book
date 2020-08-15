from Tkinter import *
import random

colors = ['red', 'green', 'blue', 'yellow', 'white']
numpress = 0

def onPress(numpress):
   popup = Toplevel()
   color = random.choice(colors)
   text  = 'Popup %s!' % numpress 
   Label(popup, text=text, bg=color, font=('times', 25)).pack()

mainwin = Tk()
lab = Label(mainwin, text='Spam!')
lab.pack(side=TOP, expand=YES, fill=X)
lab.config(font=('courier', 20, 'italic'))

btn = Button(text='Press', command=lambda: onPress(numpress))
btn.config(bg='navy', fg='white')
btn.pack(side=BOTTOM, fill=X)
mainloop()
