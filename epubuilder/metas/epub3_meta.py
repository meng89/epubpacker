# coding=utf-8

from .attrs import Attrs, AltScript, Dir, FileAs, Id, Scheme, Lang
from .dcmes import Base


class Property(Attrs):
    @property
    def property(self):
        """xml attribute: `property`"""
        return self._attrs.setdefault('property')

    @property.setter
    def property(self, value):
        self._attrs['property'] = value


class Meta3(Base, AltScript, Dir, FileAs, Id, Property, Scheme, Lang):
    """meta for Epub3.metadata"""
    def __init__(self, property_, text):
        Base.__init__(self, text)

        self.property = property_
