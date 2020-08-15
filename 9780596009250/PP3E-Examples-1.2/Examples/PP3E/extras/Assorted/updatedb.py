import shelve
db = shelve.open('bnrmay')

bob = db['bob']
print bob, bob.lastName()

print db.keys(), len(db)
for key in db.keys():
    print key, '=>', db[key]

sue = db['sue']
sue.giveRaise(.10)
db['sue'] = sue

from person import Person
ann = Person('Ann Smith')
db['ann'] = ann
db.close()
