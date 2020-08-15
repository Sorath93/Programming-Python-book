print 'I am:', __name__

def mm(mycmp, *args):
    res = args[0]
    for x in args[1:]:
        if mycmp(x, res):
            res = x
    return res


def lt(x, y): return x < y
def gt(x, y): return x > y

if __name__ == '__main__':
    print mm(lt, 3, 1, 2)
    print mm((lambda x, y: x > y), 'bb', 'aa')
