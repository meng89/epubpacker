#!/bin/env python3

from epubuilder.utils import List

a = List(['a', 'b'])

a.append(1)
a.extend([2, 3, 4, 5, 6])

for one in a:
    print(one)
