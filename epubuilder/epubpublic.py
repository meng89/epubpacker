import uuid
import os
from abc import abstractmethod

from epubuilder.meta.public import Base
from . import mimes

from .xl import Element, Text


from hooky import List, Dict


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
