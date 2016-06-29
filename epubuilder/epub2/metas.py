from epubuilder.xl import Element

from epubuilder.public.metas.base import Base

from abc import abstractmethod


class _Meta(Base):

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def content(self):
        pass

    def to_element(self):
        return Element('meta', attributes={'name': self.name, 'content': self.content})


class Meta(_Meta):
    def __init__(self, name, content):
        super().__init__()
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


class Cover(_Meta):
    def __init__(self, file):
        super().__init__()
        self._file = file

    @property
    def name(self):
        return 'cover'

    @property
    def content(self):
        return self._file.identification

    def to_element(self):
        return Element('meta', attributes={'name': self.name, 'content': self._file.identification})
