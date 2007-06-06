class class1:
    def output(self):
        print 'a.class1'

class class2:
    def __init__(self):
        self.c = class1()

    def test(self):
        self.c.output()
        d = class1()
        d.output()
