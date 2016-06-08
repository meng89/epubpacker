from abc import abstractmethod

from hooky import List


class Metadata(List):
    pass


class Public:
    @property
    @abstractmethod
    def text(self):
        pass

    @text.setter
    @abstractmethod
    def text(self, value):
        pass

    @property
    @abstractmethod
    def attrs(self):
        pass

    @abstractmethod
    def as_element(self):
        pass
