while True:
    inp = raw_input('Enter age:')
    if inp == 'stop': break
    try:
        num = int(inp)
    except:
        print 'Bad!' * 8
    else:
        print num ** 2
print 'bye'
