from abc import abstractmethod

from hooky import List


class Metadata(List):
    pass


class Public:
    @abstractmethod
    def as_element(self):
        pass
