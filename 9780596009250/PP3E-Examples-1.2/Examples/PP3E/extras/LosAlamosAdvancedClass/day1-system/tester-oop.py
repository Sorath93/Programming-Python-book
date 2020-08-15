import os

class TestCase:
    def __init__(self, program, args='', output='output'):
        self.program = program
        self.args    = args
        self.output  = output
    def run(self, failures):
        command = '%s %s' % (self.program, self.args)
        if not os.path.exists(self.output):
            print 'Generating', self.output
            output = os.popen(command).read()
            file = open(self.output, 'w')
            file.write(output)
            file.close()
        else:
            newlines = os.popen(command).readlines()
            oldlines = open(self.output).readlines()
            failed = self.findDiff(newlines, oldlines)
            failures.extend([[command] + fail for fail in failed])
    def findDiff(self, newlines, oldlines):
        raise NotImplementedError, 'findDiff'

class TestLines(TestCase):
    def findDiff(self, newlines, oldlines):
        failures = []
        combined = map(None, newlines, oldlines)
        for (ix, (newline, oldline)) in enumerate(combined):
            if newline != oldline:
                failures.append([ix, newline, oldline])
        return failures

class TestText(TestCase):
    def findDiff(self, newlines, oldlines):
        failures = []
        newtext = ''.join(newlines)
        oldtext = ''.join(oldlines)
        if newtext != oldtext:
            failures.append(['<text differs>'])
        return failures
        
class TestNumeric(TestCase):
    def findDiff(self, newlines, oldlines):
        failures = []
        for (ix, (newline, oldline)) in enumerate(combined):
            newnums = [round(float(x), 2) for x in split(newline, ',')]
            oldnums = [round(float(x), 2) for x in split(oldline, ',')]
            if newnums != oldnums:
                failures.append([ix, newline, oldline])
        return failures
    
class TestSuite:
    def run(self, tests):
        failures = []
        for test in tests:
            test.run(failures)
        self.report(failures)
    def report(self, failures):     # customize me
        if not failures:
            print 'All passed'
        else:
            print 'Failures:'
            for failure in failures:
                print failure

if __name__ == '__main__':
    tests = [TestLines('sqrt.py', output='sqrt.out'),
             TestText('strings.py', 'SPAM!', 'strings-spam.out'),
             TestLines('strings.py', 'Ni',    'strings-ni.out')
             ]
    TestSuite().run(tests)
