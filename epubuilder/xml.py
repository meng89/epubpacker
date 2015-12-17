from epubuilder.utils import List


class Node(object):
    def __init__(self):
        pass


class Element(object):
    def __init__(self, xmlstr=None):
        self._father = None

        self._type = None

        self._name = None
        self._attributes = {}

        self._sub_elements = SubElements()

    @property
    def father(self):
        return self._father

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    @property
    def attributes(self):
        return self._attributes

    @property
    def subelements(self):
        return self._sub_elements

    def string(self):
        s = '<{}'.format(self.name)
        if self.subelements:
            s += '>'
            for one in self.subelements:
                s += one.string()
            s += '</{}>'.format(self.name)
        else:
            s += ' />'
        return s


class Text(object):
    pass


class SubElements(List):
    def __init__(self):
        super().__init__()
        pass


import xml.dom.minidom
import xml.etree.ElementTree