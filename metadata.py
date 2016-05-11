from hooky import Hook, Dict


class AttrHook(Hook):
    def add_before(self, key=None, item=None, obj=None):
        if key not in ('id', 'opf:scheme'):
            raise Exception


jbm = {
    'identifier': []
       }


class M:
    def __init__(self, tag, text=None, attr=None):
        self._tag = tag
        self._attr = Dict(attr, AttrHook())
        self._text = text

    @property
    def tag(self):
        return self._tag

    @property
    def attr(self):
        return self._attr

    @property
    def text(self):
        return self._text



def make_m(tag):

