from epubuilder.xl import Element

from epubuilder.public.meta.base import Base


class Meta(Base):
    def __init__(self, name, content):
        super().__init__()
        self.name = name
        self.content = content

    def to_element(self):
        return Element('meta', attributes={'name': self.name, 'content': self.content})
