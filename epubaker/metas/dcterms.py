# coding=utf-8

"""Dublin Core Metadata Initiative, see http://dublincore.org/documents/dcmi-terms/"""

from epubaker.metas.attrs import Attrs, AltScript, Dir, FileAs, Id, Role, Lang
from epubaker.xl import Element, URI_XML


def always_true(*args, **kwargs):
    pass

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
    'modified': always_true,
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
    'xml': URI_XML
}


class _Base(Attrs):
    def __init__(self, text):
        check_funcs[self.__class__.__name__](text)
        Attrs.__init__(self)

        self._text = text

    @property
    def text(self):
        return self._text

    def to_element(self):
        e = Element((None, 'meta'))

        e.attributes[(None, 'property')] = 'dcterms:{}'.format(self.__class__.__name__)

        for attr_name, value in self._attrs.items():

            uri = None
            if ':' in attr_name:
                prefix, attr = attr_name.split(':')
                uri = namespace_map[prefix]
                e.prefixes[uri] = prefix

            else:
                attr = attr_name

            e.attributes[(uri, attr)] = value

        e.children.append(self.text)

        return e


_classes = {}

for k, v in check_funcs.items():

    _classes[k] = type(k, (_Base, AltScript, Dir, FileAs, Id, Role, Lang), {})


def get_dcterm(name):
    """get a term class by term name"""
    return _classes[name]

