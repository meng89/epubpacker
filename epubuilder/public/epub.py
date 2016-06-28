import uuid
import os
import string
import random

from abc import abstractmethod


from hooky import List, Dict


from epubuilder.xl import Element, Text, pretty_insert, xml_header

import epubuilder.version
from epubuilder.public.meta.base import Base
from epubuilder import mimes
from epubuilder.public.meta.dcmes import Identifier


CONTAINER_PATH = 'META-INF' + os.sep + 'container.xml'
ROOT_OF_OPF = 'EPUB'


class Metadata(List):
    """list-like.

    store metadata, such as author, publisher etc."""
    def _before_add(self, key=None, item=None):
        if not isinstance(item, Base):
            raise TypeError


class Toc(List):
    """list-like.

    table of contents

    store :class:`Section` objects.
    """
    def __init__(self):
        super().__init__()
        self.title = None

        self.ncx_depth = -1
        self.ncx_totalPageCount = -1
        self.ncx_maxPageNumber = -1


class Section:
    """
    store title, href and sub :class:`Section` objects.
    """
    def __init__(self, title, href=None):
        """
        :param title: title of content.
        :type title: str
        :param href: html link to a file path in :class:`Epub.files`, can have a bookmark. example: `text/a.html#hello`
        :type href: str
        """
        self._title = title
        self._href = href

    @property
    def title(self):
        """as class parameter"""
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def href(self):
        """ as class parmeter"""
        return self._href

    @href.setter
    def href(self, value):
        self._href = value

    @property
    @abstractmethod
    def subs(self):
        return []

    def to_toc_ncx_element(self):
        nav_point = Element('navPoint', attributes={'id': 'id_' + uuid.uuid4().hex})

        nav_label = Element('navLabel')
        nav_point.children.append(nav_label)

        text = Element('text')
        nav_label.children.append(text)

        text.children.append(Text(self.title))

        content = Element('content', attributes={'src': self.href if self.href else ''})
        nav_point.children.append(content)

        for subsection in self.subs:
            nav_point.children.append(subsection.to_toc_ncx_element())

        return nav_point


class Files(Dict):
    """dict-like.

    store file path and :class:`File` objects from `key` and `item`,
    every file you want to package to book, you should use this."""
    def _before_add(self, key=None, item=None):
        if not isinstance(item, File):
            raise TypeError

    def to_elements(self):
        items = []

        for path, file in self.items():
            item = Element('item', attributes={(None, 'href'): path})

            if file.identification is not None:
                item.attributes[(None, 'id')] = file.identification

            item.attributes[(None, 'media-type')] = file.mime or mimes.map_from_extension[os.path.splitext(path)[1]]

            items.append(item)

        return items


class File:
    """every file you want to put in book, you shoud use this."""
    def __init__(self, binary, mime=None, identification=None, fallback=None):
        """
        :param binary: binary data
        :type binary: bytes
        :param mime: mime
        :type mime: str
        :param identification: xml attribute: `id`
        :type identification: str
        :param fallback:
        :type fallback: file
        """

        self._binary = binary
        self.mime = mime
        self.identification = identification or 'id_' + uuid.uuid4().hex
        self.fallback = fallback

    @property
    def binary(self):
        """as class parmeter"""
        return self._binary


class Spine(List):
    """list-like.

    "The spine defines the default reading order"

    store :class:`Joint` objects.
    """

    def _before_add(self, key=None, item=None):
        if not isinstance(item, Joint):
            raise TypeError


class Joint:
    def __init__(self, path, linear=None):
        """
        :param path: file path, should in Epub.Files.keys()
        :type path: str
        :param linear: I don't know what is this mean. visit http://idpf.org to figure out by yourself.
        :type linear: bool
        """
        self._path = path
        self.linear = linear

    @property
    def path(self):
        """as class parmeter"""
        return self._path


class Epub:
    def __init__(self):
        self._metadata = Metadata()
        self._files = Files()
        self._spine = Spine()
        self._toc = Toc()

        self._cover_path = None

        # for self.write()
        self._temp_files = Files()

        self._cover_path = None

    metadata = property(lambda self: self._metadata, doc=str(Metadata.__doc__ if Metadata.__doc__ else ''))

    files = property(lambda self: self._files, doc=str(Files.__doc__ if Files.__doc__ else ''))

    spine = property(lambda self: self._spine, doc=str(Spine.__doc__ if Spine.__doc__ else ''))

    toc = property(lambda self: self._toc, doc=str(Toc.__doc__ if Toc.__doc__ else ''))

    @property
    def cover_path(self):
        """tag your file as a cover"""
        return self._cover_path

    @cover_path.setter
    def cover_path(self, path):
        if path is not None and path not in self.files.keys():
            raise ValueError()

        self._cover_path = path

    def _get_ncx_xmlstring(self):
        def_uri = 'http://www.daisy.org/z3986/2005/ncx/'

        ncx = Element('ncx', attributes={'version': '2005-1'}, prefixes={def_uri: None})
        head = Element('head')
        ncx.children.append(head)

        # same as dc:Identifier

        identifier_text = None
        for m in self.metadata:
            if isinstance(m, Identifier):
                identifier_text = m.text
                break

        head.children.append(Element('meta', attributes={'name': 'dtb:uid', 'content': identifier_text}))

        head.children.append(Element('meta', attributes={'name': 'dtb:depth', 'content': self.toc.ncx_depth}))

        head.children.append(Element('meta', attributes={'name': 'dtb:totalPageCount',
                                                         'content': self.toc.ncx_totalPageCount}))

        head.children.append(Element('meta', attributes={'name': 'dtb:maxPageNumber',
                                                         'content': self.toc.ncx_maxPageNumber}))

        head.children.append(Element('meta', attributes={'name': 'dtb:generator',
                                                         'content': 'epubuilder ' + epubuilder.version.__version__}))

        doc_title = Element('docTitle')
        ncx.children.append(doc_title)

        text = Element('text')
        doc_title.children.append(text)

        text.children.append(Text(self.toc.title))

        nav_map = Element('navMap')
        ncx.children.append(nav_map)

        for one in self.toc:
            nav_map.children.append(one.to_toc_ncx_element())

        return pretty_insert(ncx, dont_do_when_one_child=True).string()

    @staticmethod
    def _get_container_xmlstring(opf_path):
        e = Element('container')

        e.attributes['version'] = '1.0'

        e.prefixes['urn:oasis:names:tc:opendocument:xmlns:container'] = None

        rootfiles = Element('rootfiles')
        e.children.append(rootfiles)

        rootfile = Element('rootfile')
        rootfiles.children.append(rootfile)

        rootfile.attributes['full-path'] = opf_path

        rootfile.attributes['media-type'] = 'application/oebps-package+xml'

        return xml_header() + pretty_insert(e, dont_do_when_one_child=True).string()

    def _get_unused_filename(self, dire, filename):
        dire = dire or ''

        only_name, ext = os.path.splitext(filename)
        unused_filename = filename

        while ROOT_OF_OPF + dire + '/' + unused_filename in [ROOT_OF_OPF + '/' + path for path in self.files.keys()] +\
                [ROOT_OF_OPF + '/' + path for path in self._temp_files.keys()]:

            unused_filename = '_{}{}'.format(
                random.random(''.join(random.sample(string.ascii_letters + string.digits, 8))),
                ext
            )

        return unused_filename

    @abstractmethod
    def write(self, filename):
        """write to file.

        :param filename: file name.
        :type filename: str
        """
