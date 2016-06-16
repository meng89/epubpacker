from abc import abstractmethod


class Base:
    def __init__(self, text):
        self._text = text

    @property
    def text(self):
        return self._text

    @property
    @abstractmethod
    def attrs(self):
        pass

    @abstractmethod
    def to_element(self):
        pass
