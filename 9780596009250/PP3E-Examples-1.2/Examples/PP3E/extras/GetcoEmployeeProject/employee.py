class Employee:
    "general employee class"
    def __init__(self, rate, first, last):
        self.rate = rate
        self.name = Name(first, last)
    def salary(self, hours):
        "weekly pay"
        return self.rate * hours
    def display(self):
        return self.rate
    def __str__(self):
        return '<name=%s, data=%s>' % (self.name, self.display())

class Name:
    def __init__(self, first, last, middle=None):
        self.name = (first, middle, last)
    def lastName(self):
        return self.name[-1]
    def __str__(self):
        return "[%s, %s]" % (self.name[-1], self.name[0])
        
if __name__ == '__main__':
    bob = Employee(50, 'Bob', 'Smith')
    print bob.salary(40)
    print bob
