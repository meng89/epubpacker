#!/bin/env python3
import copy


class C:
    def __init__(self, name):
        self.__dict__['name'] = name

    @property
    def name(self):
        return self.__dict__['name']

    @name.setter
    def name(self, value):
        self.__dict__['name'] = value


class C2(C):
    @C

    @C.name.setter
    def name(self, value):
        raise Exception


c2 = C2('jbm')

c2.name = 'haha'
print(c2.name)
