import shelve
from Tkinter import *
from tkMessageBox import showerror
dbname = raw_input('Shelve db file?') or 'peopletext.db'
dbase = shelve.open(dbname)

def onFetch():
    key = ent.get()
    try:
        rec = dbase[key]
        popup = Toplevel()
        popup.title('Key=' + key)
        left  = Frame(popup)
        right = Frame(popup)
        left.pack(side=LEFT)
        right.pack(side=RIGHT, expand=YES, fill=X)
        for field in rec.__dict__:
            value = getattr(rec, field)
            Label(left, text=field).pack()
            valent = Entry(right, relief=RIDGE)
            valent.pack(fill=X)
            valent.insert(0, value)
    except:
        import sys
        print sys.exc_info()[0], sys.exc_info()[1]
        showerror('peoplegui', 'Bad Key!')

mainwin = Tk()
mainwin.title('DB GUI')
ent = Entry(mainwin)
ent.pack(fill=X)
Button(mainwin, text='Fetch', command=onFetch).pack()
mainloop()
