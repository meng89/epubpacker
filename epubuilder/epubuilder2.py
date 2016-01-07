import zipfile

from .baseclasses import Dict, List, Limit
from .metainfo import MetaInfo


class Epub(object):
    def __init__(self, file=None):
        self._mimetype = b'application/epub+zip'

        self.metadata = None
        self.manifest = None
        self.spine = None
        self.guide = None
        self.bindings = None

        self.toc = None

        self.files = Dict()

        if file:
            epub_zip = zipfile.ZipFile(file)

            if epub_zip.read('mimetype') != self._mimetype:
                raise Exception

            self.metainfo = MetaInfo(epub_zip=epub_zip)
            self.opf = self.metadata.container.rootfiles[0].
            for info in epub_zip.infolist():
                if info.name.split('/')[1] == 'EPUB':
                    self.files[info.name] = File(epub_zip.read(info.name), date=info.date_time, comment=info.comment)



class Files(Dict):
    def __init__(self):
        super().__init__()

        class MyLimit(Limit):
            def add_before(self, index=None, key=None, item=None, obj=None):
                if not isinstance(item, File):
                    raise Exception

        self.limits.append(MyLimit)


class File(object):
    def __init__(self, data, date=None, comment=None):
        self.data = data
        self.date = date
        self.comment = comment

    def __setattr__(self, key, value):
        pass

    def __getattr__(self, item):
        pass

class Ocf(object):
    def __init__(self, xmlstr):

class Opf(object):
    def __init__(self, file=None):
        self.metadata = Metadata()
        if file:
            pass


class Metadata(object):
    """ store title, identifier and language
    and contributor | coverage | creator | date | description | format | publisher | relation | rights | source
    | subject | type

    meta element for compatibility

    see http://www.idpf.org/epub/30/spec/epub30-publications.html#sec-metadata-elem
    """

    def __init__(self):
        pass


class Manifest(object):
    def __init__(self):
        pass


class Spine(object):
    def __init__(self):
        pass


class Guide(object):
    """ is deprecated """
    def __init__(self):
        pass


class Nav(object):
    def __init__(self):
        pass


book = Epub()


