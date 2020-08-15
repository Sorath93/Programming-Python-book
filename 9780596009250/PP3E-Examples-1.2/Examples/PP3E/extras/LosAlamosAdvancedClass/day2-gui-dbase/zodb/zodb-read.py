from ZODB import FileStorage, DB
storage= FileStorage.FileStorage(r'C:\Mark\temp\mydb.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

print len(root), root.keys()
print root['mylist']

for key in root.keys():
    print key, '\t=>', root[key]
    
rec = root['mydict']
rec['age'] += 1
rec['job'] = None
root['mydict'] = rec        # change in memory, write back
                            # does not update db: root['bob']['age'] += 1
import transaction          # get_transaction() deprecated, gone in 3.6
transaction.commit()        # same as older: get_transaction().commit()
storage.close()             # 3.6 transaction.get() = get_transaction()

