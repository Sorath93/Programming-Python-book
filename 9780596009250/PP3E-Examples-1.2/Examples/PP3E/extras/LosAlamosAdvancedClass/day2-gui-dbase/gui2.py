from Tkinter import *
import random

class MyGui:
    colors = ['red', 'green', 'blue', 'yellow', 'white']

    def __init__(self, parent, label):
        self.numpress = 0
        self.makeWidgets(parent)
        parent.title(label)

    def onPress(self):
        popup = Toplevel()
        color = random.choice(MyGui.colors)
        text  = 'Popup %s!' % self.numpress 
        Label(popup, text=text, bg=color, font=('times', 25)).pack()
        self.numpress += 1

    def makeWidgets(self, parent):
        lab = Label(parent, text='Spam!')
        lab.pack(side=TOP, expand=YES, fill=X)
        lab.config(font=('courier', 20, 'italic'))

        btn = Button(parent, text='Press', command=self.onPress)
        btn.config(bg='navy', fg='white')
        btn.pack(side=BOTTOM, fill=X)
        self.btn = btn

    def changeColor(self):
        self.btn.config(bg=random.choice(MyGui.colors))

if __name__ == '__main__':
    win1 = MyGui(Toplevel(), 'Main')
    win2 = MyGui(Toplevel(), 'Popup1')
    win3 = MyGui(Toplevel(), 'Popup2')
    Button(text='change1', command=win1.changeColor).pack()
    Button(text='change2', command=win2.changeColor).pack()
    Button(text='change3', command=win3.changeColor).pack()
    mainloop()
