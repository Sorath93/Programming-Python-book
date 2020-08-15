while True:
    inp = raw_input('Enter age:')
    if inp == 'stop': break
    try:
        num = int(inp)
    except:
        print 'bad'
    else:
        print num ** 2
print 'bye'
