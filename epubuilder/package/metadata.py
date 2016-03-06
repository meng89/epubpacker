from epubuilder.xl import Element

from ._ import _Id, _Text, _XmlLang, _Dir, _FileAs, _Property, _Scheme, \
    _Href, _Rel, _MediaType, _Properties


def element_name_checkfunc(legal_name):
    def checkfunc(name):
        if name != legal_name:
            raise Exception
    return checkfunc


def attributes_name_checkfunc(legal_names):
    def checkfunc(name):
        if name not in legal_names:
            raise Exception
    return checkfunc


def children_name_checkfunc(legal_names):
    def checkfunc(name):
        if name not in legal_names:
            raise Exception
    return checkfunc


IS_NAME_FIXED = 'is_name_fixed'
ATTRIBUTES = 'attributes'
NAME_CHECKFUNC = 'name_checkfunc'
VALUE_CHECKFUNCS = 'value_checkfuncs'
CHILDREN = 'children'
DESCRIPTORS = 'descriptors'

class Metadata(object):
    def __init__(self):
        pass


_metadata_children_des = {
    'title': title_des,
    'identifier': dc_identifier_des,
    'language': language_des
    'creator': creator_des,
}

metadata_des = {
    IS_NAME_FIXED: True,

    ATTRIBUTES: {
        NAME_CHECKFUNC: attributes_name_checkfunc([])
    },

    CHILDREN: {
        NAME_CHECKFUNC: children_name_checkfunc(['title',
                                                 'creator',
                                                 'identifier'])
    }


}
####################
# start Dublin Core Metadata Elements

##########
# start Required child of metadata. Repeatable.



class DcIdentifier(_Id, _Text):
    """dc:identifier, child of Metadata
    """
    def __init__(self, element=None):
        super().__init__(element or Element('dc:identifier'))


_identifier_des = {
    IS_NAME_FIXED: True,
    ATTRIBUTES: {
        NAME_CHECKFUNC: attributes_name_checkfunc(['id']),
        VALUE_CHECKFUNCS: {
            'id': attr_value_checkfunc,
        },
    },

    CHILDREN: {
        NAME_CHECKFUNC: children_name_checkfunc([]),
    },
}


class DcTitle(_Id, _XmlLang, _Dir, _FileAs, _Text):
    def __init__(self, element=None):
        super().__init__(element or Element('dc:title'))

_title_des = {
    IS_NAME_FIXED: True,
    ATTRIBUTES:{
        NAME_CHECKFUNC: attributes_name_checkfunc(['id', 'xmllang', 'dir', 'file-as']),
        VALUE_CHECKFUNCS: {}
    }
}


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
