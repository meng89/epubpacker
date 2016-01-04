#!/bin/env python3


from .baseclasses import List, Dict, Str, Limit


import xml.parsers.expat


def create_element(file):
    element = None

    elements = []

    ns_list = []

    string = ''

    def start_element(name, attrs):
        print('start_element',name)

        attributes = Attributes()

        l = name.rsplit(' ', 1)
        tag = l[-1]
        uri = None

        if len(l) > 1:
            uri = l[0]

        for key, value in attrs.items():
            l = key.rsplit(' ', 1)
            attr_name = l[-1]
            attr_uri = None
            if len(l) > 1:
                attr_uri = l[0]

            attributes.append(Attribute(attr_name, value, attr_uri))

        namespaces = Namespaces()

        for _uri, _prefix in ns_list:
            namespaces[_uri] = _prefix

        e = Element(tag, uri, namespaces, attributes)

        if elements:
            elements[-1].children.append(e)

        elements.append(e)

        nonlocal element
        if not element:
            element = e

    def end_element(name):
        print('end_element', name)
        elements.pop()

    def start_namespace(prefix, uri):
        print('start_namespace')
        ns_list.append((uri, prefix))

    def end_namespace(prefix):
        print('end_namespace')
        ns_list.pop()

    def character_data_handler(data):
        print('Character data: "{}"'.format(data))
        nonlocal string
        string += data

    def _do_string():
        nonlocal string
        stripped_string = string.strip()
        if stripped_string:
            s = String(stripped_string)
            elements[-1].children.append(s)
        string = ''

    p = xml.parsers.expat.ParserCreate(namespace_separator=' ')

    p.StartElementHandler = start_element

    p.EndElementHandler = end_element

    p.StartNamespaceDeclHandler = start_namespace

    p.EndNamespaceDeclHandler = end_namespace

    p.CharacterDataHandler = character_data_handler

    p.Parse(open(file).read(), 1)

    return element


class ObjectAttributeError(Exception):
    pass


def _name_check(name):
    pass


def _nsmap_check(nsmap):
    pass


def _nsuri_check(uri, namespaces):
    if uri is None:
        pass
    elif uri not in namespaces.keys():
        raise Exception


def xml_header(version='1.0', encoding='utf-8', standalone='yes'):
    s = ''
    s += '<?xml'
    s += " version='{}'".format(version) if version else ''
    s += " encoding='{}'".format(encoding) if encoding else ''
    s += " standalone='{}'".format(standalone) if standalone else ''
    s += '?>\n'
    return s


class String(Str):
    def string(self):
        s = ''
        for char in self:
            if char == '&':
                s += '&amp;'
            elif char == '<':
                s += '&lt;'
            elif char == '>':
                s += '&gt;'
            elif char == '"':
                s += '&quot;'
            elif char == "'":
                s += '&apos;'
            else:
                s += char
        return s


class Element:
    def __init__(self, name, uri=None, namespaces=None, attributes=None):
        self.namespaces = namespaces or Namespaces()
        self.attributes = attributes or Attributes()

        self.name = name
        self.uri = uri

        self.children = Children()

    def __setattr__(self, key, value):

        if key == 'name':
            _name_check(value)

        elif key == 'uri':
            _nsuri_check(value, self.namespaces)

        elif key == 'namespaces':
            if not isinstance(value, Namespaces):
                raise ObjectAttributeError

        elif key == 'attributes':
            if not isinstance(value, Attributes):
                raise ObjectAttributeError

        elif key == 'children':
            if not isinstance(value, Children):
                raise ObjectAttributeError

        else:
            raise ObjectAttributeError

        self.__dict__[key] = value

    def string(self, inherited_namespaces=None, spaces=0, step_by_step=4):

        inherited_ns = inherited_namespaces or Namespaces()

        indentation = ' ' * spaces

        s = ''
        s += indentation
        s += '<'

        name_prefix = self.namespaces[self.uri] + ':' if (self.uri and self.namespaces[self.uri]) else ''
        name_prefix += self.name

        s += name_prefix

        for uri, prefix in self.namespaces.items():
            if uri in inherited_ns.keys() and inherited_ns[uri] == prefix:
                pass

            elif uri:
                if prefix:
                    s += ' xmlns:{}="{}"'.format(prefix, uri)
                else:
                    s += ' xmlns="{}"'.format(uri)

        for attr in self.attributes:
            s += ' '
            if attr.uri:
                s += self.namespaces[attr.uri] + ':'

            s += attr.name
            s += '="{}"'.format(attr.value)

        if self.children:
            s += '>\n'

            for sub in self.children:
                inherited_ns_for_subs = inherited_ns.copy()
                inherited_ns_for_subs.update(self.namespaces)
                s += sub.string(inherited_namespaces=inherited_ns_for_subs,
                                spaces=spaces+step_by_step, step_by_step=step_by_step)
            s += indentation
            s += '</'
            s += name_prefix
            s += '>\n'

        else:
            s += ' />\n'

        return s


class Children(List):
    pass


class Namespaces(Dict):
    pass


class Namespace:
    def __init__(self, uri, prefix):
        self.uri = uri
        self.prefix = prefix

    def __setattr__(self, key, value):
        if key == 'uri':
            pass
        elif key == 'prefix':
            pass

        self.__dict__[key] = value


class Attributes(List):
    pass


class Attribute:
    def __init__(self, name, value, nsuri=None):
        self.name = name
        self.value = value
        self.uri = nsuri

    def __setattr__(self, key, value):
        if key == 'name':
            pass
        elif key == 'value':
            pass
        elif key == 'uri':
            pass
        else:
            raise Exception

        self.__dict__[key] = value


def main():
    e = create_element('/media/data/temp/1/META-INF/container.xml')
    print(e.string())


if __name__ == '__main__':
    main()

