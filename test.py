#!/bin/env python3


class C:
    def __init__(self):
        self.a = []


class C1(C):
    def __init__(self):
        super().__init__()
        self.a.append(1)


class C2(C1):
    def __init__(self):
        super().__init__()
        self.a.append(2)


c2o1 = C2()
c2o1.a.append(3)
c2o2 = C2()


print(c2o1.a, c2o2.a)
