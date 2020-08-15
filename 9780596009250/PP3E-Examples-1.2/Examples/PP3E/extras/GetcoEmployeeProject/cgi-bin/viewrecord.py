import cgi, sys
form = cgi.FieldStorage()
print 'Content-type: text/html\n'
print '<H1>', form['key'].value, '</H1>'

from ZODB import FileStorage, DB
storage = FileStorage.FileStorage('zodb1.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

try:
    key = form['key'].value
    rec = root[key]
    print '<table>' 
    fields = rec.__dict__.keys()
    for field in fields:
        print ('<tr><th>%s<td>%s' %
               (cgi.escape(field),
                cgi.escape(str(getattr(rec, field))) ))
    print '</table>'
finally:
    storage.close()
