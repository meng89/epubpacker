#!/bin/env python3

import xml.etree.ElementTree as Et


s = '''
<a xmlns:as="lsajf">
    1
    <b:as>2</b:as>
    3
</a>
'''
x = Et.fromstring(s)
x.set('xmlns:lang', 'lsfj')
print(Et.tostring(x).decode())