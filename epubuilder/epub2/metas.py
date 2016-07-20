# coding=utf-8

from epubuilder.xl import Element


class Meta(object):
    def __init__(self, name, content):
        super(Meta, self).__init__()
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
    def __init__(self, filepath):
        self.filepath = filepath
