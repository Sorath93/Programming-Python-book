from person import Person, Manager
bob = Person('Bob Smith')
sue = Person('Sue Jones', job='dev', pay=50000,
             phone='867-5309',
             photo=Person.imgdir + 'python_conf_ora.gif')
tom = Manager('Tom Jones', 'mgr', 40000)

import shelve
db = shelve.open('bnrmay')
db['bob'] = bob
db['sue'] = sue
db['tom'] = tom
db.close()

