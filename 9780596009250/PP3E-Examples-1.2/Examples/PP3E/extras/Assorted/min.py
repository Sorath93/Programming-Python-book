print 'I am', __name__

def mm(mycmp, *args):
    """
    return min among all arguments passed
    """
    res = args[0]
    for v in args[1:]:
        if mycmp(v, res):
            res = v
    return res

def lt(x, y): return x < y

if __name__ == '__main__':
    print mm(lt, 3, 1, 2)
    print mm(lambda x, y: x > y, 'aa', 'bb')
