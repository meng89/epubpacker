from epubuilder.utils import List, Dict


class Manfiest:
    def __init__(self):
        super().__init__()
        pass


class Items(List):
    def __init__(self):
        super().__init__()
        pass


class Item:
    def __init__(self):
        required_keys = ['id', 'href', 'media-type']

        # 当一个item存在 spine 中，且 media-type 非标准时 必须要指定一个id，这个id也可以有fallback，直到media-type是标准时。
        conditionally_keys = ['fallback']

        optional_keys = ['properties', 'media-overlay']

        self._attributes = Dict()

    @property
    def attributes(self):
        return self._attributes

