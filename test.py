#!/usr/bin/env python3


class D(object):
    def __init__(self, value):
        self.value = value

    def __get__(self, instance, owner):
        print('get invoke')
        return self.value

    def __set__(self, instance, value):
        print('set invoke')
        self.value = value

d = D('default')


class X(object):
    v = d


x = X()

x.v = 3

x.x = 4


print(x.__dict__)


