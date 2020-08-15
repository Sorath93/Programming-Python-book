print 'I am:', __name__

def mm(mycmp, *args):
    res = args[0] 
    for arg in args[1:]:
        if mycmp(arg, res):
            res = arg
    return res

def lt(x, y): return x < y
#def gt(x, y): return x > y

if __name__ == '__main__':
    print mm(lt, 'bb', 'aa')
    print mm((lambda x, y: x > y), 3, 1, 2)
