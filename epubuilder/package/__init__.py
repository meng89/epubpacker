# opf

from epubuilder.xl import Element, Text


class Package:
    def __init__(self, file=None):
        self.metadata = Metadata()
        if file:
            pass


class Metadata(object):
    """child of Package
    """

    def __init__(self):
        pass


class DcIdentifier:
    """dc:identifier, child of Metadata
    """
    def __init__(self, element=None):
        self._e = element or Element('dc:identifier')

    @property
    def id(self):
        return self._e.attributes['id']

    @id.setter
    def id(self, v):
        self._e.attributes['id'].value = v

    @property
    def text(self):
        return self._e.children[0].to_string()

    @text.setter
    def text(self, v):
        self._e.children[0] = Text(v)


class Manifest(object):
    def __init__(self):
        pass


class Spine(object):
    def __init__(self):
        pass


class Guide(object):
    """ is deprecated """
    def __init__(self):
        pass
