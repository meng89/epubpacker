# xl means xml without mess

import xml.etree.ElementTree as Et

from epubuilder.baseclasses import List, Dict


class Node(object):
    def __init__(self):
        pass


class Text(object):
    pass


# class SubElements(List):
#    def __init__(self):
#        super().__init__()
#        pass


class Element:
    def __init__(self,
                 name, is_name_available_write=True,
                 attributes_limit=None,
                 # namespaces_limit=None,
                 sub_elements_limit=None,
                 ):
        # self._e = Et.Element(name)

        self._name = name
        self._is_name_available_write = is_name_available_write

        self._attributes = Dict(limit=attributes_limit)
        self._sub_elements = List(limit=sub_elements_limit)

        # self._namespaces = Dict(limit=namespaces_limit)

    def __setattr__(self, key, value):
        if key == 'name':
            if self._is_name_available_write:
                self._e.tag = value
            else:
                raise AttributeError("Can't write attribute: {}".format(key))

    def __getattr__(self, key):
        if key == 'name':
            return self._e.tag

    @property
    def attributes(self):
        return self._attributes

    # 喵生苦短，不玩别喵的毛线。
    # @property
    # def namespaces(self):
    #    return self._namespaces

    @property
    def sub_elements(self):
        return self._sub_elements

    @property
    def string(self):
        return None

