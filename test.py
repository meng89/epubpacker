#!/bin/env python3


class MyDecorator(object):
    def __init__(self, fn):
        print("inside MyDecorator.__init__()")
        self.fn = fn

    def __call__(self):
        self.fn()
        print("inside MyDecorator.__call__()")


@MyDecorator
def a_function():
    print("inside a_function()")


print("Finished decorating a_function()")

a_function()

