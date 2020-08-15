from Tkinter import *
import random
autoGrow = False

class Gui3:
    colors = ['red', 'green', 'blue', 'orange', 'yellow']
    def __init__(self, parent):
        self.lblfont = 5
        self.makeWidgets(parent)
        if autoGrow: self.autoGrow()

    def reply(self):
        color = self.ent.get()
        self.lbl.config(font=('courier', self.lblfont), bg=color)
        self.lblfont += 5

    def dialog(self):
        popup = Toplevel()
        color = random.choice(self.colors)
        Label(popup, text='Popup', bg=color, font=('times', 25)).pack()

    def makeWidgets(self, win): 
        self.lbl = Label(win, text='Spam', fg='white', bg='blue')
        self.lbl.pack(side=TOP, expand=YES, fill=X)
        self.ent = Entry(win)
        self.ent.insert(0, 'Cyan')
        self.ent.pack()
        btn = Button(win, text='Press', command=self.reply)
        btn.pack(side=BOTTOM, expand=YES, fill=BOTH)
        btn.config(font=('courier', 25, 'italic bold'))
        Button(win, text='Popup',
               command=self.dialog).pack(side=BOTTOM, fill=X)
        self.ent.bind('<Return>', (lambda event: self.reply()))

    def autoGrow(self):
        try:
            self.reply()
        except: pass
        self.lbl.after(2000, self.autoGrow)

main = Tk()
main.title('GUI3')
Gui3(main)
other = Toplevel()
other.title('Other')
Gui3(other)
mainloop()

