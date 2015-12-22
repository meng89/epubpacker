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

    def set_attribute(self, name, value, nsuri=None):
        self.attributes[(nsuri, name)] = value

    @property
    def string(self, as_root=True,
               inherited_ns=None,
               version='1.0', encoding='utf-8', standalone='yes',
               spaces=0, step_by_step=2):
        s = ''
        if as_root:
            s += '<?xml'
            s += " version='{}'".format(version) if version else ''
            s += " encoding='{}'".format(encoding) if encoding else ''
            s += " standalone='{}'".format(standalone) if standalone else ''

            s += '?>\n'
        s += '' * spaces
        s += '<'
        s += self.namespaces[self.nsuri] + ':' if self.namespaces[self.nsuri] else ''
        s += self.name

        for uri, prefix in self.namespaces.items():
            if uri in inherited_ns.keys() and inherited_ns[uri] == prefix:
                pass

            elif uri:
                if prefix:
                    s += ' xmlns:{}="{}"'.format(prefix, uri)
                else:
                    s += ' xmlns="{}"'.format(uri)

        for attr in self.attributes:
            s += self.namespaces[attr.nsuri] + ':' if self.namespaces[attr.nsuri] else ''

        if self.sub_elements:
            s += '>\n'

            for sub in self.sub_elements:
                inherited_ns_for_subs = inherited_ns.copy()
                inherited_ns_for_subs.update(self.namespaces)
                s += sub.string(as_root=False, asinherited_ns=inherited_ns_for_subs,
                                spaces=spaces+step_by_step, step_by_step=step_by_step)

        else:
            s += ' />\n'

        return s


class Attribute:
    def __init__(self, name, value, nsuri=None):
        self.name = name
        self.value = value
        self.nsuri = nsuri

    def __setattr__(self, key, value):
        if key == 'name':
            pass
        elif key == 'value':
            pass
        elif key == 'nsuri':
            pass
        else:
            raise Exception

        self.__dict__[key] = value
