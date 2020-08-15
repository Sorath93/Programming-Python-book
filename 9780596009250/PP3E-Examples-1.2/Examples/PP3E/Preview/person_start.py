class Person:
    def __init__(self, name, age, pay=0, job=None):
        self.name = name
        self.age  = age
        self.pay  = pay
        self.job  = job

if __name__ == '__main__':		
    bob = Person('Bob Smith', 42, 30000, 'sweng')
    sue = Person('Sue Jones', 45, 40000, 'music')
    print bob.name, sue.pay

    print bob.name.split()[-1]
    sue.pay *= 1.10
    print sue.pay
