from abc import abstractmethod


class Base:
    @abstractmethod
    def to_element(self):
        pass
