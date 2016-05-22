"""用户不用关心 OPF 的文件名"""

import zipfile
import random
import os
import string


from hooky import List, Dict

import xl


from .package_descriptor import package_descriptor


class Files(Dict):
    pass


CONTAINER_PATH = 'META-INF' + os.sep + 'container.xml'

ROOT_OF_OPF = 'EPUB'


media_table = [
    ['image/gif', ['.gif'], 'Images'],
    ['image/jpeg', ['.jpg', 'jpeg'], 'Images'],
    ['image/png', ['.png'], 'Images'],
    ['image/svg+xml', ['.svg'], 'Images'],

    ['application/xhtml+xml', ['.html', '.xhtml'], 'Text'],

    ['application/x-dtbncx+xml', ['.ncx'], '?'],

    ['application/vnd.ms-opentype', ['.otf', '.ttf', '.ttc'], 'Fonts'],
    ['application/font-woff', ['.woff'], 'Fonts'],
    ['application/smil+xml', [], ''],
    ['application/pls+xml', [], ''],

    ['audio/mpeg', [], ''],
    ['audio/mp4', ['.mp4'], ''],

    ['text/css', ['.css'], 'Styles'],

    ['text/javascript', ['.js'], 'Scripts'],
]


class Meta:
    def __init__(self):
        self._text = None
        self._attr = {}

    @property
    def text(self):
        return self._text


def make_meta(key):
    pass


class Metadata(Dict):
    def __init__(self):
        super().__init__()

    def __getitem__(self, key):
        if key not in self.data.keys():
            self.data[key] = make_meta(key)

        return self.data[key]


class Section:
    def __init__(self, title, href=None):
        self._title = title
        self._href = href
        self._subsections = []

        self._hidden_sub = None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def href(self):
        return self._href

    @href.setter
    def href(self, value):
        self._href = value

    @property
    def subsections(self):
        return self._subsections

    #
    @property
    def hidden_sub(self):
        return self._hidden_sub

    @hidden_sub.setter
    def hidden_sub(self, value):
        if value not in (True, False):
            raise ValueError
        else:
            self._hidden_sub = value

    def as_element(self):
        li = xl.Element('li')

        if self.href:
            a_or_span = xl.Element('a')
            a_or_span.attributes['href'] = self.href
        else:
            a_or_span = xl.Element('span')

        if self.subsections:
            ol = xl.Element('ol')
            for one in self.subsections:
                ol.children.append(one.as_element())

            a_or_span.children.append(ol)

        li.children.append(a_or_span)

        return li


#####################################
# Manifest

class Item:
    def __init__(self, i_d, href, media_type):
        self._id = i_d
        self._href = href
        self._media_type = media_type

#####################################


#####################################
# Spine

class Itemref:
    def __init__(self, idref, linear=None):
        self._idref = idref
        self._linear = linear

#####################################


class Epub:
    def __init__(self):

        self._files = Files()

        self._metadata = Metadata()

        self._manifest = List()

        self._spine = List()

        # nav
        self._toc = List()
        self._landmark = List()
        self._pagelist = List()

        # self._package_element.descriptor = package_descriptor

    @property
    def files(self):
        return self._files

    @property
    def metadata(self):
        return self._metadata

    @property
    def manifest(self):
        return self._manifest

    @property
    def spine(self):
        return self._spine

    @property
    def toc(self):
        return self._toc

    @property
    def landmark(self):
        return self._landmark

    @property
    def pagelist(self):
        return self._pagelist

    def _xmlstr_nav(self):
        nav_e = xl.Element('')

        return nav_e.to_string()

    def _xmlstr_opf(self):
        self._opf_path = ROOT_OF_OPF + os.sep + 'package.opf'

        while self._opf_path in [ROOT_OF_OPF + os.sep + path for path in self.files.keys()]:
            self._opf_path = ROOT_OF_OPF + os.sep + 'package_{}.opf'.format(
                random.random(''.join(random.sample(string.ascii_letters + string.digits, 8)))
            )

        return self._opf_element.to_string()

    def _xmlstr_container(self):
        e = xl.Element('container')
        e.attributes['version'] = '1.0'
        e.attributes['xmlns'] = 'urn:oasis:names:tc:opendocument:xmlns:container'

        rootfiles = xl.Element('rootfiles')
        e.children.append(rootfiles)

        rootfile = xl.Element('rootfile')
        rootfiles.children.append(rootfile)

        rootfile.attributes['full-path'] = self._opf_path

        rootfile.attributes['media-type'] = 'application/oebps-package+xml'

        return xl.xml_header() + e.to_string()

    def write(self, filename):
        z = zipfile.ZipFile(filename, 'w')
        z.writestr('mimetype', b'application/epub+zip', compress_type=zipfile.ZIP_STORED)

        for file, data in self._files:
            z.writestr(ROOT_OF_OPF + os.sep + file, data, zipfile.ZIP_DEFLATED)

        z.writestr(self._opf_path, self._xmlstr_opf(), zipfile.ZIP_DEFLATED)

        z.writestr(CONTAINER_PATH, self._xmlstr_container().decode(), zipfile.ZIP_DEFLATED)

        z.close()
