from abc import abstractmethod

import copy

from hooky import List, Dict

from collections import UserString

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
        print('Character html: "{}"'.format(data)) if debug else None
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

    # p.StartDoctypeDeclHandler

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

    s += " version='{}'".format(version if version else '1.0')
    s += " encoding='{}'".format(encoding if encoding else 'utf-8')
    s += " standalone='{}'".format(standalone if standalone else 'yes')

    s += '?>\n'
    return s


def clear_spaces(element):

    new_element = Element(name=copy.deepcopy(element.name),
                          attributes=copy.deepcopy(element.attributes),
                          prefixes=copy.deepcopy(element.prefixes))

    for child in element.children:
        if isinstance(child, Text):
            new_text = Text(child.strip())

            if new_text:
                new_element.children.append(new_text)

        elif isinstance(child, Element):
            new_element.children.append(clear_spaces(child))

    return new_element


def _is_straight_line(element):
    if len(element.children) == 0:
        return True

    if len(element.children) == 1:
        if isinstance(element.children[0], Element):
            return _is_straight_line(element.children[0])
        else:
            return True

    elif len(element.children) > 1:
        return False


def pretty_insert(element, start_indent=0, step=4, dont_do_when_one_child=True):

    new_element = Element(name=copy.deepcopy(element.name),
                          attributes=copy.deepcopy(element.attributes),
                          prefixes=copy.deepcopy(element.prefixes))

    _indent_text = Text('\n' + ' ' * (start_indent + step))

    if _is_straight_line(element) and dont_do_when_one_child:
        new_element.children = copy.deepcopy(element.children)

    elif element.children:
        for child in element.children:

            if isinstance(child, Text):
                new_text = _indent_text + copy.deepcopy(child)

                new_element.children.append(new_text)

            elif isinstance(child, Element):
                new_element.children.append(_indent_text)

                new_element.children.append(pretty_insert(element=child,
                                                          start_indent=start_indent + step,
                                                          step=step,
                                                          dont_do_when_one_child=dont_do_when_one_child,
                                                          ))

        new_element.children.append(Text('\n' + ' ' * start_indent))

    return new_element


IS_NAME_FIXED = 'is_name_fixed'
ATTRIBUTES = 'attributes'
NAME_CHECKFUNC = 'name_checkfunc'
VALUE_CHECKFUNCS = 'value_checkfuncs'
CHILDREN = 'children'
DESCRIPTORS = 'descriptors'


URI_XML = 'http://www.w3.org/XML/1998/namespace'


class XLError(Exception):
    pass


class Node:
    @abstractmethod
    def string(self):
        pass


class Element(Node):
    def __init__(self, name, attributes=None, prefixes=None):
        self.name = name

        self.attributes = Attributes(attributes) if attributes else Attributes()

        self.prefixes = Prefixes(prefixes) if prefixes else Prefixes()

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

    def string(self, inherited_prefixes=None):

        inherited_prefixes = inherited_prefixes or Prefixes()

        auto_prefixs = Prefixes()

        def make_a_auto_prefix(_uri):
            _prefix_num = 0
            while 'prefix' + str(_prefix_num) in \
                    [one for one in self.prefixes.values()] + \
                    [one for one in inherited_prefixes.values()] + \
                    [one for one in auto_prefixs.values()]:

                _prefix_num += 1

            _prefix = 'prefix' + str(_prefix_num)
            auto_prefixs[_uri] = _prefix

            return _prefix

        def get_prefix(_uri):

            if _uri in self.prefixes.keys():
                _prefix = self.prefixes[_uri]

            elif _uri in inherited_prefixes.keys():
                _prefix = inherited_prefixes[_uri]

            elif _uri in auto_prefixs.keys():
                _prefix = auto_prefixs[_uri]

            else:
                raise ValueError

            return _prefix

        s = '<'

        ################################################################################################################
        # processing xml tag
        if self.name[0] is not None:
            try:
                prefix = get_prefix(self.name[0])
            except ValueError:
                prefix = make_a_auto_prefix(self.name[0])

            if prefix is not None:
                full_name = '{}:{}'.format(prefix, self.name[1])
            else:
                full_name = self.name[1]
        else:
            full_name = self.name[1]

        s += full_name

        ################################################################################################################
        # processing xml attributes
        _attrs_string_list = []
        for attr_name, attr_value in self.attributes.items():

            if attr_name[0] is not None:
                try:
                    prefix = get_prefix(attr_name[0])
                except ValueError:
                    prefix = make_a_auto_prefix(attr_name[0])
                _attrs_string_list.append('{}:{}="{}"'.format(prefix, attr_name[1], attr_value))

            else:
                _attrs_string_list.append('{}="{}"'.format(attr_name[1], attr_value))

        if _attrs_string_list:
            s += ' '
            s += ' '.join(_attrs_string_list)

        ################################################################################################################
        # processing xml prefixes
        _prefix_string_list = []
        for url, prefix in self.prefixes.items():
            if url == URI_XML:
                continue

            if url in inherited_prefixes.keys() and prefix == inherited_prefixes[url]:
                continue

            if url:
                if prefix:
                    _prefix_string_list.append('xmlns:{}="{}"'.format(prefix, url))
                else:
                    _prefix_string_list.append('xmlns="{}"'.format(url))

        if _prefix_string_list:
            s += ' '
            s += ' '.join(_prefix_string_list)

        ################################################################################################################
        # processing children
        if self.children:
            s += '>'

            prefixes_for_subs = inherited_prefixes.copy()
            prefixes_for_subs.update(self.prefixes)
            prefixes_for_subs.update(auto_prefixs)

            for child in self.children:
                if isinstance(child, Element):
                    s += child.string(inherited_prefixes=prefixes_for_subs)

                elif isinstance(child, Text):
                    s += child.string()

            s += '</{}>'.format(full_name)

        else:
            s += ' />'

        return s


class Prefixes(Dict):
    def _before_add(self, key=None, item=None):
        if key == URI_XML and item != 'xml':
            raise ValueError

    def __init__(self, prefixes=None):
        super().__init__()

        self[URI_XML] = 'xml'

        if prefixes:
            self.update(prefixes)


class Attributes(Dict):
    def __init__(self, attributes=None):
        super().__init__()

        self.descriptor = None

        if attributes:
            self.update(attributes)

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


class Children(List):
    def _before_add(self, key=None, item=None):
        if not isinstance(item, Node):
            raise TypeError('{} is not legal'.format(item.__class__.__name__))

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
        if isinstance(item, Element) and self.descriptor:
            self.descriptor[NAME_CHECKFUNC](item.name)
            item.descriptor = self.descriptor[DESCRIPTORS][item.name]

        super().insert(i, item)


class Text(Node, UserString):
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
                s += str(char)
        return s
