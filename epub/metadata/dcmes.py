"""
Dublin Core Metadata Element Set
http://dublincore.org/documents/dces/
"""


from abc import abstractmethod

from hooky import Dict

import xl


def always_true(*args, **kwargs):
    return True


check_funcs = {
    # identifier only
    'opf:scheme': always_true,

    'opf:alt-script': always_true,
    'dir': always_true,
    'opf:file-as': always_true,
    'id': always_true,
    'opf:role': always_true,
    'xml:lang': always_true,

    # subject only
    'opf:authority': always_true,

    # Meta only
    'property': always_true,
    'scheme': always_true
}

URI_DC = 'http://purl.org/dc/elements/1.1/'
URI_OPF = 'http://www.idpf.org/2007/opf'

namespace_map = {
    'dc': URI_DC,
    'opf': URI_OPF,
    'xml': xl.URI_XML
}


class _Meta(Dict):

    def __init__(self, text, attrs=None):
        super().__init__()

        self._text = None

        self._text_check_func = always_true

        self._attrs = {}
        self._attrs_check_funcs = check_funcs

        self['text'] = text

        self.update(attrs or {})

    @property
    @abstractmethod
    def element_name(self):
        return None

    @property
    @abstractmethod
    def available_attrs(self):
        return ()

    def __setitem__(self, key, value):
        if key == 'text':
            self._text_check_func(key, value)

            self._text = value
            self._attrs = {}

        elif key in self.available_attrs:

            if not self._attrs_check_funcs[key](value):
                raise Exception

            self._attrs[key] = value

        else:
            raise KeyError

    def to_element(self):

        if ':' in self.element_name:
            prefix, name = self.element_name.split(':')
            uri = namespace_map[prefix]
            e = xl.Element(name=(uri, name), prefixes={uri: prefix})

        else:
            e = xl.Element((None, self.element_name))

        for attr_name, value in self._attrs.items():

            uri = None
            if ':' in attr_name:
                prefix, attr = attr_name.split(':')
                uri = namespace_map[prefix]
                e.prefixes[uri] = prefix

            else:
                attr = attr_name

            e.attributes[(uri, attr)] = value

        return e


class Identifier(_Meta):
    @property
    def element_name(self):
        return 'dc:identifier'

    @property
    def available_attrs(self):
        return 'id', 'opf:scheme'


class Title(_Meta):
    @property
    def element_name(self):
        return 'dc:title'

    @property
    def available_attrs(self):
        return 'opf:alt-script', 'dir', 'opf:file-as', 'id', 'xml:lang'


class Language(_Meta):
    @property
    def element_name(self):
        return 'dc:language'

    @property
    def available_attrs(self):
        return 'id',


class Contributor(_Meta):
    @property
    def element_name(self):
        return 'dc:contributor'

    @property
    def available_attrs(self):
        return 'opf:alt-script', 'dir', 'opf:file-as', 'id', 'opf:role', 'xml:lang'


class Coverage(_Meta):
    @property
    def element_name(self):
        return 'dc:coverage'

    @property
    def available_attrs(self):
        return 'dir', 'xml:lang'


class Creator(_Meta):
    @property
    def element_name(self):
        return 'dc:creator'

    @property
    def available_attrs(self):
        return 'opf:alt-script', 'dir', 'opf:file-as', 'id', 'opf:role', 'xml:lang'


class Date(_Meta):
    @property
    def element_name(self):
        return 'dc:date'

    @property
    def available_attrs(self):
        return 'id',


class Description(_Meta):
    @property
    def element_name(self):
        return 'dc:discription'

    @property
    def available_attrs(self):
        return 'dir', 'id', 'xml:lang'


class Format(_Meta):
    @property
    def element_name(self):
        return 'dc:format'

    @property
    def available_attrs(self):
        return 'id',


class Publisher(_Meta):
    @property
    def element_name(self):
        return 'dc:publisher'

    @property
    def available_attrs(self):
        return 'opf:alt-script', 'dir', 'opf:file-as', 'id', 'xml:lang'


class Relation(_Meta):
    @property
    def element_name(self):
        return 'dc:relation'

    @property
    def available_attrs(self):
        return 'dir', 'id', 'xml:lang'


class Rights(_Meta):
    @property
    def element_name(self):
        return 'dc:rights'

    @property
    def available_attrs(self):
        return 'dir', 'id', 'xml:lang'


class Source(_Meta):
    @property
    def element_name(self):
        return 'dc:source'

    @property
    def available_attrs(self):
        return 'id',


class Subject(_Meta):
    @property
    def element_name(self):
        return 'dc:subject'

    @property
    def available_attrs(self):
        return 'dir', 'id', 'xml:lang', 'opf:authority'


class Type(_Meta):
    @property
    def element_name(self):
        return 'dc:type'

    @property
    def available_attrs(self):
        return 'id',
