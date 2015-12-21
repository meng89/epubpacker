#!/bin/env python3

from epubuilder.xl import Element

e = Element('root', nsuri='jbm', namespaces={'jbm': 'gp'})

print(e.string)