from epubuilder.baseclasses import List, Dict, Limit

from epubuilder.xl import Element









class Package(Element):
    pass


class PackageSubsLimit(Limit):
    def __init__(self):
        self.order = [Metadata,Manifest,Spine, Guide,Bindings]

    def add_before(self, index=None, key=None, item=None, obj=None):

        if isinstance(item, Metadata):
            if index == self.order.index(Metadata)
                pass
            elif

class Metadata:
    pass



class Manifest(Element):
    def __init__(self):
        super().__init__('manifest', sub_elements_limit=ManifestSubsLimit())




class ManifestSubsLimit(Limit):
    def add_before(self, index=None, key=None, item=None, obj=None):
        if not isinstance(item, Element):
            raise TypeError()
        if item.name != 'item':
            raise ValueError()

        for k, v in item.attributes.keys():
            if k == 'id':
                if v in [item.attributes['id'] for item in obj]:
                    raise AttributeError()
            if k == 'href':
                if v not in [file.path for file in obj.parent.parent.files]:
                    raise AttributeError()
            if k == 'media-type':
                pass

            if k == 'fallback':
                pass
            if k == 'properties':
                pass
            if k == 'media-overlay':
                pass
            else:
                raise AttributeError()

    def del_before(self, index=None, key=None, item=None, obj=None):
        pass


class Spine(Element):
    def __init__(self):
        super().__init__('spine', sub_elements_limit=SpineSubsLimit())


class SpineSubsLimit(Limit):
    def add_before(self, index=None, key=None, item=None, obj=None):
        if not isinstance(item, Element):
            raise TypeError()
        if item.name != 'itemref':
            raise ValueError()

        for k, v in item.attributes.keys():
            if k == 'id':
                if v in [item.attributes['id'] for item in obj]:
                    raise AttributeError()
            if k == 'href':
                if v not in [file.path for file in obj.parent.parent.files]:
                    raise AttributeError()
            if k == 'media-type':
                pass

            if k == 'fallback':
                pass
            if k == 'properties':
                pass
            if k == 'media-overlay':
                pass
            else:
                raise AttributeError()

    def del_before(self, index=None, key=None, item=None, obj=None):
        pass


class Guide:
    pass


class Bindings:
    pass