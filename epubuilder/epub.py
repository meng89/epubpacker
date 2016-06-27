from abc import abstractmethod


class Epub:

    @abstractmethod
    def write(self, filename):
        pass
