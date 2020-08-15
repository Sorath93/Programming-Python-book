from person import Person, Manager
bob = Person('Bob Smith')
sue = Person('Sue Jones', job='dev', pay=80000)
tom = Manager('Tom Jones', 60000)

import shelve
db = shelve.open('mt1db')
db['bob'] = bob
db['sue'] = sue
db['tom'] = tom
db.close()

