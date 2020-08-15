fromdir = '/cygdrive/c/Mark/PP3E-Final-Examples/Examples'
todir   = '/cygdrive/c/Mark/PP3E-temp-Final-Examples/Examples'

import os
for file in os.popen('find %s -name __init__.py -print' % fromdir):
    file = file.rstrip()
    #print file
    lenprefix = len(fromdir.split(os.sep))
    relativepart = os.sep.join(file.split(os.sep)[lenprefix:])
    target = os.path.join(todir, relativepart)
    #print target   
    print relativepart

    try:
        if os.path.exists(target):
            doit = raw_input('already exists; replace?')
        else:
            doit = raw_input('not present; copy?')
        if doit in ['y', 'Y']:
            try:
                source = open(file).read()
                open(target, 'w').write(source)
                print 'copied'
            except:
                print 'copy failed'
    except:
        print 'could not check file'
    print

