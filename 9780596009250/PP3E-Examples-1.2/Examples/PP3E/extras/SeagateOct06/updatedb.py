import shelve
db = shelve.open('sgdb')
bob = db['bob']
print bob.lastName(), bob

print db.keys(), len(db)
for key in db:
    print key, '=>', db[key]

sue = db['sue']
sue.giveRaise(.10)
db['sue'] = sue
db.close()



