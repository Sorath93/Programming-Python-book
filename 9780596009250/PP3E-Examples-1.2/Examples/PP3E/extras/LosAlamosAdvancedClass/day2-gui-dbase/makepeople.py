db = [
     {'name': 'Bob Smith', 'age': 40, 'job': ['dev', 'mgr']},
     {'name': 'Sue Jones', 'age': 35, 'job': ['dev']},
     {'name': 'Ann Smite', 'age': 45, 'job': ['admin', 'dev']}
     ]

import shelve
dbfile = shelve.open('peopledb')
for rec in db:
    dbfile[rec['name']] = rec
dbfile.close()
