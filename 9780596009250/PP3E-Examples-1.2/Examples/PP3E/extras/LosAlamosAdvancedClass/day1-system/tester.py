import os
from testcases import tests
failures = []
for test in tests:        
    command = '%s %s' % (test['program'], test['args'])
    if not os.path.exists(test['output']):
        print 'Generating', test['output']
        output = os.popen(command).read()
        file = open(test['output'], 'w')
        file.write(output)
        file.close()
    else:
        output = os.popen(command).readlines()
        oldout = open(test['output']).readlines()
        for (ix, (new, old)) in enumerate( map(None, output, oldout) ):
            if new != old:
                failures.append([command, ix, new, old])

if not failures:
    print 'All tests passed'
else:
    print 'Failures:'
    for command in failures: print command
