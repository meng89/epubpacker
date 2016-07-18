# coding=utf-8

import string
import uuid

import os
import random
from abc import abstractmethod
from hooky import List, Dict

from epubuilder.public import mimes
from epubuilder.public.metas.base import Base
from epubuilder.xl import Xl, Element, pretty_insert

CONTAINER_PATH = 'META-INF' + os.sep + 'container.xml'
ROOT_OF_OPF = 'EPUB'


class FatherEpub:
    def __init__(self):
        pass

    @property
    def _epub(self):
        return self.__epub

    @_epub.setter
    def _epub(self, value):
        self.__epub = value


class Metadata(List):
    """list-like.

    Store metadata, such as author, publisher etc.

    see :mod:`epubuilder.public.metas`"""
    def _before_add(self, key=None, item=None):
        if not isinstance(item, Base):
            raise TypeError


########################################################################################################################
# Files File
########################################################################################################################
class Files(Dict, FatherEpub):
    """dict-like.

    Store file path and :class:`epubuilder.public.File` objects from `key` and `item`.
    Any file you want to package them into the book, you have to use this."""
    def _before_add(self, key=None, item=None):
        if not isinstance(item, File):
            raise TypeError

    def _after_add(self, key=None, item=None):
        setattr(self[key], '_epub', self._epub)

########################################################################################################################
class File(FatherEpub):
    def __init__(self, binary, mime=None, fallback=None):
        """
        :param binary: binary data
        :type binary: bytes
        :param mime: mime
        :type mime: str
        :param fallback:
        :type fallback: File
        """

        FatherEpub.__init__(self)

        self._binary = binary
        self.mime = mime
        # self.identification = identification or 'id_' + uuid.uuid4().hex
        self.fallback = fallback

    @property
    def binary(self):
        """as class parmeter"""
        return self._binary


########################################################################################################################
# Spine Joint
########################################################################################################################
class Spine(List, FatherEpub):
    """list-like.

    "The spine defines the default reading order"

    store :class:`epubuilder.public.Joint` objects.
    """

    def _before_add(self, key=None, item=None):
        if not isinstance(item, Joint):
            raise TypeError

    def _after_add(self, key=None, item=None):
        setattr(self[key], '_epub', self._epub)

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
        FatherEpub.__init__(self)
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

        return itemref


########################################################################################################################
# Epub
########################################################################################################################
class Epub:
    def __init__(self):
        self._metadata = Metadata()
        setattr(self._metadata, '_epub', self)

        self._files = Files()
        setattr(self._files, '_epub', self)

        self._spine = Spine()
        setattr(self._spine, '_epub', self)

        # for opf etc.
        self._temp_files = Files()
        setattr(self._temp_files, '_epub', self)

        self._opf_e_ids = []

    metadata = property(lambda self: self._metadata, doc=str(Metadata.__doc__ if Metadata.__doc__ else ''))

    files = property(lambda self: self._files, doc=str(Files.__doc__ if Files.__doc__ else ''))

    spine = property(lambda self: self._spine, doc=str(Spine.__doc__ if Spine.__doc__ else ''))

    def _files_to_manifest(self, files):
        """

        :param files:
         :type files: Files
        :return:
        """

        items = []

        for path, file_ in files:
            item = Element('item', attributes={(None, 'href'): path})

            item.attributes[(None, 'media-type')] = file_.mime or mimes.map_from_extension[
                os.path.splitext(path)[1]]

            identification = xml_identify(path)
            new_id = identification
            i = 1
            while identification in self._opf_e_ids:
                new_id = identification + '_' + str(i)

            item.attributes[(None, 'id')] = new_id

            items.append(item)

        return items

    def _make_item_ids(self, manifest):
        """

        :param manifest:
         :type manifest: Element
        :return:
        """

        for item in manifest.children

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

        return Xl(root=pretty_insert(e, dont_do_when_one_child=True)).string()

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


def xml_identify(s):
    """
    :param s:
    :type s: str
    :return:
    :rtype: str
    """
    new_string = ''

    for char in s:
        if char.isalpha() or char.isdigit() or char in (':', '.', '_', '-'):
            new_string += char

        else:
            new_string += ':'

    if not new_string[0].isalpha():
        new_string = 'P_' + new_string

    return new_string