from .baseclasses import List


class Ocf:
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


class Container:
    def __init__(self, xmlstr=None):

        self.rootfiles = List()


class Rootfile:
    def __init__(self, full_path, media_type):
        self.full_path = full_path
        self.media_type = media_type


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
