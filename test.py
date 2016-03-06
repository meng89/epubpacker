#!/usr/bin/env python3

"""
名字定死，命名空间定死。

属性: 必用属性, 选用属性，属性值限定， 外部函数检测值

子元素: 必用子元素， 子元素数量， 顺序。

"""


def element_name_checkfunc(name):
    pass


def attr_name_checkfunc(name):
    pass


def attr_value_checkfunc(value):
    pass


def child_name_checkfunc(name):
    pass


def final_checkfunc(e):
    pass


descriptor = {
    'name_checkfunc': element_name_checkfunc,

    'attributes': {
        'name_checkfunc': attr_name_checkfunc,
        'value_checkfuncs': {
            ('xxx', 'id'): attr_value_checkfunc,
            ('xxx', 'dir'): attr_value_checkfunc
        },
    },

    'children': {
        'name_checkfunc': child_name_checkfunc,
        'descriptors': {''},
    },
}


from collections import UserList


class List(UserList):

    def __init__(self, initlist=None, hook=None, hook_when_init=True):
        self._hooks = []
        if hook:
            self._hooks.append(hook)

        super().__init__()

        if initlist:
            if hook_when_init:
                self.data.extend(initlist)
            else:
                self.extend(initlist)

    def __setitem__(self, i, item):  # x[i] = item, del and add

        del self[i]

        self.insert(i, item)

    # all del action should be here
    def __delitem__(self, i):  # del x[i], del
        [hook.del_before(key=i, obj=self) for hook in self._hooks]
        del self.data[i]

        [hook.add_after(key=i, obj=self) for hook in self._hooks]

    def append(self, item):  # add
        self.insert(len(self), item)

    # all add action should be here
    def insert(self, i, item):
        [hook.add_before(key=i, item=item, obj=self) for hook in self._hooks]

        self.data.insert(i, item)

        [hook.add_after(key=i, item=item, obj=self) for hook in self._hooks]

    def pop(self, i=-1):  # del
        x = self[i]
        del self[i]
        return x

    def remove(self, item):  # del
        i = self.index(item)
        del self[i]

    def clear(self):  # del
        for i in range(len(self)):
            self.pop()

    def extend(self, other):  # add
        for item in other:
            self.append(item)

    def __iadd__(self, other):  # x += y, add
        self.extend(other)
        return self

    def __imul__(self, n):  # x *= y, add
        old_data = self.copy()
        for x in range(n):
            self.extend(old_data)
        return self

a = List([1, 2, 3, 4])

