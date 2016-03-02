from epubuilder.xl import Element

from ._ import _Id, _Href, _MediaType, _Fallback, _Properties, _MediaOverlay, _Duration


class Manifest(_Id):
    """child of package"""
    def __init__(self, element=None):
        super().__init__(element or Element('manifest'))


class Item(_Id, _Href, _MediaType, _Fallback, _Properties, _MediaOverlay, _Duration):
    """child of manifest"""
    def __init__(self, element=None):
        super().__init__(element or Element('item'))
