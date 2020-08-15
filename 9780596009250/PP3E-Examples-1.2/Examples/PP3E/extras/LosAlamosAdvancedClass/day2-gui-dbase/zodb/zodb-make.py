from ZODB import FileStorage, DB
storage = FileStorage.FileStorage(r'C:\Mark\temp\mydb.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

object1 = (1, 'spam', 4, 'YOU')
object2 = [[1, 2, 3], [4, 5, 6]]
object3 = {'name': ['Bob', 'Doe'], 'age': 42, 'job': ('dev', 'mgr')}
object2.append([7, 8, 9])

root['mystr']   = 'spam' * 3
root['mytuple'] = object1
root['mylist']  = object2
root['mydict']  = object3
print root['mylist']

import transaction
transaction.commit()
storage.close()
