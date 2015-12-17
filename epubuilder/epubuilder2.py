class Epub(object):
    def __init__(self, file=None, directory=None):
        if file:
            pass


class Files(object):
    def __init__(self):
        pass


class File(object):
    def __init__(self):
        pass


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


class Item(object):
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

book.files.add_from_bytes()
book.toc.add()

boook.opf
