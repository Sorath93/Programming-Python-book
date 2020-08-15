from person import Person, Manager
bob = Person('Bob Smith')
sue = Person('Sue Jones', job='dev', pay=50000)
tom = Manager('Tom Jones', 40000)

import shelve
db = shelve.open('bnrdb')
db['bob'] = bob
db['sue'] = sue
db['tom'] = tom
db.close()

