from hooky import List

from epub.metadata import _Meta


class Metadata(List):
    pass


# End of Optional Elements

class Meta(_Meta):
    @property
    def element_name(self):
        return 'meta'

    @property
    def available_attrs(self):
        return 'opf:alt-script', 'dir', 'opf:file-as', 'id', 'property', 'scheme', 'xml:lang'


class Link(_Meta):
    @property
    def element_name(self):
        return 'link'

    @property
    def available_attrs(self):
        return 'href', 'id', 'media-type', 'properties', 'rel'
