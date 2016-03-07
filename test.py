#!/usr/bin/env python3

from epubuilder.xl import Element
from epubuilder.package import package_descriptor

p = Element((None, 'package'))

p.descriptor = package_descriptor

p.children.append(Element(name=(None, 'metadata')))

print(package_descriptor)
