import os                                  # delete old output files in tree
from PP3E.PyTools.find import find         # only need full path if I'm moved
for filename in find('*.out.txt'):
    print filename
    if raw_input('View?') == 'y':
        print open(filename).read()
    if raw_input('Delete?') == 'y':
        os.remove(filename)
