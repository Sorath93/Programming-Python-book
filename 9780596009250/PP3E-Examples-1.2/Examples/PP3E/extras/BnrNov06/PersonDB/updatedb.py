import shelve
db = shelve.open('bnrdb')
tom = db['tom']
print tom, tom.lastName()

print db.keys(), len(db)
for key in db:
    print key, '=>', db[key]

sue = db['sue']
sue.giveRaise(.10)
db['sue'] = sue
db.close()


