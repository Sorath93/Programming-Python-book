import timematrix
text = 'abcdefghijklmnop' * 100

def mapCall():
    res = map(ord, text)
    
def listComp():
    res = [ord(c) for c in text]

def forLoop():
    res = []
    for c in text:
        res.append(ord(c))

print timematrix.timer(listComp)
print timematrix.timer(forLoop)
print timematrix.timer(mapCall)
