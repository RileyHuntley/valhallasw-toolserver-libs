import a

class class1(a.class1):
    def output(self):
        print("b.class1")

class class2(a.class2):
    def test2(self):
        a = class1()
        a.output()
