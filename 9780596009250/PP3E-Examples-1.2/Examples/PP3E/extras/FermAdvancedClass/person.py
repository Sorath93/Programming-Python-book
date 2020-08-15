class Person:
    def __init__(self, name, job):
        self.name = name
        self.job = job
    def upperName(self):
        return self.name.upper() * 8
