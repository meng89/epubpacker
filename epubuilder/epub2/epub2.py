from hooky import List

from .epub3 import Epub


class _Toc(List):
    def __init__(self):
        super().__init__()

        self.ncx_depth = -1
        self.ncx_totalPageCount = -1
        self.ncx_maxPageNumber = -1


class Epub2(Epub):
    def __init__(self):
        super().__init__()
        delattr(Epub2, )

