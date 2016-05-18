"""用户不用关心 OPF 的文件名"""

import zipfile
import random
import os
import string


from hooky import List, Dict

import xl

from xl import Element


from .package_descriptor import package_descriptor


class Files(Dict):
    pass


CONTAINER_PATH = 'META-INF' + os.sep + 'container.xml'



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
    def __init__(self, title, link=None):
        self._title = title
        self._link = link
        self._subsections = []

        self._hidden_sub = None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        self._link = value

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


class Epub:
    def __init__(self, file=None):

        self._top_of_opf = "EPUB"

        if file:
            z = zipfile.ZipFile(file)

            if z.read('mimetype') != b'application/epub+zip':
                raise TypeError('Seems its not a epub file.')

            container_e = xl.parse(z.read(CONTAINER_PATH).decode())
            if container_e.name != 'container':
                raise TypeError

            opf_path = None

            _rootfiles_e = None
            for child in container_e.children:
                if child.name == 'rootfiles':
                    _rootfiles_e = child

            _rootfile_e = None
            for child in _rootfiles_e.children:
                if child.name == 'rootfile':
                    _rootfile_e = child

            if _rootfile_e:
                opf_path = _rootfile_e.attributes['full-path']

            self._top_of_opf = opf_path.split(os.sep, 1)[0]

            self._opf_element = xl.parse(z.read(opf_path).decode())

            self._files = Files()

            for filename in z.namelist():
                top, _filename = filename.split(os.sep, 1)

                if top == self._top_of_opf:
                    self._files[_filename] = z.read(filename)

        else:
            self._top_of_opf = 'EPUB'

            self._opf_element = xl.Element('package')

            self._nav_element = xl.Element('')

            self._files = Files()

        self._metadata = Metadata()

        self._spine = List()

        # nav
        self._toc = List()
        self._landmark = List()
        self._pagelist = List()

        # self._package_element.descriptor = package_descriptor

    def add_file(self, data, path, media_type):
        pass

    @property
    def metadata(self):
        return self._metadata

    @property
    def spine(self):
        return self._spine

    # nav
    @property
    def nav_style_element(self):
        return self._nav_style_element

    @property
    def toc(self):
        return self._toc

    @property
    def landmark(self):
        return self._landmark

    @property
    def pagelist(self):
        return self._pagelist

    @property
    def files(self):
        return self._files

    @property
    def package_element(self):
        return self._opf_element

    def write(self, filename):
        z = zipfile.ZipFile(filename, 'w')
        z.writestr('mimetype', b'application/epub+zip', compress_type=zipfile.ZIP_STORED)

        for file, data in self._files:
            z.writestr(self._top_of_opf + os.sep + file, data, zipfile.ZIP_DEFLATED)

        z.writestr(self._opf_path, self._xmlstr_opf(), zipfile.ZIP_DEFLATED)

        z.writestr(CONTAINER_PATH, self._xmlstr_container().decode(), zipfile.ZIP_DEFLATED)

        z.close()

    def xmlstr_nav(self):
        return self._nav_element.to_string()

    def _xmlstr_opf(self):

        self._opf_path = self._top_of_opf + os.sep + 'package.opf'

        while self._opf_path in [self._top_of_opf + os.sep + path for path in self.files.keys()]:
            self._opf_path = self._top_of_opf + os.sep + 'package_{}.opf'.format(
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
