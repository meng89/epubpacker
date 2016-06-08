"""
Dublin Core Metadata Element Set
http://dublincore.org/documents/dces/
"""


from abc import abstractmethod

from hooky import Dict

from .metadata import Public

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
    'opf': URI_OPF,
    'xml': xl.URI_XML
}


class Attrs(Dict):

    def __init__(self, available_attrs, attr_check_funcs):
        super().__init__()
        self._available_attrs = available_attrs
        self._attr_check_funcs = attr_check_funcs

    def __setitem__(self, key, value):
        if key not in self._available_attrs:
            raise KeyError

        if not self._attr_check_funcs[key](value):
            raise ValueError

        super().__setitem__(key, value)


class _Meta(Public):
    _text_check_func = always_true

    available_attrs = ()
    _attrs_check_funcs = check_funcs

    def __init__(self, text):
        super().__init__()

        self._attrs = Attrs(available_attrs=self.available_attrs, attr_check_funcs=self._attrs_check_funcs)

        self.text = text

    @property
    def text(self):
        return self.__dict__['text']

    @text.setter
    def text(self, value):
        if self._text_check_func(value):
            self.__dict__['text'] = value
        else:
            raise Exception

    @property
    def attrs(self):
        return self._attrs

    def as_element(self):
        e = xl.Element((URI_DC, self.__class__.__name__.lower()))
        e.prefixes[URI_DC] = 'dc'

        for attr_name, value in self.attrs.items():

            uri = None
            if ':' in attr_name:
                prefix, attr = attr_name.split(':')
                uri = namespace_map[prefix]
                e.prefixes[uri] = prefix

            else:
                attr = attr_name

            e.attributes[(uri, attr)] = value

        e.children.append(xl.Text(self.text))

        return e


class Identifier(_Meta):
    available_attrs = 'id', 'opf:scheme'


class Title(_Meta):
    available_attrs = 'opf:alt-script', 'dir', 'opf:file-as', 'id', 'xml:lang'


class Language(_Meta):
    available_attrs = 'id',


class Contributor(_Meta):
    available_attrs = 'opf:alt-script', 'dir', 'opf:file-as', 'id', 'opf:role', 'xml:lang'


class Coverage(_Meta):
    available_attrs = 'dir', 'xml:lang'


class Creator(_Meta):
    available_attrs = 'opf:alt-script', 'dir', 'opf:file-as', 'id', 'opf:role', 'xml:lang'


class Date(_Meta):
    available_attrs = 'id',


class Description(_Meta):
    available_attrs = 'dir', 'id', 'xml:lang'


class Format(_Meta):
    available_attrs = 'id',


class Publisher(_Meta):
    available_attrs = 'opf:alt-script', 'dir', 'opf:file-as', 'id', 'xml:lang'


class Relation(_Meta):
    available_attrs = 'dir', 'id', 'xml:lang'


class Rights(_Meta):
    available_attrs = 'dir', 'id', 'xml:lang'


class Source(_Meta):
    available_attrs = 'id',


class Subject(_Meta):
    available_attrs = 'dir', 'id', 'xml:lang', 'opf:authority'


class Type(_Meta):
    available_attrs = 'id',
