#!/usr/bin/env python3

"""
名字定死，命名空间定死。

属性: 必用属性, 选用属性，属性值限定， 外部函数检测值

子元素: 必用子元素， 子元素数量， 顺序。

"""


def attr_name_checkfunc(name):
    pass


def attr_value_checkfunc(value):
    pass


def child_name_checkfunc(name):
    pass


def final_checkfunc(e):
    pass


descriptor = {
    'freeze_name': True,

    'attrs': {
        'name_checkfunc': attr_name_checkfunc,
        'value_checkfuncs': {
            'id': attr_value_checkfunc,
            'dir': attr_value_checkfunc
        },
    },

    'children': {
        'name_checkfunc': child_name_checkfunc,
        'descriptors': {''},
    },
}
