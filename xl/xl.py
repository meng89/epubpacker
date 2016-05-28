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

        prefixes = Prefixes()

        for _uri, _prefix in ns_list:
            prefixes[_uri] = _prefix

        e = Element(name=(uri, tag), attributes=attributes, prefixes=prefixes)

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

    # p.XmlDeclHandler =

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


def xml_header(version=None, encoding=None, standalone=None):
    s = ''
    s += '<?xml'

    s += " version='{}'".format(version) if version else '1.0'
    s += " encoding='{}'".format(encoding) if encoding else 'utf-8'
    s += " standalone='{}'".format(standalone) if standalone else 'yes'

    s += '?>\n'
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


def clear_space(element):
    pass


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


class XLError(Exception):
    pass


class Element:
    def __init__(self, name, attributes=None, prefixes=None):
        self.name = name
        self.attributes = attributes or Attributes()
        self.prefixes = prefixes or Prefixes()

        self.children = Children()

    @property
    def descriptor(self):
        return self.__dict__['descriptor'] if 'descriptor' in self.__dict__.keys() else None

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
        if not isinstance(value, tuple):
            value = (None, value)

        if len(value) != 2:
            raise ValueError

        if value[0] is not None and not isinstance(value[0], str):
            raise ValueError

        if not isinstance(value[1], str):
            raise ValueError

        if self.descriptor:
            self.descriptor[NAME_CHECKFUNC](value)

        # if value[0] is not None and value[0] not in self.attributes.keys():

        self.__dict__['name'] = value

    @property
    def prefixes(self):
        return self.__dict__['prefixes']

    @prefixes.setter
    def prefixes(self, value):
        self.__dict__['prefixes'] = value

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

    def to_string(self, inherited_prefixes=None):

        inherited_prefixes = inherited_prefixes or Prefixes()

        auto_prefixs = Prefixes()

        def get_prefix(_uri):

            try:
                _prefix = self.prefixes[_uri]
            except KeyError:
                try:
                    _prefix = auto_prefixs[_uri]
                except KeyError:
                    _prefix_num = 0
                    while 'prefix' + str(_prefix_num) in [one for one in self.prefixes.keys()] +\
                                                         [one for one in auto_prefixs.keys()]:
                        _prefix_num += 1

                    _prefix = 'prefix' + str(_prefix_num)

                auto_prefixs[self.name[0]] = _prefix

            return _prefix

        s = ''

        s += '<'

        # processing xml tag
        if self.name[0]:

            prefix = get_prefix(self.name[0])
            if prefix:
                full_name = '{}:{}'.format(prefix, self.name[1])
            else:
                full_name = self.name[1]

        else:
            full_name = self.name[1]

        print(repr(full_name))

        s += full_name

        # processing xml attributes
        if self.attributes:
            s += ' ' + self.attributes.to_string(get_prefix)

        # processing xml namespaces uri prefix
        self_prefixes_and_auto_prefixes = copy.deepcopy(self.prefixes)
        self_prefixes_and_auto_prefixes.update(auto_prefixs)

        prefixes_string = self_prefixes_and_auto_prefixes.to_string(inherited_prefixes)

        print(repr(s))

        if prefixes_string:
            s += ' ' + prefixes_string

        if self.children:
            s += '>'

            prefixes_for_subs = inherited_prefixes.copy()
            prefixes_for_subs.update(self.prefixes)

            for child in self.children:
                if isinstance(child, Element):

                    s += child.to_string(inherited_prefixes=prefixes_for_subs)

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

    def __getitem__(self, uri):
        if uri == XML_URI:
            return 'xml'
        else:
            return super().__getitem__(uri)

    def __setitem__(self, uri, prefix):
        if uri == XML_URI:
            if prefix != 'xml':
                print(uri, prefix)
                raise Exception

        else:
            super().__setitem__(uri, prefix)

    def to_string(self, inherited_prefixes):
        inherited_prefixes = inherited_prefixes or Prefixes()

        string_list = []
        for url, prefix in self.items():
            if url == XML_URI:
                continue

            if url in inherited_prefixes.keys() and prefix == inherited_prefixes[url]:
                continue

            if url:
                if prefix:
                    string_list.append('xmlns:{}="{}"'.format(prefix, url))
                else:
                    string_list.append('xmlns="{}"'.format(url))

        return ' '.join(string_list)


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
        if not isinstance(key, tuple):
            key = (None, key)

        if self.descriptor:
            self.descriptor[NAME_CHECKFUNC](key)
            self.descriptor[VALUE_CHECKFUNCS][key](value)

        if key == (None, 'xmlns'):
            raise AttributeError

        super().__setitem__(key, value)

    def to_string(self, get_prefix_func):
        string_list = []
        for attr_name, attr_value in self.items():

            if attr_name[0]:
                prefix = get_prefix_func(attr_name[0])
                string_list.append('{}:{}="{}"'.format(prefix, attr_name[1], attr_value))

            else:
                string_list.append('{}="{}"'.format(attr_name[1], attr_value))

        return ' '.join(string_list)


class Children(List):
    def __init__(self):
        super().__init__()

    @property
    def descriptor(self):
        return self.__dict__['descriptors'] if 'descriptors' in self.__dict__.keys() else None

    @descriptor.setter
    def descriptor(self, value):
        self.__dict__['descriptors'] = value

        for item in self:
            if not isinstance(item, Text):
                self.descriptor[NAME_CHECKFUNC](item.element_name)
                item.descriptor = self.descriptor[DESCRIPTORS][item.element_name]

    def insert(self, i, item):
        if not isinstance(item, (Element, Text)):
            raise Exception

        if isinstance(item, Element) and self.descriptor:
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
