#!/bin/env python3

from epubuilder.xl import Element

e = Element('root', nsuri='jbm', ns_d={'jbm': 'gp'})

print(e.string)