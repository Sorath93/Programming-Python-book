from Tkinter import *
import random

class Gui1:
    colors = ['blue', 'red', 'green', 'yellow', 'orange']
    
    def __init__(self, parent, fontsize=25):
        self.fontsize = fontsize
        self.makeWidgets(parent)
        self.parent = parent
        # self.timer()
    
    def reply(self):
        popup = Toplevel()
        popup.title('Popup Window')
        color = random.choice(self.colors)
        Label(popup, text='Popup!', bg=color).pack()
        self.lab.config(fg=color)

    def timer(self):
        self.lab.config(bg=random.choice(self.colors))
        self.fontsize += 2
        self.lab.config(font=('Courier', self.fontsize, 'italic'))
        self.parent.after(250, self.timer)
                   
    def makeWidgets(self, parent):
        self.lab = Label(parent, text='Spam', font=('Courier', self.fontsize, 'italic'))
        self.lab.pack(side=TOP, expand=YES, fill=BOTH)
        Button(parent, text='press', command=self.reply).pack(side=TOP, fill=X)
        Button(parent, text='grow', command=self.timer).pack(side=LEFT)
        Button(parent, text='stop', command=self.timer).pack(side=RIGHT)

main = Tk()
main.title('GUI1')
Gui1(main)

popup = Toplevel()
popup.title('More')
Gui1(popup, 1)
main.mainloop()
