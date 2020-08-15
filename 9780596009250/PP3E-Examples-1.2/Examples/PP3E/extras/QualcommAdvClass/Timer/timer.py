import time
reps = range(1000000)

def timer(func, *args):
    startTime = time.clock()
    func(*args)
    return time.clock() - startTime

def forLoop():
    tmp = []
    for i in reps:
        tmp.append(1)

def listComp():
    tmp = [1 for i in reps]

def mapCall():
    tmp = map((lambda x: 1), reps)

def testSeqs():
    for func in (forLoop, listComp, mapCall):
        print func.__name__,
        print timer(func)

if __name__ == '__main__':
    testSeqs()
    
