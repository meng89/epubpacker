from epubuilder.xl import Element

from ._ import _Idref, _Linear, _Id, _Properties


class _PageProgressionDirection(_E):
    @property
    def page_progression_direction(self):
        """option"""
        return self._e.attributes['page-progression-direction']

    @page_progression_direction.setter
    def page_progression_direction(self, v):
        if v in ('ltr', 'rtl', 'default'):
            self._e.attributes['page-progression-direction'].value = v
        else:
            raise Exception


class Spine(_Id, _PageProgressionDirection):
    def __init__(self, element=None):
        super().__init__(element or Element('spine'))


class Itemref(_Idref, _Linear, _Id, _Properties):
    def __init__(self, element=None):
        super().__init__(element or Element('itemref'))
