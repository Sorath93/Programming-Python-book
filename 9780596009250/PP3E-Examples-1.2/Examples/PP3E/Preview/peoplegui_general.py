from Tkinter import *
from tkMessageBox import showerror
import shelve

def makeWidgets(fieldnames, newrecord):
    global entries
    window = Tk()
    window.title('People Shelve')
    form   = Frame(window)
    labels = Frame(form)
    values = Frame(form)
    labels.pack(side=LEFT)
    values.pack(side=RIGHT)
    form.pack()
    entries = {}
    for label in ('key',) + fieldnames:
        Label(labels, text=label).pack()
        ent = Entry(values)
        ent.pack()
        entries[label] = ent
    Button(window, text="Fetch",
           command=lambda: fetchRecord(fieldnames)).pack(side=LEFT)
    Button(window, text="Update",
           command=lambda: updateRecord(fieldnames, newrecord)).pack(side=LEFT)
    Button(window, text="Quit",
           command=window.quit).pack(side=RIGHT)
    return window

def fetchRecord(fieldnames):
    key = entries['key'].get()
    try:
        record = db[key]                      # fetch by key, show in gui
    except:
        showerror(title='Error', message='No such key!')
    else:
        for field in fieldnames:
            entries[field].delete(0, END)
            entries[field].insert(0, repr(getattr(record, field)))

def updateRecord(fieldnames, newrecord):
    key = entries['key'].get()
    if key in db.keys():
        record = db[key]                      # update existing record
    else:                                     # make/store new one for key
        record = newrecord()                  # eval: strings must be quoted
    for field in fieldnames:
        setattr(record, field, eval(entries[field].get()))
    db[key] = record

def main(file, fieldnames, newrecord):
    global db
    db = shelve.open('class-shelve')
    window = makeWidgets(fieldnames, newrecord)
    window.mainloop()
    db.close()

if __name__ == '__main__':
    from person import Person
    fieldnames = ('name', 'age', 'job', 'pay')
    main('class-shelve', fieldnames, (lambda: Person(name='?', age='?')))
    
