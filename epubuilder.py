#!/bin/env python3
# coding=utf-8

import os
import time
import uuid
import zipfile

import magic
from lxml import etree

import userlist

version = '0.1.0'

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
    ['Styles', [E_CSS]],
    ['Scripts', [E_JS]],
]


class PathError(Exception):
    pass


class MediaTypeError(Exception):
    pass


class File(object):
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

    def get_media_type(self):
        media_type = None
        for k, es in MEDIA_TYPES.items():
            if self.extension in es:
                media_type = k
        return media_type

    @property
    def extension(self):
        return os.path.splitext(self._path)[1]


class Epub(object):
    def __init__(self,):
        self._files_root_dir = 'EPUB'
        self._content_path = '{}/content.opf'.format(self._files_root_dir)
        self._container_path = 'META-INF/container.xml'
        # self.EPUB2fallback = False

        self.title = None
        self.identifier = uuid.uuid1().urn
        self.language = None

        self._nav_file = None

        self._sections = []
        '''
        [
            {
                'title': '1 XXX',
                'link': '',
                'sub_sections':
                    [
                        'title': '1.2 XXX', 'link': '', 'sub_sections': []
                    ]
            }
        ]
        '''
        def spine_add_check(item):
            if item['file'] not in self.files:
                raise ValueError('file not in files')
        self._spine = userlist.UserList(add_check_fun=spine_add_check)

        def files_add_check(item):
            if item.path in [file.path for file in self.files]:
                raise ValueError('file.path is already in files')
        self._files = userlist.UserList(add_check_fun=files_add_check)

        def landmarks_add_check(item):
            if item['type'] not in ['cover', 'titlepage', 'frontmatter', 'bodymatter', 'backmatter', 'toc', 'loi',
                                    'lot', 'preface', 'bibliography', 'index', 'glossary', 'acknowledgments']:
                raise ValueError('landmark type is wrong')
        self._landmarks = userlist.UserList(add_check_fun=landmarks_add_check)

    def set_title(self, title):
        self.title = title

    def set_identifier(self, identifier):
        self.identifier = identifier

    def set_language(self, language):
        self.language = language

    @property
    def files(self):
        return self._files

    @property
    def spine(self):
        return self._spine

    @property
    def landmarks(self):
        return self._landmarks

    def set_toc(self, branch, link=None):
        """
        set table of contents in the book

        :param branch: an list form of chapters and sections, like: ['Chapter 1 ', 'Section 1']
        :param link: path of file in epub
        :return: None
        """
        section = self._create_and_get_section(self._sections, branch)
        section['link'] = link

    def write(self, filename):
        zip_file = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
        zip_file.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)

        for file in self._files:
            zip_file.writestr('{}/{}'.format(self._files_root_dir, file.path), file.binary, zipfile.ZIP_STORED)

        for doc, path in ((self._get_container(), self._container_path),
                          (self._get_xml_content(), self._content_path)):
            zip_file.writestr(path, self._tostring(doc), zipfile.ZIP_STORED)

        zip_file.writestr('{}/{}'.format(self._files_root_dir, self._nav_file.path), self._nav_file.binary)

    @staticmethod
    def _create_and_get_section(sections, branch):
        """

        :param sections:
        :param branch:
        :return:
        """
        if len(branch) > 1:
            sub_sections = None
            for section in sections:
                if section['title'] == branch[0]:
                    sub_sections = section['sub_sections']
                    break

            if not sub_sections:
                sub_sections = []
                sections.append({'title': branch[0], 'sub_sections': sub_sections})

            return Epub._create_and_get_section(sub_sections, branch[1:])

        elif len(branch) == 1:
            s = None
            for section in sections:
                if section['title'] == branch[0]:
                    s = section

            if not s:
                s = {'title': branch[0], 'sub_sections': []}
                sections.append(s)
            return s

    @staticmethod
    def _get_file_id(file):
        return file.path.replace('/', '_')

    @staticmethod
    def _tostring(doc):
        return etree.tostring(doc, pretty_print=True, encoding='utf-8', xml_declaration=True, standalone="yes")

    def _get_container(self):
        doc = etree.Element('container', version='1.0', xmlns='urn:oasis:names:tc:opendocument:xmlns:container')
        rootfiles = etree.SubElement(doc, 'rootfiles')
        rootfile = etree.SubElement(rootfiles, 'rootfile')
        rootfile.set('full-path', self._content_path)
        rootfile.set('media-type', 'application/oebps-package+xml')
        return doc

    def _get_xml_content(self):
        doc = etree.Element('package', xmlns='http://www.idpf.org/2007/opf', version='3.0')
        doc.set('unique-identifier', 'uid')
        self._create_xml_content_metadata(doc)
        self._create_xml_content_manifest(doc)
        self._create_xml_content_spine(doc)
        self._create_xml_content_guide(doc)
        return doc

    def _create_xml_content_metadata(self, node):
        dc = "http://purl.org/dc/elements/1.1/"
        opf = "http://www.idpf.org/2007/opf"

        metadata = etree.SubElement(node, 'metadata', nsmap={'dc': dc, 'opf': opf})

        dc_identifier = etree.SubElement(metadata, '{' + dc + '}' + 'identifier')
        dc_identifier.set('id', 'uid')
        dc_identifier.text = self.identifier
        dc_title = etree.SubElement(metadata, '{' + dc + '}' + 'title')
        dc_title.text = self.title
        dc_language = etree.SubElement(metadata, '{' + dc + '}' + 'language')
        dc_language.text = self.language

        meta_property_dcterms_modified = etree.SubElement(metadata, 'meta', property='dcterms:modified')
        meta_property_dcterms_modified.text = time.strftime('%Y-%m-%dT%XZ', time.gmtime())
        '''
        <dc:language>en</dc:language>
        <meta property="dcterms:modified">2011-01-01T12:00:00Z</meta>
        '''

    def _create_xml_content_manifest(self, node):
        self._update_nav_file()
        manifest = etree.SubElement(node, 'manifest')
        item = etree.SubElement(manifest, 'item',  properties='nav', href=self._nav_file.path, id='nav')
        item.set('media-type', self._nav_file.get_media_type())

        for file in self._files:
            item = etree.SubElement(manifest, 'item', href=file.path, id=self._get_file_id(file))
            item.set('media-type', file.get_media_type())

    def _create_xml_content_spine(self, node):
        spine = etree.SubElement(node, 'spine')
        for joint in self.spine:
            itemref = etree.SubElement(spine, 'itemref', idref=self._get_file_id(joint['file']))
            if 'linear' in joint.keys():
                itemref.set('linear', 'yes' if joint['linear'] else 'no')

    def _create_xml_content_guide(self, node):
        pass

    def _get_nav(self):
        epub = 'http://www.idpf.org/2007/ops'
        doc = etree.Element('html', xmlns='http://www.w3.org/1999/xhtml',
                            nsmap={'epub': epub})

        etree.SubElement(doc, 'head')
        body = etree.SubElement(doc, 'body')

        nav_t = etree.SubElement(body, 'nav', id='toc')
        nav_t.set('{' + epub + '}' + 'type', 'toc')
        Epub._get_toc_ol_node(nav_t, self._sections)

        nav_l = etree.SubElement(body, 'nav', id='landmarks')
        nav_l.set('{' + epub + '}' + 'type', 'landmarks')
        self._get_landmarks_ol_node(nav_l)
        return doc

    @staticmethod
    def _get_toc_ol_node(node, sections):
        ol = etree.SubElement(node, 'ol')
        for section in sections:
            li = etree.SubElement(ol, 'li')
            a = etree.SubElement(li, 'a')
            a.set('href', section['link'])
            a.text = section['title']
            if section['sub_sections']:
                Epub._get_toc_ol_node(li, section['sub_sections'])
        return ol

    def _get_landmarks_ol_node(self, node):
        epub = 'http://www.idpf.org/2007/ops'

        ol = etree.SubElement(node, 'ol')
        for landmark in self.landmarks:
            li = etree.SubElement(ol, 'li')
            a = etree.SubElement(li, 'a')
            a.set('href', landmark['file'].path)
            a.set('{' + epub + '}' + 'type', landmark['type'])
            a.text = landmark['text']

        return ol

    def _update_nav_file(self):
        binary = Epub._tostring(self._get_nav())
        if self._nav_file:
            self._nav_file._binary = binary
        else:
            self._nav_file = File('nav.xhtml', binary)


class EasyEpub(object):
    def __init__(self):
        self._epub = Epub()

        self._cover_image_file = None
        self._cover_page_file = None
        self._cover_joint = None
        self._cover_landmark = None

        self._landmark_bodymatter = None

        self.set_language = self._epub.set_language
        self.set_title = self._epub.set_title
        self.set_identifier = self._epub.set_identifier

        self.set_toc = self._epub.set_toc

    def add_page(self, page, path=None, linear=None):
        if not isinstance(page, bytes):
            raise Exception
        if magic.from_buffer(page, mime=True) != b'application/xml':
            raise Exception

        if not path:
            path = self._recommend_file_path(self._recommend_directory('page.xhtml') + '/' + 'page.xhtml')
        file = File(path, page)

        self._epub.files.append(file)
        joint = {'file': file}
        if linear is not None:
            joint.update({'linear': linear})
        self._epub.spine.append(joint)
        return file

    def add_other_file(self, src_path):
        binary = open(src_path, 'rb').read()
        file_name = os.path.split(src_path)[1]
        path = self._recommend_file_path(self._recommend_directory(file_name) + '/' + file_name)
        file = File(path, binary)
        self._epub.files.append(file)
        return file

    def create_cover_from_xhtml_binary(self, cover_binary):
        if not isinstance(cover_binary, bytes):
            raise Exception
        if magic.from_buffer(cover_binary, mime=True) != b'application/xml':
            raise Exception

        cover_path = self._recommend_file_path(self._recommend_directory('cover.xhtml') + '/' + 'cover.xhtml')

        cover_page_file = File(cover_path, cover_binary)
        cover_joint = {'file': cover_page_file, 'linear': 'yes', 'info': 'easy_epub_cover'}
        cover_landmark = {'file': cover_page_file, 'type': 'cover', 'text': 'cover', 'info': 'easy_epub_cover'}

        self._cover_joint and self._epub.spine.remove(self._cover_joint)
        self._cover_page_file and self._epub.files.remove(self._cover_page_file)
        self._cover_landmark and self._epub.landmarks.remove(self._cover_landmark)

        self._epub.files.append(cover_page_file)
        self._epub.spine.insert(0, cover_joint)
        self._epub.landmarks.insert(0, cover_landmark)

        self._cover_page_file = cover_page_file
        self._cover_joint = cover_joint
        self._cover_landmark = cover_landmark

        return cover_page_file

    def create_cover_from_image(self, image_path):
        """create image file first, and create cover file"""
        image_file = self.add_other_file(image_path)

        cover_path = self._recommend_file_path(self._recommend_directory('cover.xhtml') + '/' + 'cover.xhtml')
        cover_binary = self._create_cover_page(image_file, self._relative_position(image_file.path,
                                                                                   os.path.split(cover_path)[0]))
        cover_page_file = File(cover_path, cover_binary)
        cover_joint = {'file': cover_page_file, 'linear': False, 'info': 'easy_epub_cover'}

        self._cover_joint and self._epub.spine.remove(self._cover_joint)
        self._cover_page_file and self._epub.files.remove(self._cover_page_file)
        self._cover_image_file and self._epub.files.remove(self._cover_image_file)

        self._epub.files.append(cover_page_file)
        self._epub.spine.insert(0, cover_joint)

        self._cover_image_file = image_file
        self._cover_page_file = cover_page_file
        self._cover_joint = cover_joint

        return image_file, cover_page_file

    def write(self, path):
        self._epub.write(path)

    @staticmethod
    def _recommend_directory(file_name):
        half_name, ext = os.path.splitext(file_name)
        reconmmend_directory = 'Unkown'
        for dire, exts in DEFAULT_DIRECTORY:
            if ext in exts:
                reconmmend_directory = dire
                break
        return reconmmend_directory

    def _recommend_file_path(self, path):
        recommend_path = path
        directory, name = os.path.split(path)
        half_name, ext = os.path.splitext(name)

        i = 0
        while True:
            if recommend_path not in [file.path for file in self._epub.files]:
                break
            recommend_path = '{}/{}_{}{}'.format(directory, half_name, i, ext)
            i += 1

        return recommend_path

    @staticmethod
    def _create_cover_page(file, image_path):
        image_es = (E_GIF, E_JPEG, E_JPG, E_SVG)

        if not isinstance(file, File):
            raise TypeError('must be an instance of File, not {}'.format(type(file)))

        elif os.path.splitext(file.path)[1] not in image_es:
            raise MediaTypeError('item.media_type must be one of: {}, not {}'.format(image_es,
                                                                                     os.path.splitext(file.path)[1]))

        # width, height = Image.open(io.BytesIO(file.binary)).size

        xml = 'http://www.w3.org/XML/1998/namespace'
        epub = 'http://www.idpf.org/2007/ops'

        doc = etree.Element('html', xmlns='http://www.w3.org/1999/xhtml', lang='en', nsmap={'epub': epub})
        doc.set('{'+xml+'}'+'lang', 'en')
        head = etree.SubElement(doc, 'head')
        title = etree.SubElement(head, 'title')
        title.text = 'Cover'
        body = etree.SubElement(doc, 'body')
        img = etree.SubElement(body, 'img')
        img.set('src', image_path)
        img.set('alt', 'Cover Image')
        img.set('title', 'Cover Image')
        img.set('width', '100%')
        return etree.tostring(doc, encoding='utf-8', doctype='<!DOCTYPE html>', standalone=True)

    @staticmethod
    def _relative_position(full_path, dirt):
        paths = full_path.split('/')
        dirs = dirt.split('/')
        l = len(paths) if len(paths) >= len(dirs) else len(dirs)
        for i in range(l):
            if len(paths) == i or len(dirs) == i or paths[i] != dirs[i]:
                return '/'.join(['..'] * len(dirs[i:]) + list(paths[i:]))
