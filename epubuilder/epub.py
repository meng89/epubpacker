from abc import abstractmethod

import os
import string
import random

from epubuilder.xl import Element, Text, pretty_insert, xml_header

from epubuilder.meta.dcmes import Identifier
import epubuilder.version

from . import epubpublic as p


CONTAINER_PATH = 'META-INF' + os.sep + 'container.xml'
ROOT_OF_OPF = 'EPUB'


class Epub:
    def __init__(self):
        self._metadata = p.Metadata()
        self._files = p.Files()
        self._spine = p.Spine()
        self._toc = p.Toc()

        self._cover_path = None

        # for self.write()
        self._temp_files = p.Files()

        self._cover_path = None

    metadata = property(lambda self: self._metadata, doc=str(p.Metadata.__doc__ if p.Metadata.__doc__ else ''))

    files = property(lambda self: self._files, doc=str(p.Files.__doc__ if p.Files.__doc__ else ''))

    spine = property(lambda self: self._spine, doc=str(p.Spine.__doc__ if p.Spine.__doc__ else ''))

    toc = property(lambda self: self._toc, doc=str(p.Toc.__doc__ if p.Toc.__doc__ else ''))

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
        pass
