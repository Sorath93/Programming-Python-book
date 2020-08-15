from person import Person
import shelve
db = shelve.open('fermi1')
db['bob'] = Person('Bob', 'dev')
db['sue'] = Person('Sue', 'mgr')
db.close()
