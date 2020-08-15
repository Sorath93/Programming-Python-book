errs = open('errorlog', 'a')
while True:
    inp = raw_input('Enter age:')
    if inp == 'stop': break
    try:
        num = int(inp)
    except:
        print >> errs, 'Bad input!'
        print '(see log file)'
    else:
        if num > 60:
            print 'old' * 2
        elif num > 40:
            print 'old'
        else:
            print num ** 2

print 'bye'


