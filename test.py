#!/bin/env python3
import copy


class C(object):
    def __init__(self, name):
        self.__dict__['name'] = name

    @property
    def name(self):
        return self.__dict__['name']

    @name.setter
    def name(self, value):
        self.__dict__['name'] = value


def r():
    raise Exception

C2 = copy.deepcopy(C)

c1 = C2('jbm')
c1.name = '23333'
print(c1.name)


C.name.setter = r()

c1.name = '24444'
print(c1.name)
