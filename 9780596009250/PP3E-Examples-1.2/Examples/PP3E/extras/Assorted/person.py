class Person:
    imgdir = 'C:\\Mark\\training-cd\\Extras\\Gui\\gifs\\'
    def __init__(self, name, job=None, pay=None, phone=None, photo=None):
        self.name  = name
        self.job   = job
        self.pay   = pay
        self.phone = phone
        self.photo = photo
    def lastName(self):
        return self.name.split()[-1]
    def giveRaise(self, percent):
        self.pay *= (1.0 + percent)
    def showPhoto(self):
        import os
        os.startfile(self.photo)
    def __str__(self):
        return '[Person: name=%s, pay=%s]' % (self.name, self.pay)

class Manager(Person):
    def giveRaise(self, percent, bonus=.10):
        Person.giveRaise(self, percent + bonus)

if __name__ == '__main__':
    bob = Person('Bob Smith')
    sue = Person('Sue Jones', job='dev', pay=50000,
                 phone='867-5309',
                 photo=Person.imgdir + 'python_conf_ora.gif')
    print bob
    print bob.lastName(), sue.lastName()
    sue.giveRaise(.10)
    print sue
    tom = Manager('Tom Jones', 'mgr', 40000)
    tom.giveRaise(.10)
    print tom
    sue.showPhoto()
