from epubuilder.xl import Element

from .public import Base


class Meta(Base):
    def __init__(self):
        super().__init__()
        self._name

    def to_element(self):
        m = Element('meta', attributes={'name'})
