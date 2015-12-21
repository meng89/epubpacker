# xl means xml without mess

import xml.etree.ElementTree as Et

from epubuilder.baseclasses import List, Dict


class ObjectAttributeError(Exception):
    pass


def _name_check(name):
    pass


def _nsmap_check(nsmap):
    pass


def _nsuri_check(nsuri, namespaces):
    if nsuri not in namespaces.keys():
        pass
        raise Exception
    pass


class Element(object):
    def __init__(self, name, nsuri=None, namespaces=None):

        self.__dict__['attributes'] = List()

        self.__dict__['namespaces'] = Dict(namespaces or {None: None})

        self.__dict__['sub_elements'] = List()

        self.name = name

        self.nsuri = nsuri

    def __setattr__(self, key, value):
        print('__setattr__: key: {}, value: {}'.format(key, value))

        if key == 'name':
            _name_check(value)

        elif key == 'nsuri':
            _nsuri_check(value, self.namespaces)

        else:
            raise ObjectAttributeError

        self.__dict__[key] = value

    # def __getattribute__(self, key):
    #    print('__getattribute__: key: {}'.format(key))
    #    return super().__getattribute__(key)

    @property
    def attributes(self):
        return self.__dict__['attributes']

    @property
    def namespaces(self):
        return self.__dict__['namespaces']

    @property
    def sub_elements(self):
        return self.__dict__['sub_elements']

    @property
    def string(self):
        s = ''
        s += '<'
        s += self.namespaces[self.nsuri] + ':' if self.namespaces[self.nsuri] else ''
        s += self.name
        for uri, prefix in self.namespaces.items():
            if uri:
                if prefix is None:
                    s += ' xmlns="{}"'.format(uri)
                else:
                    s += ' xmlns:{}="{}"'.format(prefix, uri)

        for attr in self.attributes:
            pass

        if self.sub_elements:
            s += '>'

            for sub in self.sub_elements:
                pass

            s += '</'
            s += self.namespaces[self.nsuri] + ':' if self.namespaces[self.nsuri] else ''
            s += self.name
            s += '>'
        else:
            s += ' />'

        return s


class Attribute:
    def __init__(self, name, nsuri=None, value=None):
        pass



