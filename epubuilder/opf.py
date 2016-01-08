from epubuilder.baseclasses import List, Dict, Limit

from epubuilder.xl import Element


class SubsQuantityError(Exception):
    pass


class SubTypeError(Exception):
    pass


class AttributeQuantityError(Exception):
    pass


class Package(Element):
    def check(self):
        # order = [Metadata, Manifest, Spine,  Guide, Bindings]

        items = self.children.copy()

        for item, c in ((items[0], Metadata), (items[1], Manifest), (items[2], Spine)):
            if isinstance(item, c):
                item.check()
            else:
                raise SubTypeError
        items = items[3:]

        if items:
            if isinstance(items[0], Guide):
                items[0].check()
                del items[0]

        if items:
            if isinstance(items[0], Bindings):
                items[0].check()
                del items[0]

        while items:
            if isinstance(items[0], Collection):
                items[0].check()
                del items[0]
            else:
                raise SubTypeError


class Metadata(Element):
    def check(self):
        if len(self.attributes) != 0:
            raise AttributeQuantityError

        items = self.children.copy()
        dc_identifiers = [item for item in items if item.name == 'dc:identifier']
        for dc_identifier in dc_identifiers:
            dc_identifier.check()


class DcIdentifier(Element):
    def check(self):




class Manifest(Element):
    def check(self):
        for item in self.children:
            if isinstance(item, Item):
                item.check()
            else:
                raise TypeError


class Item(Element):
    def check(self):
        keys = self.attributes.keys()

        if 'id' not in keys:
            raise AttributeError
        else:
            keys.remove('id')
        if [item for item in self.parent if item.atttributes['id'] == self.attributes['id']] > 1:
            raise AttributeError

        if 'href' not in keys:
            raise AttributeError
        else:
            keys.remove('href')
        if self.attributes['href'] not in [file.path for file in self.parent.parent.parent.parent.files]:
            raise AttributeError()

        if 'media-type' not in keys:
            raise AttributeError
        else:
            keys.remove('media-type')

        if 'fallback' in keys():
            keys.remove('fallback')
        if 'properties':
            keys.remove('properties')
        if 'media-overlay':
            keys.remove('media-overlay')

        if keys:
            raise AttributeError()


class Spine(Element):
    def check(self):
        keys = self.attributes.keys()

        if 'id' in keys:
            keys.remove('id')

        if 'toc' in keys:
            keys.remove('id')

        if 'page-progression-direction':
            if self.attributes['page-progression-direction'] not in ('ltr', 'rtl', 'default'):
                raise AttributeError
            keys.remove('page-progression-direction')

        if keys:
            raise AttributeError

        if len(self.sub_elements) < 1:
            raise SubsQuantityError

        for item in self.sub_elements:
            if isinstance(item, Itemref):
                item.check()
            else:
                raise SubTypeError


class Itemref(Element):
    def check(self):
        keys = self.attributes.keys()
        if 'idref' in keys():
            if self.attributes['idref'] not in [item.attributes['id']
                                                for item in self.parent.parent[1].sub_elements]:
                raise AttributeError
            keys.remove('idref')
        else:
            raise AttributeError

        if 'linear' in keys:
            if self.attributes['linear'] not in ('yes', 'no'):
                raise AttributeError
            keys.remove('linear')

        if 'id' in keys:
            keys.remove('id')

        if 'properties' in keys:
            keys.remove('properties')

        if len(self.sub_elements) > 1:
            raise SubsQuantityError


# DEPRECATED
class Guide(Element):
    pass


class Bindings(Element):
    def check(self):
        if len(self.attributes) > 1:
            raise AttributeError

        if len(self.sub_elements) < 1:
            raise SubsQuantityError

        for item in self.sub_elements:
            if isinstance(item, MediaType):
                item.check()
            else:
                raise SubTypeError


class MediaType(Element):
    def check(self):
        keys = self.attributes.keys()

        if 'media-type' in keys:
            keys.remove('media-type')
        else:
            raise AttributeError

        if 'handle' in keys:
            keys.remove('handle')
        else:
            raise AttributeError

        if len(self.sub_elements) > 1:
            raise SubsQuantityError


class Collection(Element):
    def check(self):
        keys = self.attributes.keys()

        if 'xml:lang' in keys:
            keys.remove('xml:lang')

        if 'dir' in keys:
            keys.remove('dir')

        if 'id' in keys:
            keys.remove('id')

        if 'role' in keys:
            keys.remove('role')
        else:
            raise AttributeError
