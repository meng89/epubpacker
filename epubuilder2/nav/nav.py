from epubl.package_descriptor import value_checkfunc, pass_func, XML_URI
from xl import IS_NAME_FIXED, ATTRIBUTES, NAME_CHECKFUNC, VALUE_CHECKFUNCS, CHILDREN, DESCRIPTORS

package_children_descriptors = {
    (None, 'metadata'): metadata_descriptor,
    (None, 'manifest'): manifest_descriptor,
    (None, 'spine'): spine_descriptor,
    # (None, 'collection'):
}

package_attributes_descriptors = {
    # required
    (None, 'version'): value_checkfunc(('3.1',)),
    (None, 'unique-identifier'): pass_func,  # same dc:identifier

    # optional
    (None, 'prefix'): pass_func,
    (XML_URI, 'lang'): pass_func,
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
