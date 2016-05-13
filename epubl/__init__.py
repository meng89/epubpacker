"""用户不用关心文件名字"""

import zipfile

from hooky import List, Dict

from xl import Element


class Files(Dict):
    pass


class Epubl:

    def __init__(self, filename=None):
        if filename:
            pass

        else:
            self._package_dom = Element('package')
            self._files = Files()

