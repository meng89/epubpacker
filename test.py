#!/bin/env python3


def fun1():
    a = 0

    def fun2():
        a += 1


    return fun2()

print(fun1())