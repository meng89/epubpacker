"""
Dublin Core Metadata Element Set, see http://dublincore.org/documents/dces/

All classes in this module
"""

import uuid

from epubuilder.xl import Element, Text, URI_XML

from .attrs import Id, Scheme, AltScript, Dir, FileAs, Role, Lang, Authority, Attrs
from .base import Base

URI_DC = 'http://purl.org/dc/elements/1.1/'
URI_OPF = 'http://www.idpf.org/2007/opf'

namespace_map = {
    'opf': URI_OPF,
    'xml': URI_XML
}


class _Base(Base, Attrs):
    """the name"""
    def __init__(self, text):
        Base.__init__(self)
        Attrs.__init__(self)

        self._text = text

    @property
    def text(self):
        return self._text

    def to_element(self):
        e = Element((URI_DC, self.__class__.__name__.lower()))
        e.prefixes[URI_DC] = 'dc'

        for attr_name, value in self._attrs.items():

            if ':' in attr_name:
                prefix, attr = attr_name.split(':')
                uri = namespace_map[prefix]
                e.prefixes[uri] = prefix

                e.attributes[(uri, attr)] = value

            else:
                attr = attr_name

                e.attributes[(None, attr)] = value

        e.children.append(Text(self._text))

        return e


##########################################################################

class Identifier(_Base, Id, Scheme):
    """identifier"""
    def __init__(self, text):
        super().__init__(text)
        self.id = 'id_' + uuid.uuid4().hex


class Title(_Base, AltScript, Dir, FileAs, Id, Lang):
    """title of Book"""


class Language(_Base, Id):
    """https://tools.ietf.org/html/rfc5646

    example: en-US
    """


class Contributor(_Base, AltScript, Dir, FileAs, Id, Role, Lang):
    """contributor"""


class Coverage(_Base, Dir, Lang):
    """coverage"""


class Creator(_Base, AltScript, Dir, FileAs, Id, Role, Lang):
    """creator"""


class Date(_Base, Id):
    """date"""


class Description(_Base, Dir, Id, Lang):
    """description"""


class Format(_Base, Id):
    """format"""


class Publisher(_Base, AltScript, Dir, FileAs, Id, Lang):
    """publisher"""


class Relation(_Base, Dir, Id, Lang):
    """relation"""


class Rights(_Base, Dir, Id, Lang):
    """rights"""


class Source(_Base, Id):
    """source"""


class Subject(_Base, Dir, Id, Lang, Authority):
    """subject"""


class Type(_Base, Id):
    """type"""