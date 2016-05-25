#!/usr/bin/env python3


import test

setattr(test, 'aaa', 'hello world!j')

from test import aaa

print(aaa)
