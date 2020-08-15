class Record:
    recnum = 0
    def __init__(self):
        self.recnum = Record.recnum
        Record.recnum += 1
    def id(self):
        return self.recnum
    def __str__(self):
        res = 'Record: '
        for field in self.__dict__:
            res += '[%s => %s] ' % (field, getattr(self, field))
        return res


