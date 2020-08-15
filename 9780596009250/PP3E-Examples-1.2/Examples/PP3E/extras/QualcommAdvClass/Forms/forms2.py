from Tkinter import *

class FormGui:
    def __init__(self, win, fields):
        form = Frame(win)
        left = Frame(form)
        rite = Frame(form)
        form.pack(side=TOP)
        left.pack(side=LEFT)
        rite.pack(side=RIGHT)
        self.ents = []
        for field in fields:
            Label(left, text=field).pack(side=TOP)
            ent = Entry(rite)
            ent.pack(side=TOP)
            ent.insert(0, '?')
            self.ents.append(ent)
        self.fields = fields
        Button(win, text='Ok', command=self.onOK).pack(side=LEFT, fill=X)

    def onOK(self):
        print 'OK...'
        for (name, ent) in zip(self.fields, self.ents):
            print name, '=>', ent.get()

if __name__ == '__main__':
    fields = ['name', 'age', 'job', 'pay']
    win = Tk()
    win.title('Form GUI')
    FormGui(win, fields)
    class SubForm(FormGui):
        def onOK(self):
            print 'Spam'
    SubForm(Toplevel(), ['spam', 'Spam', 'SPAM'])
    mainloop()
    print 'Bye'
