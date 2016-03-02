from epubuilder.xl import Element

from ._ import _Id, _Text, _XmlLang, _Dir, _FileAs, _Property, _Scheme, \
    _Href, _Rel, _MediaType, _Properties


class Metadata(object):
    def __init__(self):
        pass


####################
# start Dublin Core Metadata Elements

##########
# start Required child of metadata. Repeatable.

class DcIdentifier(_Id, _Text):
    """dc:identifier, child of Metadata
    """
    def __init__(self, element=None):
        super().__init__(element or Element('dc:identifier'))


class DcTitle(_Id, _XmlLang, _Dir, _FileAs, _Text):
    def __init__(self, element=None):
        super().__init__(element or Element('dc:title'))


class DcLanguage(_Id, _Text):
    def __init__(self, element=None):
        super().__init__(element or Element('dc:language'))

# end Required child of metadata. Repeatable.
##########


##########
# start Optional child of metadata.

class DcCreator(_Id, _XmlLang, _Dir, _FileAs, _Text):
    def __init__(self, element=None):
        super().__init__(element or Element('dc:creator'))


class DcType(_Id, _Text):
    def __init__(self, element=None):
        super().__init__(element or Element('dc:type'))

# up is Repeatable. down is not


class DcPublisher(_Id, _XmlLang, _Dir, _FileAs, _Text):
    def __init__(self, element=None):
        super().__init__(element or Element('dc:publisher'))

# end Optional child of metadata.
##########

# end Dublin Core Metadata Elements
####################


class Meta(_Property, _Id, _Scheme, _XmlLang, _Dir, _Text):
    def __init__(self, element=None):
        super().__init__(element or Element('meta'))


class Link(_Href, _Rel, _Id, _MediaType, _Properties):
    def __init__(self, element=None):
        super().__init__(element or Element('link'))
