rec = {'name': {'first': 'Bob', 'last': 'Smith'},
       'job':  ['dev', 'mgr'],
       'age':  40.5}

import pickle
db = open('bobfile', 'w')
pickle.dump(rec,  db)
db.close()
