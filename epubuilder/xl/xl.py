from abc import abstractmethod

import copy

from hooky import List, Dict

from collections import UserString

import xml.parsers.expat


class HandlerError(Exception):
    pass


def parse(xmlstr, debug=False):
    """
    parse xml string to Xl object

    :param xmlstr:
    :type xmlstr: str
    :param debug:
    :type debug: bool
    :return:
    :rtype: Xl
    """

    xl = Xl()

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

        e = Element(tag=(uri, tag), attributes=attributes, prefixes=prefixes)

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

    def start_doc_type_decl(doc_type_name, system_id, public_id, has_internal_subset):
        xl.doc_type = DocType(doc_type_name=doc_type_name, system_id=system_id, public_id=public_id)

        if has_internal_subset == 1:
            raise HandlerError('Has internal subset, cannot handler it!')

    def decl_handler(version, encoding, standalone):
        xl.header = Header(version=version, encoding=encoding, standalone=standalone)

    p = xml.parsers.expat.ParserCreate(namespace_separator=' ')

    p.XmlDeclHandler = decl_handler

    p.StartDoctypeDeclHandler = start_doc_type_decl

    # internal dtd
    # p.EntityDeclHandler = entity_decl_handler

    p.StartElementHandler = start_element

    p.EndElementHandler = end_element

    p.StartNamespaceDeclHandler = start_namespace

    p.EndNamespaceDeclHandler = end_namespace

    p.CharacterDataHandler = character_data_handler

    p.Parse(xmlstr, 1)

    xl.root = element

    return xl


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
    if not isinstance(element, Element):
        raise TypeError

    new_element = Element(tag=copy.deepcopy(element.tag),
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

    new_element = Element(tag=copy.deepcopy(element.tag),
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


URI_XML = 'http://www.w3.org/XML/1998/namespace'


class XLError(Exception):
    pass


class Xl:
    def __init__(self, header=None, doc_type=None, root=None):
        self.header = header or Header()
        self.doc_type = doc_type
        self.root = root or Element()

    def string(self, ):
        s = ''

        s += self.header.string()

        if self.doc_type:
            s += '\n' + self.doc_type.string()

        s += '\n' + self.root.string()

        return s


class Node:
    @abstractmethod
    def string(self):
        pass


class Header(Node):
    def __init__(self, version=None, encoding=None, standalone=None):
        self.version = version
        self.encoding = encoding
        self.standalone = standalone

    def string(self):
        s = ''
        s += '<?xml'

        if self.version:
            s += " version='{}'".format(self.version)  # 1.0

        if self.encoding:
            s += " encoding='{}'".format(self.encoding)  # utf-8

        if self.standalone is not None:
            s += " standalone='{}'".format(self.standalone)  # yes

        s += '?>\n'
        return s


class DocType(Node):
    def __init__(self, doc_type_name=None, system_id=None, public_id=None):
        self.doc_type_name = doc_type_name
        self.system_id = system_id
        self.public_id = public_id

    def string(self):
        s = ''
        s += '<!DOCTYPE'

        s += ' {}'.format(self.doc_type_name)
        s += ' "{}"'.format(self.public_id)
        s += ' "{}"'.format(self.system_id)

        s += '>'

        return s


class Element(Node):
    """
    XML element node.
    """
    def __init__(self, tag=None, attributes=None, prefixes=None):
        """
        :param tag:
        :type tag: tuple or str
        :param attributes:
        :type attributes: Attributes or dict
        :param prefixes:
        :type prefixes: Prefixes or dict
        """
        self.tag = tag

        self.attributes = Attributes(attributes) if attributes else Attributes()

        self.prefixes = Prefixes(prefixes) if prefixes else Prefixes()

        self.children = Children()

    @property
    def tag(self):
        return self.__dict__['tag']

    @tag.setter
    def tag(self, value):
        if not isinstance(value, tuple):
            value = (None, value)

        if len(value) != 2:
            raise ValueError

        if value[0] is not None and not isinstance(value[0], str):
            raise ValueError

        self.__dict__['tag'] = value

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
        if self.tag[1] is None:
            raise TypeError

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
        if self.tag[0] is not None:
            try:
                prefix = get_prefix(self.tag[0])
            except ValueError:
                prefix = make_a_auto_prefix(self.tag[0])

            if prefix is not None:
                full_name = '{}:{}'.format(prefix, self.tag[1])
            else:
                full_name = self.tag[1]
        else:
            full_name = self.tag[1]

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

        if attributes:
            self.update(attributes)

    def __setitem__(self, key, value):
        if not isinstance(key, tuple):
            key = (None, key)

        if key == (None, 'xmlns'):
            raise AttributeError

        super().__setitem__(key, value)


class Children(List):
    def __init__(self):
        super().__init__()

    def _before_add(self, key=None, item=None):
        if not isinstance(item, Node):
            raise TypeError('{} is not legal'.format(item.__class__.__name__))


class Text(Node, UserString):
    """
    XML text node
    """
    def __init__(self, string):
        """
        :param string:
        :type string: str
        """
        super().__init__(string)

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
