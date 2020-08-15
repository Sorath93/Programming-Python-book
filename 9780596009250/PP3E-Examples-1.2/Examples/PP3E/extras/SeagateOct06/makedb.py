from person import Person, Manager
bob = Person('Bob Smith')
sue = Person('Sue Jones', job='dev', pay=70000)
tom = Manager('Tom Jones', 50000)

import shelve
db = shelve.open('sgdb')
db['bob'] = bob
db['sue'] = sue
db['tom'] = tom
db.close()
