import sys
sys.stdin  = open('infile.txt')
sys.stdout = open('logfile.txt', 'w')

while True:
    inp = raw_input('Enter age:')
    if inp == 'stop': break
    num = int(inp)
    if num > 30:
        print 'High:', num
    elif num > 20:
        print 'Mid:', num / 2
    else:
        print 'Low:', num ** 2
print 'bye'
sys.stdout.close()
