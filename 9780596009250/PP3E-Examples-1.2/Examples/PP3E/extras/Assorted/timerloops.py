import time
callreps = 50
loopreps = 100000
loopinit = range(loopreps)

def timer(func, *args):
    startTime = time.clock()
    for x in range(callreps):
        res = func(*args)
    return time.clock() - startTime     # drop res

if __name__ == '__main__':

    def testFor():
        res = []
        for i in loopinit:
            res.append(i)
        return res

    def testComp():
        return [i for i in loopinit]

    def testMap(): 
        return map(lambda i: i, loopinit)

    for test in (testFor, testComp, testMap):
        totTime = timer(test)
        print test.__name__, '=>', totTime
