#!/usr/bin/env python3

import sys
sys.path.append('..')

import xml.etree.ElementTree as Et

import xl as xl


def main():
    file = '1.xml'
    e = xl.parse(open(file).read())
    cleaned_e = xl.clean(e)
    pretty_e = xl.insert_for_pretty(cleaned_e)

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
