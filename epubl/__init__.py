"""用户不用关心文件名字"""

import zipfile

from hooky import List, Dict

from xl import Element


class Files(Dict):
    pass


class Epubl:

    def __init__(self, file=None):
        if file:
            z = zipfile.ZipFile(file)

            if z.read('mimetype') != b'application/epub+zip':
                raise TypeError('Seems its not a epub file.')

            for filename in z.namelist():

        else:
            self._package_element = Element('package')
            self._files = Files()

