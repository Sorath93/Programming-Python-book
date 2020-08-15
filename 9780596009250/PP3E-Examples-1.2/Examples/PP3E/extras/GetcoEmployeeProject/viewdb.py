from Tkinter import *

def viewer(win, object, title='Viewer'):
    left  = Frame(win)
    right = Frame(win)
    left.pack(side=LEFT)
    right.pack(side=RIGHT)
    fields = object.__dict__.keys()
    for field in fields:
        Label(left, text=field).pack()
        Label(right, text=getattr(object, field)).pack()
    win.title(title)

def viewdb(dbfilename):
    from ZODB import FileStorage, DB
    storage = FileStorage.FileStorage(dbfilename)
    db = DB(storage)
    connection = db.open()
    root = connection.root()
    for key in root.keys():
        popup = Toplevel()
        viewer(popup, root[key], key)
    
if __name__ == '__main__':
    win = Tk()
    Label(win, text='Database viewer 0.1').pack()
    viewdb('zodb1.fs')
    win.mainloop()

