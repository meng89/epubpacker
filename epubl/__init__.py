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


class Epubl:
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

            self._package_element = xl.parse(z.read(opf_path).decode())
            self._package_element.descriptor = package_descriptor

            self._files = Files
            for filename in z.namelist():
                top, _filename = filename.split(os.sep, 1)

                if top == self._top_of_opf:
                    self._files[_filename] = z.read(filename)

        else:
            self._top_of_opf = 'EPUB'
            self._package_element = xl.Element('package')
            self._nav_element = xl.Element('')
            self._files = Files()

    @property
    def files(self):
        return self._files

    @property
    def package_element(self):
        return self._package_element

    def write(self, filename):
        z = zipfile.ZipFile(filename, 'w')
        z.writestr('mimetype', b'application/epub+zip', compress_type=zipfile.ZIP_STORED)

        for file, data in self._files:
            z.writestr(self._top_of_opf + os.sep + file, data, zipfile.ZIP_DEFLATED)

        z.writestr(self._opf_path, self._package_xmlstr(), zipfile.ZIP_DEFLATED)

        z.writestr(CONTAINER_PATH, self._container_xmlstr().decode(), zipfile.ZIP_DEFLATED)

        z.close()

    def _package_xmlstr(self):

        self._opf_path = self._top_of_opf + os.sep + 'package.opf'
        while self._opf_path in [self._top_of_opf + os.sep + path for path in self.files.keys()]:
            self._opf_path = self._top_of_opf + os.sep + 'package_{}.opf'.format(
                random.random(''.join(random.sample(string.ascii_letters + string.digits, 8)))
            )

        return self._package_element.to_string()

    def _container_xmlstr(self):
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
