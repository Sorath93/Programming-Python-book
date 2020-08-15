from Tkinter import *
fields = ['name', 'age', 'job', 'pay']

win = Tk()
form = Frame(win)
left = Frame(form)
rite = Frame(form)
form.pack(side=TOP)
left.pack(side=LEFT)
rite.pack(side=RIGHT)
win.title('Form GUI')

ents = []
for field in fields:
    Label(left, text=field).pack(side=TOP)
    ent = Entry(rite)
    ent.pack(side=TOP)
    ent.insert(0, '?')
    ents.append(ent)

def onOK():
    print 'OK...'
    for (name, ent) in zip(fields, ents):
        print name, '=>', ent.get()
        
def onCancel():
    print 'Cancel...'
    win.quit()

Button(win, text='Ok', command=onOK).pack(side=LEFT, fill=X)
Button(win, text='Cancel', command=onCancel).pack(side=LEFT, fill=X)
win.mainloop()
    
