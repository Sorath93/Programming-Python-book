class MinMax:
    def mm(self, *args):
        res = args[0]
        for x in args[1:]:
            if self.docmp(x, res):      # define me in subclass
                res = x
        return res

class Min(MinMax):
    def docmp(self, x, y):
        return x < y

class Max(MinMax):
    def docmp(self, x, y):
        return x > y

if __name__ == '__main__':
    obj = Min()
    print obj.mm('cc', 'aa', 'bb')
    obj= Max()
    print obj.mm(3, 2, 4, 1)
    
