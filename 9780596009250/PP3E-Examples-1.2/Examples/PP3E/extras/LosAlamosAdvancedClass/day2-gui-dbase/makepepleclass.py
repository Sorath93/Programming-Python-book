from classdb import People
bob = People('Bob Smith', 40, ['dev', 'mgr'])
sue = People('Sue Jone',  35, ['dev'])
ann = People('Ann Smite', 45, ['admin', 'dev'])

import shelve
db = shelve.open('peopledb3')
recid = 0
for rec in (bob, sue, ann):
    db[str(recid)] = rec
    recid += 1
db.close()
