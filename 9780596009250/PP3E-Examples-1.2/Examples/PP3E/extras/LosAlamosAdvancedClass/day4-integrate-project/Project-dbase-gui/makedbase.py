from person import Record
import shelve
filename = raw_input('Data txt file?') or 'peopletext.txt'    # or sys.argv[1]
startrec = '<begin>'
endrec   = '<end>'
dbase = shelve.open(filename.replace('.txt', '.db'))

myfile = open(filename)
while True:
    line = myfile.readline()
    if not line: break
    if line.startswith(startrec):
        newrec = Record()
        while True:
            line = myfile.readline()
            if line.startswith(endrec): break
            field, value = line.split(':')
            value = value.strip()
            setattr(newrec, field, value)
        # store record
        dbase[str(newrec.id())] = newrec
dbase.close()       
