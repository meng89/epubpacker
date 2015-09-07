#!/bin/env python3
# coding=utf-8

version = '0.0.1'

import os
import io
import time
import uuid
import zipfile

import magic
from lxml import etree
from PIL import Image

E_GIF = '.gif'
E_JPG = '.jpg'
E_JPEG = '.jpeg'
E_PNG = '.png'
E_SVG = '.svg'
E_XHTML = '.xhtml'
E_NCX = '.ncx'
E_OTF = '.otf'
E_TTF = '.ttf'
E_TTC = '.ttc'
E_MPEG = '.mpeg'
E_MP4 = '.mp4'
E_CSS = '.css'
E_JS = '.js'

MEDIA_TYPES = {
    'image/gif': ['.gif'],
    'image/jpeg': ['.jpg', 'jpeg'],
    'image/png': ['.png'],
    'image/svg+xml': ['.svg'],

    'application/xhtml+xml': ['.xhtml'],

    'application/x-dtbncx+xml': [E_NCX],
    'application/vnd.ms-opentype': ['.otf', '.ttf', '.ttc'],
    'application/font-woff': ['.woff'],
    'application/smil+xml': [],
    'application/pls+xml': [],

    'audio/mpeg': [],
    'audio/mp4': ['.mp4'],

    'text/css': ['.css'],
    'text/javascript': ['.js'],
}


class PathError(Exception):
    pass


class MediaTypeError(Exception):
    pass


def _create_and_get_section(sections, elements):
    """
     神奇的函数！
    """
    if len(elements) > 1:
        sub_sections = None
        for section in sections:
            if section['title'] == elements[0]:
                sub_sections = section['sub_sections']
                break

        if not sub_sections:
            sub_sections = []
            sections.append({'title': elements[0], 'sub_sections': sub_sections})

        return _create_and_get_section(sub_sections, elements[1:])

    elif len(elements) == 1:
        s = None
        for section in sections:
            if section['title'] == elements[0]:
                s = section

        if not s:
            s = {'title': elements[0], 'sub_sections': []}
            sections.append(s)
        return s


class Item(object):
    def __init__(self, binary, path):
        self._id = uuid.uuid1()
        self._binary = binary
        self._path = path

    @property
    def id(self):
        return self._id

    @property
    def path(self):
        return self._path

    @property
    def binary(self):
        return self._binary

    @property
    def media_type(self):
        media_type = None
        for k, es in MEDIA_TYPES:
            if self.extension in es:
                media_type = k
        return media_type

    @property
    def extension(self):
        return os.path.splitext(self._path)[1]


class SimpleEPUB(object):
    def __init__(self):
        self.files = []


class StupidEPUB(object):
    """
    def create_cover():

    def add_page():

    def add_file():

    def write():

    """
    def __init__(self, ):
        self.title = None
        self.language = None

        self.EPUB2fallback = False

        self._content_path = 'OEBPS/content.opf'
        self._container_path = 'META-INF/container.xml'

        self._cover_item = None

        self._toc_item = None

        self._items = []

        self._sections = []
        # like this:
        '''
        [
            {
                'title': '1',
                'link': '',
                'sub_sections':
                    [
                        'title': '2', 'link': '', 'sub_sections': []
                    ]
            }
        ]
        '''

        self._spine = {'cover': None, 'toc': None, 'pages': []}

    def _update_toc_item(self):
        binary = StupidEPUB._tostring(self._get_toc())
        if self._toc_item:
            self._toc_item._binary = binary
        else:
            self._toc_item = Item(binary, 'toc.xhtml')

    def set_section(self, branch, link=None, hidden_sub=True):
        section = _create_and_get_section(self._sections, branch)
        section['link'] = link
        section['hidden_sub'] = hidden_sub

    def add_item(self, item):
        if item.path in [one.path for one in self._items]:
            raise PathError('path:"{}" already exist.')
        else:
            self._items.append(item)

    def write(self, filename):
        zip_file = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
        zip_file.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)

        for doc, path in ((self._get_container(), self._container_path), (self._get_xml_content(), self._content_path)):
            zip_file.writestr(path, self._tostring(doc), zipfile.ZIP_STORED)

    @staticmethod
    def _tostring(doc):
        return etree.tostring(doc, pretty_print=True, encoding='utf-8', xml_declaration=True)

    def _get_container(self):
        doc = etree.Element('container', version='1.0', xmlns='urn:oasis:names:tc:opendocument:xmlns:container')
        rootfiles = etree.SubElement(doc, 'rootfiles')
        rootfile = etree.SubElement(rootfiles, 'rootfile')
        rootfile.set('full-path', self._content_path)
        rootfile.set('media-type', 'application/oebps-package+xml')
        return doc

    def _get_xml_content(self):
        doc = etree.Element('package', xmlns='http://www.idpf.org/2007/opf', version='3.0')

        self._create_xml_content_metadata(etree.SubElement(doc, 'metadata'))
        self._create_xml_content_manifest(etree.SubElement(doc, 'manifest'))
        self._create_xml_content_spine(etree.SubElement(doc, 'spine'))
        self._create_xml_content_guide(etree.SubElement(doc, 'guide'))

    def _create_xml_content_metadata(self, node):
        metadata = etree.SubElement(node, 'metadata')
        metadata.set('xmlns:dc', "http://purl.org/dc/elements/1.1/")
        dc_identifier = etree.SubElement(metadata, 'dc:identifier')
        dc_identifier.set(id="pub-id")
        dc_identifier.text = 'urn:uuid:' + uuid.uuid1()
        dc_title = etree.SubElement(metadata, 'dc:title')
        dc_title.text = self.title
        dc_language = etree.SubElement(metadata, 'dc:language')
        dc_language.text = self.language
        meta_property_dcterms_modified = etree.SubElement(metadata, 'meta', property='dcterms:modified')
        meta_property_dcterms_modified.text = time.strftime('%Y-%m-%d %X %Z', time.localtime(time.time()))
        '''
        <dc:language>en</dc:language>
        <meta property="dcterms:modified">2011-01-01T12:00:00Z</meta>
        '''

    def _create_xml_content_manifest(self, node):
        self._update_toc_item()
        manifest = etree.SubElement(node, 'manifest')
        item = etree.SubElement(manifest, 'item',  properties='nav', href=self._toc_item.path, id='toc')
        item.set('media-type', self._toc_item.get_media_type())

        for i in self._items:
            item = etree.SubElement(manifest, 'item', href=i.path, id=i.id)
            item.set('media-type', i.media_type())

    def _create_xml_content_spine(self, node):
        spine = etree.SubElement(node, 'spine')
        for item in [self._spine['cover'], self._spine['toc']] + self._spine['pages']:
            if item:
                etree.SubElement(spine, 'itemref', itemref=item.id)

    def _create_xml_content_guide(self, node):
        pass

    def _get_toc(self):
        doc = etree.Element('html', xmlns='http://www.w3.org/1999/xhtml')
        doc.set('xmlns:epub', 'http://www.idpf.org/2007/ops')
        etree.SubElement(doc, 'head')
        body = etree.SubElement(doc, 'body')
        nav = etree.SubElement(body, 'nav', id='toc')
        nav.set('epub:type', 'toc')
        if self._sections:
            StupidEPUB()._get_toc_ol_node(nav, self._sections)

    @staticmethod
    def _get_toc_ol_node(node, sections):
        ol = etree.SubElement(node, 'ol')
        for section in sections:
            li = etree.SubElement(ol, 'li')
            a = etree.SubElement(li, 'a')
            a.set('herf', section['link'])
            a.text = section['title']
            if section['sub_sections']:
                StupidEPUB()._get_toc_ol_node(li, section['sub_sections'])


class EasyEPUB(StupidEPUB):
    def __init__(self):
        super(EasyEPUB, self).__init__()

    def add_page(self, page, path=None):
        if not isinstance(page, bytes):
            raise Exception
        if magic.from_buffer(page, mime=True) != b'application/xml':
            raise Exception

        if not path:
            i = 1
            while True:
                path = 'Text/page_{}.xhtml'.format(str(i))
                if path not in [item.path for item in self._items]:
                    break
        item = Item(page, path)
        self.add_item(item)
        self._spine['pages'].append(item)
        return item

    def create_cover(self, image_path):
        binary = open(image_path, 'rb').read()
        image = Item(binary, 'Images/' + os.path.split(image_path)[0])
        self.add_item(image)
        cover = Item(self._create_cover_page(image), 'Text/cover.xhtml')
        self.add_item(cover)
        self._spine['cover'] = cover
        return image, cover

    @staticmethod
    def _create_cover_page(item):
        image_es = (E_GIF, E_JPEG, E_JPG, E_SVG)

        if isinstance(item, Item):
            raise TypeError('must be an instance of epub.Item')
        elif os.path.splitext(item.path)[0] not in image_es:
            raise MediaTypeError('item.media_type must be one of: ', image_es)

        width, height = Image.open(io.BytesIO(item.binary)).size

        doc = etree.Element('html', xmlns='http://www.w3.org/1999/xhtml')
        head = etree.SubElement(doc, 'head')
        title = etree.SubElement(head, 'title')
        title.text = 'Cover'
        body = etree.SubElement(doc, 'body')
        div = etree.SubElement(body, 'div', style='text-align: center; padding: 0pt; margin: 0pt;')
        svg = etree.SubElement(div, 'svg', xmlns="http://www.w3.org/2000/svg", height="100%",
                               preserveAspectRatio="xMidYMid meet", version="1.1",
                               viewBox="0 0 {} {}".format(width, height),
                               width="100%")
        svg.set('xmlns:xlink', 'http://www.w3.org/1999/xlink')
        image = etree.SubElement(svg, 'image', width=str(width), height=str(height))
        image.set('xlink:href', item.path)

        return etree.tostring(doc, encoding='utf-8', doctype='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" '
                                                             '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">')
