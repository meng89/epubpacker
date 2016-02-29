#!/bin/env python3

import sys
sys.path.append('..')

import xml.etree.ElementTree as Et

from epubuilder.xl import parse, clean, insert_for_pretty


def main():
    file = '1.xml'
    e = parse(file)
    cleaned_e = clean(e)
    pretty_e = insert_for_pretty(cleaned_e)

    print('#### element:')
    print(e.to_string())
    print()

    print('#### clean element:')
    print(cleaned_e.to_string())
    print()

    print('#### pretty element:')
    print(pretty_e.to_string())
    print()


    e = Et.ElementTree(file=file)
    e.write('et.xml')
    print('#### etree:')
    print(open('et.xml').read())


if __name__ == '__main__':
    main()
