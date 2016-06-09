"""Dublin Core Metadata Initiative"""

import time

from abc import abstractmethod

from hooky import Dict

import xl

from ..metadata import Public


def always_true():
    pass


def _w3c_date(string):
    return True


l = [
    'abstract', 'accessRights', 'accrualMethod', 'accrualPeriodicity', 'accrualPolicy', 'alternative', 'audience',
    'available',
    'bibliographicCitation',
    'conformsTo', 'contributor', 'coverage', 'created', 'creator',
    'date', 'dateAccepted', 'dateCopyrighted', 'dateSubmitted', 'description',
    'educationLevel', 'extent',
    'format',
    'hasFormat', 'hasPart', 'hasVersion',
    'identifier', 'instructionalMethod',
    'isFormatOf', 'isPartOf', 'isReferencedBy', 'isReplacedBy', 'isRequiredBy', 'issued', 'isVersionOf',
    'language', 'license',
    'mediator', 'medium', 'modified',
    'provenance', 'publisher',
    'references', 'relation', 'replaces', 'requires', 'rights', 'rightsHolder',
    'source', 'spatial', 'subject',
    'tableOfContents', 'temporal', 'title', 'type',
    'valid'
]


check_funcs = {
    'modified': _w3c_date,
}


check_funcs.update(dict((one, always_true) for one in l if one not in check_funcs.keys()))


_attr_check_funcs = {
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
    'scheme': always_true
}

URI_DC = 'http://purl.org/dc/elements/1.1/'
URI_OPF = 'http://www.idpf.org/2007/opf'

namespace_map = {
    'dc': URI_DC,
    'opf': URI_OPF,
    'xml': xl.URI_XML
}


class _Attrs(Dict):
    def __setitem__(self, key, value):
        if key in ('opf:alt-script', 'dir', 'opf:file-as', 'id', 'scheme', 'xml:lang'):

            if not _attr_check_funcs[key](value):
                raise Exception

            self.data[key] = value

        else:
            raise KeyError


class _Meta(Public):
    def __init__(self, text):
        super().__init__()

        self.text = text
        self._attrs = _Attrs()

    @staticmethod
    def _text_check_func(text):
        pass

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
        e = xl.Element((None, 'meta'))

        e.attributes[(None, 'property')] = 'dcterms:{}'.format(self.__class__.__name__)

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


_classes = {}


for k, v in check_funcs.items():

    _v = staticmethod(v)

    _classes[k] = type(k, (_Meta,), {'_text_check_func': _v})


def get_class(name):
    return _classes[name]
