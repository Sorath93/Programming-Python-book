import shelve
db = shelve.open('mt1db')
bob = db['bob']
print bob.lastName(), bob

print db.keys(), len(db)
for key in db:
    print key, '=>', db[key]

sue = db['sue']
sue.giveRaise(.10)
db['sue'] = sue
db.close()   
