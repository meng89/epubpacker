#!/usr/bin/env python3


class D(object):
    def __init__(self, value):
        self.value = value

<<<<<<< HEAD
    def __get__(self, instance, owner):
        print('get invoke')
        return self.value
=======
    @property
    def name(self):
        raise
        return self.__dict__['name']
>>>>>>> 0f5241ee6a9c450364f9c30a62acc9c253e685b1

    def __set__(self, instance, value):
        print('set invoke')
        self.value = value

d = D('default')

<<<<<<< HEAD

class X(object):
    v = d
=======
class B:
    pass

>>>>>>> 0f5241ee6a9c450364f9c30a62acc9c253e685b1

"""
名字定死，命名空间定死。

属性: 必用属性, 选用属性，属性值限定， 外部函数检测值

子元素: 必用子元素， 子元素数量， 顺序。

"""

<<<<<<< HEAD
x = X()

x.v = 3

x.x = 4


print(x.__dict__)


=======
b = B()

b2 = b.__class__()
>>>>>>> 0f5241ee6a9c450364f9c30a62acc9c253e685b1
