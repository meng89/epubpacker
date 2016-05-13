#!/bin/env python3

import copy

from hooky import List, Dict

from collections import UserString as Str

import xml.parsers.expat


def parse(xmlstr, debug=False):
    element = None

    elements = []

    ns_list = []

    s = ''

    def start_element(name, attrs):
        _do_string()

        print('start_element', name) if debug else None

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

            attributes[(attr_uri, attr_name)] = value

        namespaces = Prefixes()

        for _uri, _prefix in ns_list:
            namespaces[_uri] = _prefix
        print(tag, uri, namespaces, attributes)
        print()
        e = Element((uri, tag), namespaces, attributes)

        if elements:
            elements[-1].children.append(e)

        elements.append(e)

        nonlocal element
        if not element:
            element = e

    def end_element(name):
        _do_string()
        print('end_element', name) if debug else None
        elements.pop()

    def start_namespace(prefix, uri):
        print('start_namespace') if debug else None
        ns_list.append((uri, prefix))

    def end_namespace(prefix):
        print('end_namespace') if debug else None
        ns_list.pop()

    def character_data_handler(data):
        print('Character data: "{}"'.format(data)) if debug else None
        nonlocal s
        s += data

    def _do_string():
        nonlocal s
        if s and elements:
            string = Text(s)
            elements[-1].children.append(string)
            s = ''

    p = xml.parsers.expat.ParserCreate(namespace_separator=' ')

    p.StartElementHandler = start_element

    p.EndElementHandler = end_element

    p.StartNamespaceDeclHandler = start_namespace

    p.EndNamespaceDeclHandler = end_namespace

    p.CharacterDataHandler = character_data_handler

    p.Parse(xmlstr, 1)

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

    s += '?>'
    return s


def clean(element):
    new_element = copy.copy(element)

    children = Children()

    for child in new_element.children:
        if isinstance(child, Text):
            new_string = Text(child.strip())
            if new_string:
                children.append(new_string)
        elif isinstance(child, Element):
            children.append(clean(child))
    new_element.children = children

    return new_element


def insert_for_pretty(e, indent=4, indent_after_children=0, one_child_dont_do=True):

    new_e = copy.deepcopy(e)

    if one_child_dont_do and len(new_e.children) == 1:
        pass

    elif new_e.children:
        new_children = Children()

        for child in new_e.children:
            new_children.append(Text('\n' + ' ' * indent))

            if isinstance(child, Text):
                new_children.append(child)

            elif isinstance(child, Element):
                new_children.append(insert_for_pretty(child, indent=indent + indent, indent_after_children=indent))

        new_children.append(Text('\n' + ' ' * indent_after_children))

        new_e.children = new_children

    return new_e


IS_NAME_FIXED = 'is_name_fixed'
ATTRIBUTES = 'attributes'
NAME_CHECKFUNC = 'name_checkfunc'
VALUE_CHECKFUNCS = 'value_checkfuncs'
CHILDREN = 'children'
DESCRIPTORS = 'descriptors'


XML_URI = 'http://www.w3.org/XML/1998/namespace'


class Element:
    def __init__(self, name, prefixes=None, attributes=None):
        self.descriptor = None

        self.prefixes = prefixes or Prefixes()
        self.attributes = attributes or Attributes()

        self.name = name

        self.children = Children()

    @property
    def descriptor(self):
        return self.__dict__['descriptor']

    @descriptor.setter
    def descriptor(self, value):
        self.__dict__['descriptor'] = value
        if self.descriptor:
            self.attributes.descriptor = self.descriptor[ATTRIBUTES]
            self.children.descriptor = self.descriptor[CHILDREN]

    @property
    def name(self):
        return self.__dict__['name']

    @name.setter
    def name(self, value):
        if self.descriptor:
            self.descriptor[NAME_CHECKFUNC](value)

        if not isinstance(value, tuple) or len(value) != 2:
            raise Exception

        self.__dict__['name'] = value

    @property
    def attributes(self):
        return self.__dict__['attributes']

    @attributes.setter
    def attributes(self, value):
        self.__dict__['attributes'] = value

    @property
    def children(self):
        return self.__dict__['children']

    @children.setter
    def children(self, value):
        self.__dict__['children'] = value

    def to_string(self, inherited_namespaces=None):

        inherited_prefixes = inherited_namespaces or Prefixes()

        s = ''

        s += '<'

        full_name = ''
        if self.name[0] and self.prefixes[self.name[0]]:
            full_name += self.prefixes[self.name[0]] + ':'
        full_name += self.name[1]

        s += full_name

        for uri, prefix in self.prefixes.items():
            if uri in inherited_prefixes.keys() and inherited_prefixes[uri] == prefix:
                pass

            elif uri == XML_URI:
                pass

            elif uri:
                if prefix:
                    s += ' xmlns:{}="{}"'.format(prefix, uri)
                else:
                    s += ' xmlns="{}"'.format(uri)

        for name, value in self.attributes.items():
            s += ' '

            if name[0]:
                s += self.prefixes[name[0]] + ':'

            s += name[1]
            s += '="{}"'.format(value)

        if self.children:
            s += '>'

            for child in self.children:
                if isinstance(child, Element):
                    inherited_prefixes_for_subs = inherited_prefixes.copy()
                    inherited_prefixes_for_subs.update(self.prefixes)
                    s += child.to_string(inherited_namespaces=inherited_prefixes_for_subs)

                elif isinstance(child, Text):
                    s += child.to_string()

            s += '</{}>'.format(full_name)

        else:
            s += ' />'

        return s


class Prefixes(Dict):
    def __init__(self):
        super().__init__()
        self[XML_URI] = 'xml'

    def __setitem__(self, key, value):
        if key == XML_URI and value != 'xml':
            raise Exception

        super().__setitem__(key, value)


class Attributes(Dict):
    def __init__(self):
        super().__init__()

        self.descriptor = None

    @property
    def descriptor(self):
        return self.__dict__['descriptor']

    @descriptor.setter
    def descriptor(self, value):
        self.__dict__['descriptor'] = value

        for attr_name, value in self.items():
            self[attr_name] = value

    def __setitem__(self, key, value):
        if self.descriptor:
            self.descriptor[NAME_CHECKFUNC](key)
            self.descriptor[VALUE_CHECKFUNCS][key](value)

        super().__setitem__(key, value)


class Children(List):
    def __init__(self):
        super().__init__()
        self.descriptor = None

    @property
    def descriptor(self):
        return self.__dict__['descriptors']

    @descriptor.setter
    def descriptor(self, value):
        self.__dict__['descriptors'] = value

        for item in self:
            if not isinstance(item, Text):
                self.descriptor[NAME_CHECKFUNC](item.name)
                item.descriptor = self.descriptor[DESCRIPTORS][item.name]

    def insert(self, i, item):
        if not isinstance(item, (Element, Text)):
            raise Exception

        if isinstance(item, Element):
            self.descriptor[NAME_CHECKFUNC](item.name)
            item.descriptor = self.descriptor[DESCRIPTORS][item.name]

        super().insert(i, item)


class Text(Str):
    def to_string(self):
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
                s += str(char)
        return s
