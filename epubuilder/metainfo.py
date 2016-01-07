from .baseclasses import List

from . import xl


class MetaInfo:
    _container_path = 'META-INF/container.xml'
    _encryption_path = 'META-INF/encryption.xml'
    _manifest_path = 'META-INF/manifest.xml'
    _metadata_path = 'META-INF/metadata.xml'
    _rights_path = 'META-INF/rights.xml'
    _signatures_path = 'META-INF/signatures.xml'

    def __init__(self, epub_zip=None):
        # self.__dict__['_container_path'] = 'META-INF/container.xml'
        # self.__dict__['_encryption_path'] = 'META-INF/encryption.xml'
        # self.__dict__['_manifest_path'] = 'META-INF/manifest.xml'
        # self.__dict__['_metadata_path'] = 'META-INF/metadata.xml'
        # self.__dict__['_rights_path'] = 'META-INF/rights.xml'
        # self.__dict__['_signatures_path'] = 'META-INF/signatures.xml'

        self.container = Container(xmlstr=epub_zip.read(self._container_path) if epub_zip else None)

        self.encryption = Encryption(xmlstr=epub_zip.read(self._encryption_path)
                                     if (epub_zip and self._encryption_path in epub_zip.namelist()) else None)

        self.manifest = Manifest(xmlstr=epub_zip.read(self._manifest_path)
                                 if (epub_zip and self._manifest_path in epub_zip.namelist()) else None)

        self.metadata = Metadata(xmlstr=epub_zip.read(self._metadata_path)
                                 if (epub_zip and self._metadata_path in epub_zip.namelist()) else None)

        self.rights = Rights(xmlstr=epub_zip.read(self._rights_path)
                             if (epub_zip and self._rights_path in epub_zip.namelist()) else None)

        self.signatures = Signatures(xmlstr=epub_zip.read(self._signatures_path)
                                     if (epub_zip and self._signatures_path in epub_zip.namelist()) else None)

    def __setattr__(self, key, value):
        if key == 'container' and not isinstance(value, Container):
            raise Exception
        elif key == 'encryption' and not isinstance(value, Encryption):
            raise Exception
        elif key == 'manifest' and not isinstance(value, Manifest):
            raise Exception
        elif key == 'metadata' and not isinstance(value, Metadata):
            raise Exception
        elif key == 'rights' and not isinstance(value, Rights):
            raise Exception
        elif key == 'signatures' and not isinstance(value, Signatures):
            raise Exception
        else:
            raise AttributeError

        self.__dict__[key] = value


class Container:
    def __init__(self, xmlstr=None):
        self._element = xl.parse(xmlstr)
        self.rootfiles = Rootfiles(self._element.children[0])

    def get_xmlstr(self):
        pass


class Rootfiles(List):
    def __init__(self, element=None):
        super().__init__()
        self.subs = Subs()
        if element.children:
            for one in element.children:
                if one.name == 'rootfile':
                    self.subs.append(Rootfile(element=one))

    def element(self):
        e = xl.Element(name='rootfiles')
        for sub in self.subs:
            e.attributes.append(sub.element)


class Rootfile:
    def __init__(self, element=None, full_path=None, media_type=None):
        if element:
            self.full_path = element.attributes['full-path']
            self.media_type = element.attributes['media_type']
        else:
            self.full_path = full_path
            self.media_type = media_type

    def element(self):
        e = xl.Element(name='rootfile')
        e.attributes['full-path'] = self.full_path
        e.attributes['media-type'] = self.media_type
        return e


class Encryption:
    def __init__(self, xmlstr=None):
        pass


class Manifest:
    def __init__(self, xmlstr=None):
        pass


class Metadata:
    def __init__(self, xmlstr=None):
        pass


class Rights:
    def __init__(self, xmlstr=None):
        pass


class Signatures:
    def __init__(self, xmlstr=None):
        pass


class Subs(List):
    def __init__(self):
        super().__init__()