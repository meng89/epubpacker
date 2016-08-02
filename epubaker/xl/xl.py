# coding=utf-8

from __future__ import print_function

from abc import abstractmethod

import copy

from hooky import List, Dict

import xml.parsers.expat


class HandlerError(Exception):
    pass


def parse(xmlstr, debug=False):
    """
    parse XML string to Xl object

    :param xmlstr:
    :type xmlstr: str
    :param debug:
    :type debug: bool
    :return: object of :class:`Xl`
    :rtype: Xl
    """

    xl = Xl()

    out_element = [None]

    elements = []

    ns_list = []

    s = ['']

    def start_element(name, attrs):
        _do_string()

        print('start_element', name) if debug else None

        attributes = {}

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

        prefixes = {}

        for _uri, _prefix in ns_list:

            prefixes[_uri] = _prefix

        e = Element(tag=(uri, tag), attributes=attributes, prefixes=prefixes)

        if elements:
            elements[-1].children.append(e)

        elements.append(e)

        # nonlocal out_element
        if not out_element[0]:
            out_element[0] = e

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
        # nonlocal s
        s[0] += data

    def _do_string():
        # nonlocal s
        if s[0] and elements:
            string = s[0]
            elements[-1].children.append(string)
            s[0] = ''

    def start_doc_type_decl(doc_type_name, system_id, public_id, has_internal_subset):
        xl.doc_type = DocType(doc_type_name=doc_type_name, system_id=system_id, public_id=public_id)

        if has_internal_subset == 1:
            raise HandlerError('Has internal subset, cannot handler it!')

    def decl_handler(version, encoding, standalone):
        standalone_ = None

        if standalone == 1:
            standalone_ = True
        elif standalone == 0:
            standalone_ = False
        elif standalone == -1:
            standalone_ = None

        xl.header = Header(version=version, encoding=encoding, standalone=standalone_)

    p = xml.parsers.expat.ParserCreate(namespace_separator=' ', encoding='UTF=8')

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

    xl.root = out_element[0]

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


def clean_whitespaces(element):
    """
    :param element:
    :return: A copy of the element, all whitespace characters have been stripped from the beginning and the end of the
     text node in the children and children's children and so on. delete the text node If it is empty.
    """
    if not isinstance(element, Element):
        raise TypeError

    new_element = Element(tag=copy.deepcopy(element.tag),
                          attributes=copy.deepcopy(element.attributes),
                          prefixes=copy.deepcopy(element.prefixes))

    for child in element.children:
        if isinstance(child, str):
            new_text = child.strip()

            if new_text:
                new_element.children.append(new_text)

        elif isinstance(child, Element):
            new_element.children.append(clean_whitespaces(child))

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
    """
    Modify the copy of the element, to make it looks more pretty and clear.

    :param element:
    :type element: Element
    :param start_indent:
    :type start_indent: int
    :param step:
    :type step: int
    :param dont_do_when_one_child:
    :type dont_do_when_one_child: bool
    :return: object of :class:`Element`
    """

    new_element = Element(tag=copy.deepcopy(element.tag),
                          attributes=copy.deepcopy(element.attributes),
                          prefixes=copy.deepcopy(element.prefixes))

    _indent_text = '\n' + ' ' * (start_indent + step)

    if _is_straight_line(element) and dont_do_when_one_child:
        new_element.children = copy.deepcopy(element.children)

    elif element.children:
        for child in element.children:

            if isinstance(child, str):
                new_text = _indent_text + child

                new_element.children.append(new_text)

            elif isinstance(child, Element):
                new_element.children.append(_indent_text)

                new_element.children.append(pretty_insert(element=child,
                                                          start_indent=start_indent + step,
                                                          step=step,
                                                          dont_do_when_one_child=dont_do_when_one_child,
                                                          ))

        new_element.children.append('\n' + ' ' * start_indent)

    return new_element


URI_XML = 'http://www.w3.org/XML/1998/namespace'


class XLError(Exception):
    pass


class Xl(object):
    def __init__(self, header=None, doc_type=None, root=None):
        """
        :param header:
        :type header: Header
        :param doc_type:
        :type doc_type: DocType
        :param root:
        :type root: Element
        """

        self.header = header or header
        """object of :class:`Header`"""

        self.doc_type = doc_type
        """object of :class:`DocType`"""

        self.root = root
        """object of :class:`Element`"""

    def string(self):
        """To xml string"""
        s = ''

        if self.header:
            s += self.header.string() + '\n'

        if self.doc_type:
            s += self.doc_type.string() + '\n'

        s += self.root.string()

        return s


class _Node(object):
    @abstractmethod
    def string(self):
        pass


class Header(_Node):
    """
    Handle XML header node
    """
    def __init__(self, version=None, encoding=None, standalone=None):
        """

        :param version:
        :type version: str
        :param encoding:
        :type encoding: str
        :param standalone:
        :type standalone: bool
        """
        self.version = version or '1.0'
        self.encoding = encoding or 'utf-8'
        self.standalone = standalone

    def string(self):
        if not (self.version or self.encoding or self.standalone):
            return ''

        s = ''

        s += '<?xml'

        if self.version:
            s += ' version="{}"'.format(self.version)

        if self.encoding:
            s += ' encoding="{}"'.format(self.encoding)

        if self.standalone is not None:
            s += ' standalone="{}"'.format('yes' if self.standalone else 'no')

        s += ' ?>'

        return s


class DocType(_Node):
    """
    Handle XML doc type node
    """
    def __init__(self, doc_type_name, system_id, public_id):
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


class Element(_Node):
    """
    Handle XML element node.
    """
    def __init__(self, tag=None, attributes=None, prefixes=None):
        _Node.__init__(self)
        """
        :param tag:
        :type tag: tuple or str
        :param attributes:
        :type attributes: _Attributes or dict
        :param prefixes:
        :type prefixes: _Prefixes or dict
        """

        self._tag = None

        self.tag = tag
        """tuple object of length 2.

        First in the tuple is the url of the namespaces,
        the second is the xml element tag you know ordinarily.
        """

        self._attributes = _Attributes(attributes) if attributes else _Attributes()
        """dict-like.

        Store xml attribute names and values in *keys* and *values*

        """

        self._prefixes = _Prefixes(prefixes) if prefixes else _Prefixes()
        """dict-like.

        Store xml namespaces urls and prefixes in *keys* and *values*

        Ignore this is fine, because you will get automatic prefixes for the namespaces.
        """

        self._children = _Children()
        """list-like.

        Store children Node"""

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        if not isinstance(value, tuple):
            value = (None, value)

        if len(value) != 2:
            raise ValueError

        if value[0] is not None:
            if isinstance(value[0], str):
                pass
            elif isinstance(value[0], unicode):
                pass
            else:
                raise ValueError

        if isinstance(value[1], str):
            pass
        elif isinstance(value[1], unicode):
            pass
        else:
            raise ValueError

        self._tag = value

    @property
    def prefixes(self):
        return self._prefixes

    @prefixes.setter
    def prefixes(self, value):
        self._prefixes = value

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, value):
        self._attributes = value

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = value
        self.__dict__['children'] = value

    def string(self, inherited_prefixes=None):
        """to string, you may want to see :class:`Xl.string`"""
        if self.tag[1] is None:
            raise TypeError

        inherited_prefixes = inherited_prefixes or _Prefixes()

        auto_prefixs = _Prefixes()

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

                # elif isinstance(child, Text):
                #    s += child.string()

                elif isinstance(child, str):
                    s += _escape(child)

            s += '</{}>'.format(full_name)

        else:
            s += ' />'

        return s


class _Prefixes(Dict):
    def _before_add(self, key=None, item=None):
        if key == URI_XML and item != 'xml':
            raise ValueError

        if item in self.values() and (key not in self.keys() or item != self[key]):
            raise ValueError

    def __init__(self, prefixes=None):
        Dict.__init__(self)

        self[URI_XML] = 'xml'

        if prefixes:
            self.update(prefixes)


class _Attributes(Dict):
    def __init__(self, attributes=None):
        Dict.__init__(self)

        if attributes:
            self.update(attributes)

    def __setitem__(self, key, value):
        if not isinstance(key, tuple):
            key = (None, key)

        if key[0] is not None:
            if isinstance(key[0], str):
                pass

            elif isinstance(key[0], unicode):
                pass

            else:
                raise KeyError

        if isinstance(key[1], str):
            pass

        elif isinstance(key[1], unicode):
            pass

        else:
            raise KeyError

        if key == (None, 'xmlns'):
            raise AttributeError

        Dict.__setitem__(self, key, value)


class _Children(List):
    def __init__(self):
        List.__init__(self)

    def _before_add(self, key=None, item=None):
        if isinstance(item, (_Node, str)):
            pass

        elif isinstance(item, unicode):
            pass

        else:
            raise TypeError('{} is not legal'.format(item.__class__.__name__))


def _escape(string):
    """

    :param string:
     :type string: str
    :return:
     :rtype: str
    """
    s = ''
    for char in string:
        if char == '&':
            s += '&amp;'
        elif char == '<':
            s += '&lt;'
        elif char == '>':
            s += '&gt;'
        else:
            s += str(char)
    return s
