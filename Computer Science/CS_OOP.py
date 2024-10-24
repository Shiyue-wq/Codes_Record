class A:
    def __init__(self, a=100):
        self.a = a


class B:
    def __init__(self, b=200):
        self.b = b


class C(B,A):
    def __init__(self,a,b,c=300):
        super().__init__(a)
        super().__init__(b)
        self.c = c

    def output(self):
        print(self.a)
        print(self.b)
        print(self.c)

if __name__ == '__main__':
    c = C(1,2,3)
    c.output()
