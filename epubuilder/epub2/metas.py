from epubuilder.xl import Element

from epubuilder.public.metas.base import Base


class Meta(Base):
    def __init__(self, name, content):
        super().__init__()
        self.name = name
        self.content = content

    def to_element(self):
        return Element('meta', attributes={'name': self.name, 'content': self.content})


class Cover(Base):
    def __init__(self, file):
        super().__init__()
        self._file = file

    def to_element(self):
        return Meta(name='cover', content=self._file.identification).to_element()

