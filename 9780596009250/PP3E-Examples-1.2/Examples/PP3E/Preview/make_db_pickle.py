from initdata import db
import pickle
dbfile = open('people-pickle', 'w')
pickle.dump(db, dbfile)
dbfile.close()
