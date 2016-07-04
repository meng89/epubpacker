import string
import uuid

import os
import random
from abc import abstractmethod
from hooky import List, Dict

from epubuilder.public import mimes
from epubuilder.public.metas.base import Base
from epubuilder.xl import Element, pretty_insert, xml_header

CONTAINER_PATH = 'META-INF' + os.sep + 'container.xml'
ROOT_OF_OPF = 'EPUB'


class FatherEpub:
    @property
    def _epub(self):
        return self.__epub

    @_epub.setter
    def _epub(self, value):
        self.__epub = value


class Metadata(List):
    """list-like.

    store metadata, such as author, publisher etc."""
    def _before_add(self, key=None, item=None):
        if not isinstance(item, Base):
            raise TypeError


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


class Spine(List, FatherEpub):
    """list-like.

    "The spine defines the default reading order"

    store :class:`Joint` objects.
    """

    def _before_add(self, key=None, item=None):
        if not isinstance(item, Joint):
            raise TypeError

    def _after_add(self, key=None, item=None):
        setattr(self[key], '_epub', self._epub)
        print('heihei')

    def to_element(self):
        spine = Element('spine')
        for joint in self:
            spine.children.append(joint.to_element())
        return spine


class Joint(FatherEpub):
    def __init__(self, path, linear=None):
        """
        :param path: file path, in Epub.Files.keys()
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

    def to_element(self):
        itemref = Element('itemref', attributes={(None, 'idref'): self._epub.files[self.path].identification})

        if self.linear is True:
            itemref.attributes[(None, 'linear')] = 'yes'
        elif self.linear is False:
            itemref.attributes[(None, 'linear')] = 'no'


class EPUB:
    def __init__(self):
        self._metadata = Metadata()
        setattr(self._metadata, '_epub', self)

        self._files = Files()
        setattr(self._files, '_epub', self)

        self._spine = Spine()
        setattr(self._spine, '_epub', self)
        print('haha')

        # self._toc = Toc()

        self._cover_path = None

        # for self.write()
        self._temp_files = Files()

        self._cover_path = None

    metadata = property(lambda self: self._metadata, doc=str(Metadata.__doc__ if Metadata.__doc__ else ''))

    files = property(lambda self: self._files, doc=str(Files.__doc__ if Files.__doc__ else ''))

    spine = property(lambda self: self._spine, doc=str(Spine.__doc__ if Spine.__doc__ else ''))

    # toc = property(lambda self: self._toc, doc=str(Toc.__doc__ if Toc.__doc__ else ''))

    @staticmethod
    def _find_ncx_id(items):
        ncx_id = None
        for item in items:
            if item.attributes[(None, 'media-type')] == mimes.NCX:
                ncx_id = item.attributes[(None, 'id')]
                break
        return ncx_id

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
