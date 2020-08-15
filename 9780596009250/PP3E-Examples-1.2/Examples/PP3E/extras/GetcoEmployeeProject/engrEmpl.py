import employee

class EngrEmpl(employee.Employee):
    def __init__(self, salary, first, last):
        self.salary = salary
        self.name = employee.Name(first, last)
    def display(self):
        return self.salary

if __name__ == '__main__':
    tom = EngrEmpl(80000, 'Tom', 'Jones')
    print tom
    print tom.salary
    
