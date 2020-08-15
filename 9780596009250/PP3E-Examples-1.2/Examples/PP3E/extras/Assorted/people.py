class People:
    def __init__(self, name, zid, job=None, pay=0):
        self.name = name
        self.zid  = zid
        self.job  = job
        self.pay  = pay
    def lastName(self):
        return self.name.split()[-1]
    def giveRaise(self, percent):
        self.pay *= (1.0 + percent)
    def __str__(self):
        return '[People: %s, %s, %s]' % (self.name.upper(), self.zid, self.pay)

class Manager(People):
    def __init__(self, name, zid, pay):
        People.__init__(self, name, zid, 'mgr', pay)
    def giveRaise(self, percent, bonus=.10):
        People.giveRaise(self, (percent + bonus))

def makeBob():
    return People('Bob Smith')

if __name__ == '__main__':
    bob = People('Bob Smith', '123456')
    sue = People('Sue Jones', '654321', job='dev', pay=60000)
    print bob
    print sue
    print bob.lastName(), sue.lastName()
    sue.giveRaise(.10)
    print sue
    tom = Manager('Tom Jones', '234567', 80000)
    tom.giveRaise(.10)
    print tom
    
