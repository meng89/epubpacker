# coding=utf-8

from epubaker.xl import Element


class Meta2(object):
    """meta for Epub2.metadata"""
    def __init__(self, name, content):
        super(Meta2, self).__init__()
        self._name = name
        self._content = content

    @property
    def name(self):
        return self._name

    @property
    def content(self):
        return self._content

    def to_element(self):
        return Element('meta', attributes={'name': self.name, 'content': self.content})


class Cover(object):
    """cover for Epub2.metadata"""
    def __init__(self, filepath):
        self.filepath = filepath
