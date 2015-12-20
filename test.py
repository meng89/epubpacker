#!/bin/env python3

import xml.etree.ElementTree as Et


class C:
    def __init__(self, s=None):
        self._s = s or 'hello world'

    def string(self):
        print(self._s)


def check(fn):
    def wapper(self):
        print('here')
        fn(self)
    return wapper


class Myc(C):
    pass

Myc.string = check(Myc.string)


c2 = Myc('b')
c2.string()

def fuck(fn):
    print("fuck %s!"% fn.__name__[::-1].upper())

@fuck
def wfg():
    pass
