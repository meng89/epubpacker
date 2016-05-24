
from hooky import Dict


def none_func(*args, **kwargs):
    return True

check_table = {
    'opf:alt-script': none_func,
    'dir': none_func,
    'opf:file-as': none_func,
    'id': none_func,
    'opf:role': none_func,
    'xml:lang': none_func
}


def meta(name):
    if name == 'Creator':
        available_attrs = ('opf:alt-script', 'dir', 'opf:file-as', 'id', 'opf:role', 'xml:lang')
    elif name == 'dc:title':
        available_attrs = ('opf:alt-script', 'dir', 'opf:file-as', 'id', 'opf:role', 'xml:lang')

    class Meta(Dict):
        def __init__(self):
            super().__init__()

        def __setitem__(self, key, value):
            if key == 'text':
                self._text = value

            elif key in available_attrs:

                if check_table[key](value):
                    self.__dict__[key] = value

                else:
                    raise ValueError

            else:
                raise KeyError

    return Meta
