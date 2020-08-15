import pickle
dbfile = open('people-pickle')
db = pickle.load(dbfile)
dbfile.close()

db['sue']['pay'] *= 1.10
db['tom']['name'] = 'Tom Tom'

dbfile = open('people-pickle', 'w')
pickle.dump(db, dbfile)
dbfile.close()
