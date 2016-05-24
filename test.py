#!/usr/bin/env python3

from epub.metadata import meta


M = meta('Creator')
m = M()

t = meta('dc:title')

print(isinstance(m, M))
