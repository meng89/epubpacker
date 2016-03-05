#!/usr/bin/env python3


class C:
    def __init__(self, name):
        self.__dict__['name'] = name

    @property
    def name(self):
        raise
        return self.__dict__['name']

    @name.setter
    def name(self, value):
        self.__dict__['name'] = value


class B:
    pass


"""
名字定死，命名空间定死。

属性: 必用属性, 选用属性，属性值限定， 外部函数检测值

子元素: 必用子元素， 子元素数量， 顺序。

"""

b = B()

b2 = b.__class__()
