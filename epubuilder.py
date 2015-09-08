#!/bin/env python3
# coding=utf-8

import os
import io
import time
import uuid
import zipfile

import magic
from lxml import etree
from PIL import Image

version = '0.0.1'

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

DEFAULT_DIRECTORY = [
    ['Text', [E_XHTML]],
    ['Images', [E_JPG, E_JPEG, E_PNG, E_SVG, E_GIF]],
    ['Fonts', [E_OTF, E_TTC, E_TTF]],
    ['Video', [E_MP4, E_MPEG]],
    ['Styles'], [E_CSS],
    ['Scripts', [E_JS]],
]


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
    def __init__(self, path, binary):
        self._id = uuid.uuid1()
        self._binary = binary
        self._path = path

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
        self._content_path = 'OEBPS/content.opf'
        self._container_path = 'META-INF/container.xml'
        # self.EPUB2fallback = False

        self.title = None
        self.language = None

        self._cover_item = None

        self._files = []
        self._toc_item = None

        self._sections = []
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

        self.spine = []

    def add_file(self, path, data):
        if path in [one.path for one in self._files]:
            raise PathError('path:"{}" already exist.')
        else:
            item = Item(path, data)
            self._files.append(item)
        return item

    def files_iter(self):
        return iter(self._files)

    def set_section(self, branch, link=None):
        section = _create_and_get_section(self._sections, branch)
        section['link'] = link

    def add_to_spine(self, file):
        if file in self._files:
            self.spine.append(file)
        else:
            raise Exception

    def write(self, filename):
        zip_file = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
        zip_file.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)

        for doc, path in ((self._get_container(), self._container_path),
                          (self._get_xml_content(), self._content_path)):
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

        for i in self._files:
            item = etree.SubElement(manifest, 'item', href=i.path, id=i.id)
            item.set('media-type', i.media_type())

    def _create_xml_content_spine(self, node):
        spine = etree.SubElement(node, 'spine')
        for item in self.spine:
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
            SimpleEPUB()._get_toc_ol_node(nav, self._sections)

    @staticmethod
    def _get_toc_ol_node(node, sections):
        ol = etree.SubElement(node, 'ol')
        for section in sections:
            li = etree.SubElement(ol, 'li')
            a = etree.SubElement(li, 'a')
            a.set('herf', section['link'])
            a.text = section['title']
            if section['sub_sections']:
                SimpleEPUB()._get_toc_ol_node(li, section['sub_sections'])

    def _update_toc_item(self):
        binary = SimpleEPUB._tostring(self._get_toc())
        if self._toc_item:
            self._toc_item._binary = binary
        else:
            self._toc_item = Item(binary, 'toc.xhtml')


class StupidEPUB(object):
    """
    def create_cover():

    def add_page():

    def add_file():

    def write():

    """
    def __init__(self, ):
        pass


class EasyEPUB(object):
    def __init__(self):
        self._epub = SimpleEPUB()
        self._cover = None

    def add_page(self, page, path=None):
        if not isinstance(page, bytes):
            raise Exception
        if magic.from_buffer(page, mime=True) != b'application/xml':
            raise Exception

        if not path:
            i = 1
            while True:
                path = 'Text/page_{}.xhtml'.format(str(i))
                if path not in [item.path for item in self._epub.files_iter()]:
                    break

        item = self._epub.add_file(page, path)
        self._epub.add_to_spine(item)
        return item

    def add_other_file(self, src_path):
        binary = open(src_path, 'rb').read()
        file_name = os.path.split(src_path)[1]
        path = self._recommend_item_path(self._recommend_directory(file_name) + '/' + file_name)
        item = self._epub.add_file(path, binary)
        return item

    def create_cover(self, image_path):
        """create image file first, and create cover file"""
        image = self.add_other_file(image_path)

        cover_path = self._recommend_item_path(self._recommend_directory('cover.xhtml') + '/' + 'cover.xhtml')

        cover_binary = self._create_cover_page(image, self._relative_position(image.path, os.path.split(cover_path)[0]))

        cover = self._epub.add_file(cover_path, cover_binary)

        self._cover = cover

        return image, cover

    @staticmethod
    def _recommend_directory(file_name):
        half_name, ext = os.path.splitext(file_name)
        reconmmend_directory = 'Unkown'
        for dire, exts in DEFAULT_DIRECTORY:
            if ext in exts:
                reconmmend_directory = dire
                break
        return reconmmend_directory

    def _recommend_item_path(self, path):
        recommend_path = None
        directory, name = os.path.split(path)
        half_name, ext = os.path.splitext(name)
        i = 1
        while True:
            if recommend_path not in [item.path for item in self._epub.files_iter()]:
                break
            else:
                recommend_path = '{}/{}_{}{}'.format(directory, half_name, i, ext)
                i += 1
        return recommend_path

    # def _recommend_item_id(self, path):
    #    directory, name = os.path.split(path)
    #    recommend_id = None
    #    i = 1
    #    while True:
    #        if recommend_id not in [item.path for item in self._items]:
    #            break
    #        else:
    #            recommend_id = '{}-{}'.format(name, i)
    #            i += 1
    #    return recommend_id

    @staticmethod
    def _create_cover_page(item, image_path):
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
        image.set('xlink:href', image_path)

        return etree.tostring(doc, encoding='utf-8', doctype='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" '
                                                             '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">')

    @staticmethod
    def _relative_position(full_path, dirt):
        paths = full_path.split('/')
        dirs = dirt.split('/')
        l = len(paths) if len(paths) >= len(dirs) else len(dirs)
        for i in range(l):
            if len(paths) == i or len(dirs) == i or paths[i] != dirs[i]:
                return '/'.join(['..'] * len(dirs[i:]) + list(paths[i:]))
