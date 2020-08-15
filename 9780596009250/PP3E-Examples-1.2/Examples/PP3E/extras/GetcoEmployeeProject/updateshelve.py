from ZODB import FileStorage, DB
storage = FileStorage.FileStorage('zodb1.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

for key in root.keys():
    print key, '=>', root[key]

joe = root['[Blo, Joe]']
joe.salary += 10000
root['[Blo, Joe]'] = joe

import employee
tim = employee.Employee(40, 'Tim', 'Jones')
root[str(tim.name)] = tim

import transaction
transaction.commit()
storage.close()
