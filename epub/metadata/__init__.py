
from hooky import Dict

from abc import abstractproperty, abstractmethod, abstractstaticmethod


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


class _Meta(Dict):

    @property
    @abstractmethod
    def available_attrs(self):
        return ()

    def __setitem__(self, key, value):
        if key == 'text':
            self._text = value

        elif key in self.available_attrs:

            if check_funcs[key](value):
                self.__dict__[key] = value

            else:
                raise ValueError

        else:
            raise KeyError

    def to_element(self):
        pass


class Identifier(_Meta):
    @property
    def available_attrs(self):
        return 'id', 'opf:scheme'


class Title(_Meta):
    @property
    def available_attrs(self):
        return 'opf:alt-script', 'dir', 'opf:file-as', 'id', 'xml:lang'


class Language(_Meta):
    @property
    def available_attrs(self):
        return 'id',


# Optional Elements

class Contributor(_Meta):
    @property
    def available_attrs(self):
        return 'opf:alt-script', 'dir', 'opf:file-as', 'id', 'opf:role', 'xml:lang'


class Coverage(_Meta):
    @property
    def available_attrs(self):
        return 'dir', 'xml:lang'


class Creator(_Meta):
    @property
    def available_attrs(self):
        return 'opf:alt-script', 'dir', 'opf:file-as', 'id', 'opf:role', 'xml:lang'


class Date(_Meta):
    @property
    def available_attrs(self):
        return 'id',


class Description(_Meta):
    @property
    def available_attrs(self):
        return 'dir', 'id', 'xml:lang'


class Format(_Meta):
    @property
    def available_attrs(self):
        return 'id',


class Publisher(_Meta):
    @property
    def available_attrs(self):
        return 'opf:alt-script', 'dir', 'opf:file-as', 'id', 'xml:lang'


class Relation(_Meta):
    @property
    def available_attrs(self):
        return 'dir', 'id', 'xml:lang'


class Rights(_Meta):
    @property
    def available_attrs(self):
        return 'dir', 'id', 'xml:lang'


class Source(_Meta):
    @property
    def available_attrs(self):
        return 'id',


class Subject(_Meta):
    @property
    def available_attrs(self):
        return 'dir', 'id', 'xml:lang', 'opf:authority'


class Type(_Meta):
    @property
    def available_attrs(self):
        return 'id',


class Meta(_Meta):
    @property
    def available_attrs(self):
        return 'opf:alt-script', 'dir', 'opf:file-as', 'id', 'property', 'scheme', 'xml:lang'


class Link(_Meta):
    @property
    def available_attrs(self):
        return 'href', 'id', 'media-type', 'properties', 'rel'
