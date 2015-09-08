#!/bin/env python3


import os

f = 'Text/cover.xhtml'


def splitall(path):
    parts = os.path.split(path)
    if parts[1] == path:        # 'a' -> ['', 'a']
        return [parts[1]]
    elif parts[1] == '':
        if parts[0] == path:  # '/' -> ['/', '']
            return [parts[0]]
        else:                 # 'a/b/ - > ['a/b', '']
            return splitall(parts[0])
    else:                     # '/a' -> ['/', 'a']
        return splitall(parts[0]) + [parts[1]]


p = ('a', 'b', 'c', '1.txt')

d1 = ('a', 'b')
d2 = ('a', 'b', 'c', 'd', 'e')
d3 = ('a', 'e', 'c', 'z')


