from Tkinter import *
from tkMessageBox import showerror
import shelve
fieldnames = ('name', 'age', 'job', 'pay')

class PeopleGui(Tk):
    def __init__(self):
        Tk.__init__(self)
        form   = Frame(self)
        labels = Frame(form)
        values = Frame(form)
        labels.pack(side=LEFT)
        values.pack(side=RIGHT)
        form.pack()

        self.entries = {}
        for label in ('key',) + fieldnames:
            Label(labels, text=label).pack()
            ent = Entry(values)
            ent.pack()
            self.entries[label] = ent

        Button(self, text="Fetch",  command=self.fetchRecord).pack(side=LEFT)
        Button(self, text="Update", command=self.updateRecord).pack(side=LEFT)
        Button(self, text="Quit",   command=self.quit).pack(side=LEFT)

    def fetchRecord(self):
        entries = self.entries
        key = entries['key'].get()
        db = shelve.open('class-shelve')
        try:
            record = db[key]
        except:
            showerror(title='Error', message='No such key!')
        else:
            for field in fieldnames:
                entries[field].delete(0, END)
                entries[field].insert(0, repr(getattr(record, field)))
        db.close()

    def updateRecord(self):
        entries = self.entries
        key = entries['key'].get()
        db = shelve.open('class-shelve')
        if key in db.keys():
            record = db[key]                      # update existing record
        else:
            from person import Person             # make/store new one for key
            record = Person(name='?', age='?')
        for field in fieldnames:
            setattr(record, field, eval(entries[field].get()))
        db[key] = record
        db.close()

window = PeopleGui()
window.mainloop()
