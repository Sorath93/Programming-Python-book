import time
reps = 1000
size = 10000

def tester(func, *args):
    startTime = time.time()
    for i in range(reps):
        func(*args)
    elapsed = time.time() - startTime
    return elapsed

def forLoop():
    res = []
    for x in range(size):
        res.append(abs(x))

def listComp():
    res = [abs(x) for x in range(size)]

def mapFunc():
    res = map(abs, range(size))

for testfunc in (forLoop, listComp, mapFunc):
    print testfunc.__name__, tester(testfunc)

