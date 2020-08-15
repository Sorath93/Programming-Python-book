from employee import Employee

class AdminEmpl(Employee):
    def __init__(self, vacationDays, rate, first, last):
        self.vacat = vacationDays
        Employee.__init__(self, rate, first, last)
    def vacation(self, numDays):
        if numDays > self.vacat:
            return False
        else:
            self.vacat -= numDays
            return True
    def display(self):
        return '%s, %s' % (self.rate, self.vacat)

if __name__ == '__main__':
    sue = AdminEmpl(20, 60, 'Sue', 'Jones')
    print sue
    sue.vacation(10)
    print sue.vacat
            
        
        
