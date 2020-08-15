import timematrix
size = 1000

def listComp():
    res = [x + y for x in range(size) for y in range(size)]

def forLoop():
    res = []
    for x in range(size):
        for y in range(size):
            res.append(x + y)

print timematrix.timer(listComp, reps=100)
print timematrix.timer(forLoop, reps=100)
