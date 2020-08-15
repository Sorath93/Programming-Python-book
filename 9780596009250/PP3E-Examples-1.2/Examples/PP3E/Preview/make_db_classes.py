import shelve
from person import Person
from manager import Manager

bob = Person('Bob Smith', 42, 30000, 'sweng')
sue = Person('Sue Jones', 45, 40000, 'music')
tom = Manager('Tom Doe',  50, 50000)

db = shelve.open('class-shelve')
db['bob'] = bob
db['sue'] = sue
db['tom'] = tom
db.close()
