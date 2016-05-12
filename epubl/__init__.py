import zipfile

from hooky import List

from xl import Element


class Source:


class File:
    def __init__(self):
        self._path = None
        self._source_type = None # one in ('path', 'epub', 'bytes')
        self._

    @property
    def path(self):
        return self._path


class Epubl:
    def __init__(self):
        self._package_element = Element('package')

        self._files = List()