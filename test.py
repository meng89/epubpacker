#!/usr/bin/env python3

from epubuilder2.package import package_descriptor
from xl import Element

p = Element((None, 'package'))

p.descriptor = package_descriptor

p.children.append(Element(name=(None, 'metadata')))

print(package_descriptor)
