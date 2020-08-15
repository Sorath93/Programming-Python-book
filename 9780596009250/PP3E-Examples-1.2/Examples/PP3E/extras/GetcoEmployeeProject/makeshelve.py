from employee  import Employee
from adminEmpl import AdminEmpl
from engrEmpl  import EngrEmpl

bob = Employee(50, 'Bob', 'Smith')
ann = Employee(60, 'Ann', 'Smith')
sue = AdminEmpl(20, 60, 'Sue', 'Jones')
tom = EngrEmpl(80000, 'Tom', 'Jones')
joe = EngrEmpl(90000, 'Joe', 'Blo')

from ZODB import FileStorage, DB
storage = FileStorage.FileStorage('zodb1.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

for emp in (bob, sue, tom, ann, joe):
    root[str(emp.name)] = emp            # eg: db['Smith, Bob'] = bob

import transaction
transaction.commit()
storage.close()
