from .xl import IS_NAME_FIXED, ATTRIBUTES, NAME_CHECKFUNC, VALUE_CHECKFUNCS, CHILDREN, DESCRIPTORS
from .xl import URI_XML


def value_checkfunc(legal_values):
    def checkfunc(value):
        if value not in legal_values:
            raise Exception
    return checkfunc


def pass_func(value, *args, **kwargs):
    pass

id_func = pass_func


# package/spine/itemref

itemref_descriptors = {
    # required
    (None, 'idref'): pass_func,
    # optional
    # yes 线性阅读，应该是不实用目录是翻页可以翻到。
    # no 是翻页翻不到，但是可以通过目录打开
    (None, 'linear'): value_checkfunc(('yes', 'no')),


    (None, 'id'): id_func,
    (None, 'properties'): pass_func,
}

itemref_descriptor = {
    IS_NAME_FIXED: True,
    ATTRIBUTES: {
        NAME_CHECKFUNC: value_checkfunc(itemref_descriptors.keys()),
        VALUE_CHECKFUNCS: itemref_descriptors,
    },

    CHILDREN: {
        NAME_CHECKFUNC: value_checkfunc(()),
    },
}

# package/spine

spine_attributes_descriptors = {
    (None, 'id'): id_func
}

spine_children_descriptors = {
    (None, 'itemref'): itemref_descriptor  # >= 1
}

spine_descriptor = {
    IS_NAME_FIXED: True,
    ATTRIBUTES: {
        NAME_CHECKFUNC: value_checkfunc(spine_attributes_descriptors.keys()),
        VALUE_CHECKFUNCS: spine_attributes_descriptors,
    },

    CHILDREN: {
        NAME_CHECKFUNC: value_checkfunc(spine_children_descriptors.keys()),
    },
}

# package/manifest/item

item_descriptors = {
    # required
    (None, 'id'): id_func,
    (None, 'href'): pass_func,
    (None, 'media-type'): pass_func,
    # conditionally required
    (None, 'fallback'): pass_func,
    (None, 'duration'): pass_func,
    # optional
    (None, 'properties'): pass_func,
    (None, 'media-overlay'): pass_func
}

item_descriptor = {
    IS_NAME_FIXED: True,
    ATTRIBUTES: {
        NAME_CHECKFUNC: value_checkfunc(item_descriptors.keys()),
        VALUE_CHECKFUNCS: item_descriptors,
    },

    CHILDREN: {
        NAME_CHECKFUNC: value_checkfunc(()),
    },
}


# package/manifest

manifest_attributes_descriptors = {
    (None, 'id'): id_func
}

manifest_children_descriptors = {
    (None, 'item'): item_descriptor  # >= 1
}

manifest_descriptor = {
    IS_NAME_FIXED: True,
    ATTRIBUTES: {
        NAME_CHECKFUNC: value_checkfunc(manifest_attributes_descriptors.keys()),
        VALUE_CHECKFUNCS: manifest_attributes_descriptors,
    },

    CHILDREN: {
        NAME_CHECKFUNC: value_checkfunc(manifest_children_descriptors.keys()),
    },
}


# package/metadata/link

link_attributes_descriptors = {
    # required
    (None, 'href'): pass_func,
    (None, 'rel'): pass_func,
    # optional
    (None, 'id'): id_func,
    (None, 'media-typ'): pass_func,
    (None, 'properties'): pass_func
}

link_des = {
    IS_NAME_FIXED: True,
    ATTRIBUTES: {
        NAME_CHECKFUNC: value_checkfunc(link_attributes_descriptors.keys()),
        VALUE_CHECKFUNCS: link_attributes_descriptors,
    },

    CHILDREN: {
        NAME_CHECKFUNC: value_checkfunc(()),
    },
}


# package/metadata/meta

meta_attributes_descriptors = {
    # required
    (None, 'property'): pass_func,
    # optional
    (None, 'id'): id_func,
    (None, 'scheme'): pass_func,
    (URI_XML, 'lang'): pass_func,
    (None, 'dir'): value_checkfunc(('ltr', 'rtl'))
}

meta_des = {
    IS_NAME_FIXED: True,
    ATTRIBUTES: {
        NAME_CHECKFUNC: value_checkfunc(meta_attributes_descriptors.keys()),
        VALUE_CHECKFUNCS: meta_attributes_descriptors,
    },

    CHILDREN: {
        NAME_CHECKFUNC: value_checkfunc(()),
    },
}


# package/metadata/metadata:type

dc_type_attributes_descriptors = {
    (None, 'id'): id_func
}

dc_type_des = {
    IS_NAME_FIXED: True,
    ATTRIBUTES: {
        NAME_CHECKFUNC: value_checkfunc(dc_type_attributes_descriptors.keys()),
        VALUE_CHECKFUNCS: dc_type_attributes_descriptors,
    },

    CHILDREN: {
        NAME_CHECKFUNC: value_checkfunc(()),
    },
}


# package/metadata/metadata:publisher

dc_publisher_attributes_descriptors = {
    (None, 'id'): id_func,
    (URI_XML, 'lang'): pass_func,
    (None, 'dir'): value_checkfunc(('ltr', 'rtl')),
    (None, 'file-as'): pass_func
}

dc_publisher_des = {
    IS_NAME_FIXED: True,
    ATTRIBUTES: {
        NAME_CHECKFUNC: value_checkfunc(dc_publisher_attributes_descriptors.keys()),
        VALUE_CHECKFUNCS: dc_publisher_attributes_descriptors,
    },

    CHILDREN: {
        NAME_CHECKFUNC: value_checkfunc(()),
    },
}


# package/metadata/metadata:creator

dc_creator_attributes_descriptors = {
    (None, 'id'): id_func,
    (URI_XML, 'lang'): pass_func,
    (None, 'dir'): value_checkfunc(('ltr', 'rtl')),
    (None, 'file-as'): pass_func
}

dc_creator_des = {
    IS_NAME_FIXED: True,
    ATTRIBUTES: {
        NAME_CHECKFUNC: value_checkfunc(dc_creator_attributes_descriptors.keys()),
        VALUE_CHECKFUNCS: dc_creator_attributes_descriptors,
    },
    CHILDREN: {
        NAME_CHECKFUNC: value_checkfunc(()),
    },
}


# package/metadata/metadata:language

dc_language_attributes_descriptors = {
    (None, 'id'): id_func
}

dc_language_des = {
    IS_NAME_FIXED: True,
    ATTRIBUTES: {
        NAME_CHECKFUNC: value_checkfunc(dc_language_attributes_descriptors.keys()),
        VALUE_CHECKFUNCS: dc_language_attributes_descriptors,
    },

    CHILDREN: {
        NAME_CHECKFUNC: value_checkfunc(()),
    },
}
# package/metadata/metadata:identifier

dc_identifier_attributes_descriptors = {
    (None, 'id'): id_func
}

dc_identifier_des = {
    IS_NAME_FIXED: True,
    ATTRIBUTES: {
        NAME_CHECKFUNC: value_checkfunc(dc_identifier_attributes_descriptors.keys()),
        VALUE_CHECKFUNCS: dc_identifier_attributes_descriptors,
    },

    CHILDREN: {
        NAME_CHECKFUNC: value_checkfunc(()),
    },
}

# package/metadata/metadata:title

dc_title_attributes_descriptors = {

    # optional
    (None, 'id'): id_func,
    (URI_XML, 'lang'): pass_func,
    (None, 'dir'): value_checkfunc(('ltr', 'rtl')),
    (None, 'file-as'): pass_func
}

dc_title_des = {
    IS_NAME_FIXED: True,
    ATTRIBUTES: {
        NAME_CHECKFUNC: value_checkfunc(dc_title_attributes_descriptors.keys()),
        VALUE_CHECKFUNCS: dc_title_attributes_descriptors
    }
}

DC_URI = 'http://purl.org/metadata/elements/1.1/'


# package/metadata

metadata_children_descriptors = {
    # any order

    (DC_URI, 'identifier'): dc_identifier_des,  # 1
    (DC_URI, 'title'): dc_title_des,  # 1
    (DC_URI, 'language'): dc_language_des,  # >= 1

    (DC_URI, 'publisher'): dc_publisher_des,  # >= 0
    (DC_URI, 'creator'): dc_creator_des,  # >= 0
    (DC_URI, 'type'): dc_type_des,  # >= 0

    (None, 'meta'): meta_des,  # >= 1
    (None, 'link'): link_des  # >= 0
}

metadata_descriptor = {
    IS_NAME_FIXED: True,
    ATTRIBUTES: {
        NAME_CHECKFUNC: value_checkfunc(())
    },
    CHILDREN: {
        NAME_CHECKFUNC: value_checkfunc(metadata_children_descriptors.keys())
    }
}


# package

package_children_descriptors = {
    (None, 'metadata'): metadata_descriptor,
    (None, 'manifest'): manifest_descriptor,
    (None, 'spine'): spine_descriptor,
    # (None, 'collection'):
}

package_attributes_descriptors = {
    # required
    (None, 'version'): value_checkfunc(('3.1',)),
    (None, 'unique-identifier'): pass_func,  # same metadata:identifier

    # optional
    (None, 'prefix'): pass_func,
    (URI_XML, 'lang'): pass_func,
    (None, 'dir'): value_checkfunc(('ltr', 'rtl')),
    (None, 'id'): pass_func
}

package_descriptor = {
    IS_NAME_FIXED: True,

    ATTRIBUTES: {
        NAME_CHECKFUNC: value_checkfunc(value_checkfunc(package_attributes_descriptors.keys())),
        VALUE_CHECKFUNCS: package_attributes_descriptors
    },
    CHILDREN: {
        NAME_CHECKFUNC: value_checkfunc(package_children_descriptors.keys()),
        DESCRIPTORS: package_children_descriptors
    }
}
