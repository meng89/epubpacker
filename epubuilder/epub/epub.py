import string
import uuid
import zipfile

import os
import random
from hooky import List, Dict

from epubuilder.tools import identify_mime

from epubuilder.xl import pretty_insert, Element, Text, xml_header, URI_XML

from .metadata import Metadata
from .metadata.dcmes import Identifier, URI_DC

import epubuilder.version

CONTAINER_PATH = 'META-INF' + os.sep + 'container.xml'


media_table = [

    # Image Types
    ['image/gif', ['.gif'], 'Images'],
    ['image/jpeg', ['.jpg', 'jpeg'], 'Images'],
    ['image/png', ['.png'], 'Images'],
    ['image/svg+xml', ['.svg'], 'Images'],

    # Application Types
    ['application/xhtml+xml', ['.html', '.xhtml'], 'Text'],
    ['application/font-sfnt', ['.otf', '.ttf', '.ttc'], 'Fonts'],  # old 'application/vnd.ms-opentype'
    ['application/font-woff', ['.woff'], 'Fonts'],
    ['application/smil+xml', [], 'Text'],  # EPUB Media Overlay documents
    ['application/pls+xml', [], ''],  # Text-to-Speech (TTS) Pronunciation lexicons

    # Audio Types
    ['audio/mpeg', [], ''],
    ['audio/mp4', ['.mp4'], ''],

    # Text Types
    ['text/html', [], 'Text'],
    ['text/css', ['.css'], 'Styles'],
    ['text/javascript', ['.js'], 'Scripts'],

    # Font Types
    ['font/woff2', ['.woff2'], 'Fonts'],
]


##################################################
# toc


def html_dir():
    _html_dir = os.path.join(os.path.dirname(__file__), 'html')
    if os.path.exists(_html_dir):
        if not os.path.isdir(_html_dir):
            raise FileNotFoundError

    return _html_dir


class Toc(List):
    def __init__(self):
        super().__init__()
        self.title = None

        self.add_js_for_nav_flod = False

        # todo
        self.ncx_depth = -1
        self.ncx_totalPageCount = -1
        self.ncx_maxPageNumber = -1

    def _before_add(self, key=None, item=None):
        if not isinstance(item, Section):
            raise TypeError


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

    @property
    def hidden_sub(self):
        return self._hidden_sub

    @hidden_sub.setter
    def hidden_sub(self, value):
        if value not in (True, False):
            raise ValueError
        else:
            self._hidden_sub = value

    def to_toc_element(self):
        li = Element('li')

        if self.href:
            a_or_span = Element((None, 'a'))
            a_or_span.attributes[(None, 'href')] = self.href
        else:
            a_or_span = Element((None, 'span'))

        a_or_span.children.append(Text(self.title))

        li.children.append(a_or_span)

        if self.subsections:
            ol = Element('ol')

            if self.hidden_sub:
                ol.attributes[(None, 'hidden')] = ''

            for one in self.subsections:
                ol.children.append(one.to_toc_element())

            li.children.append(ol)

        return li

    def to_toc_ncx_element(self):
        nav_point = Element('navPoint', attributes={'id': 'id_' + uuid.uuid4().hex})

        nav_label = Element('navLabel')
        nav_point.children.append(nav_label)

        text = Element('text')
        nav_label.children.append(text)

        text.children.append(Text(self.title))

        content = Element('content', attributes={'src': self.href if self.href else ''})
        nav_point.children.append(content)

        for subsection in self.subsections:
            nav_point.children.append(subsection.to_toc_ncx_element())

        return nav_point


####################################
# for Manifest and zip files

class Files(Dict):
    def _before_add(self, key=None, item=None):
        if not isinstance(item, File):
            raise TypeError

    def to_elements(self):
        elements = []
        for path, file in self.items():
            item = Element((None, 'item'), attributes={(None, 'href'): path, (None, 'media-type'): file.mime})

            if file.identification is not None:
                item.attributes[(None, 'id')] = file.identification

            # for _TempFile
            try:
                if getattr(file, 'properties'):
                    item.attributes['properties'] = getattr(file, 'properties')
            except AttributeError:
                pass

            elements.append(item)

        return elements


class File:
    def __init__(self, binary, mime=None, identification=None):
        self._binary = binary
        self.mime = mime or identify_mime(self.binary)
        self.identification = identification or 'id_' + uuid.uuid4().hex

    @property
    def binary(self):
        return self._binary


class _TempFile(File):
    def __init__(self, binary, mime=None, identification=None, properties=None):
        super().__init__(binary, mime, identification)
        self.properties = properties


#####################################
# for Spine

class Spine(List):
    def _before_add(self, key=None, item=None):
        if not isinstance(item, Itemref):
            raise TypeError


class Itemref:
    def __init__(self, idref, linear=None):
        self._idref = idref
        self._linear = linear

    @property
    def idref(self):
        return self._idref

    def to_element(self):
        e = Element((None, 'itemref'), attributes={(None, 'idref'): self.idref})

        if self._linear is True:
            e.attributes[(None, 'linear')] = 'yes'
        elif self._linear is False:
            e.attributes[(None, 'linear')] = 'no'

        return e


#####################################

ROOT_OF_OPF = 'EPUB'


class Epub:
    def __init__(self):

        self._files = Files()

        self._metadata = Metadata()

        self._spine = Spine()

        # nav
        self._toc = Toc()
        self._landmark = List()
        self._pagelist = List()

        # for self.write()
        self._temp_files = Files()

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

    @property
    def files(self):
        return self._files

    @property
    def metadata(self):
        return self._metadata

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

    def _nav_to_tempfile(self):
        default_ns = 'http://www.w3.org/1999/xhtml'
        epub_ns = 'http://www.idpf.org/2007/ops'

        html = Element((None, 'html'), prefixes={default_ns: None, epub_ns: 'epub'})

        head = Element('head')
        html.children.append(head)

        if self.toc.title:
            _title = Element('title')
            head.children.append(_title)
            _title.children.append(Text(self.toc.title))

        body = Element((None, 'body'))
        html.children.append(body)

        if self.toc:
            nav = Element((None, 'nav'), prefixes={epub_ns: 'epub'}, attributes={(epub_ns, 'type'): 'toc'})
            ol = Element((None, 'ol'))

            for section in self.toc:
                ol.children.append(section.to_toc_element())

            nav.children.append(ol)
            body.children.append(nav)

        if self.toc.add_js_for_nav_flod:
            js_path = self._get_unused_filename(None, 'a.js')
            self._temp_files[js_path] = _TempFile(open(os.path.join(html_dir(), 'a.js'), 'rb').read(),
                                                  mime='text/javascript')

            # css_path = self._get_unused_filename(None, 'a.css')
            # self._temp_files[css_path] = _TempFile(open(os.path.join(html_dir(), 'css.js'), 'rb').read(),
            #                                       mime='text/style')

            head.children.append(Element('script', attributes={'src': js_path}))
            script_before_body_close = Element('script', attributes={'type': 'text/javascript'})
            script_before_body_close.children.append(Text('set_button();'))

            body.children.append(script_before_body_close)

        toc_filename = self._get_unused_filename(None, 'nav.xhtml')

        self._temp_files[toc_filename] = \
            _TempFile(pretty_insert(html, dont_do_when_one_child=True).string().encode(),
                      mime='application/xhtml+xml',
                      properties='nav scripted' if self.toc.add_js_for_nav_flod else 'nav')

    def _ncx_to_tempfile(self):
        def_ns_uri = 'http://www.daisy.org/z3986/2005/ncx/'

        ncx = Element('ncx', attributes={'version': '2005-1'}, prefixes={def_ns_uri: None})
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

        toc_ncx_filename = self._get_unused_filename(None, 'toc.ncx')
        self._temp_files[toc_ncx_filename] = \
            _TempFile(pretty_insert(ncx, dont_do_when_one_child=True).string().encode(),
                      mime='application/x-dtbncx+xml')

    def _xmlstr_opf(self):
        def_ns = 'http://www.idpf.org/2007/opf'
        # dcterms_ns = 'http://purl.org/metadata/terms/'

        package = Element((None, 'package'),
                          prefixes={def_ns: None},
                          attributes={(None, 'version'): '3.0', (URI_XML, 'lang'): 'en'})

        for m in self.metadata:
            if isinstance(m, Identifier):
                package.attributes['unique-identifier'] = m.as_element().attributes[(None, 'id')]

        # unique - identifier = "pub-id"
        # metadata
        metadata_e = Element((None, 'metadata'),
                             prefixes={URI_DC: 'dc'})

        for m in self.metadata:
            metadata_e.children.append(m.as_element())

        package.children.append(metadata_e)

        # manifest
        manifest = Element((None, 'manifest'))
        package.children.append(manifest)

        manifest.children.extend(self.files.to_elements())

        manifest.children.extend(self._temp_files.to_elements())

        # find toc ncx id for spine
        toc_ncx_item_e_id = None
        for temp_file_e in self._temp_files.to_elements():
            if temp_file_e.attributes[(None, 'media-type')] == 'application/x-dtbncx+xml':
                toc_ncx_item_e_id = temp_file_e.attributes[(None, 'id')]

        # spine
        spine = Element((None, 'spine'))
        package.children.append(spine)

        spine.attributes['toc'] = toc_ncx_item_e_id

        for itemref in self.spine:
            spine.children.append(itemref.to_element())

        return pretty_insert(package, dont_do_when_one_child=True).string()

    @staticmethod
    def _xmlstr_container(opf_path):
        e = Element((None, 'container'))

        e.attributes[(None, 'version')] = '1.0'

        e.prefixes['urn:oasis:names:tc:opendocument:xmlns:container'] = None

        rootfiles = Element('rootfiles')
        e.children.append(rootfiles)

        rootfile = Element('rootfile')
        rootfiles.children.append(rootfile)

        rootfile.attributes['full-path'] = opf_path

        rootfile.attributes['media-type'] = 'application/oebps-package+xml'

        return xml_header() + pretty_insert(e, dont_do_when_one_child=True).string()

    def write(self, filename):

        z = zipfile.ZipFile(filename, 'w', compression=zipfile.ZIP_DEFLATED)

        z.writestr('mimetype', 'application/epub+zip'.encode('ascii'), compress_type=zipfile.ZIP_STORED)

        # wirte custom files
        for filename, file in self.files.items():
            z.writestr(ROOT_OF_OPF + os.sep + filename, file.binary, zipfile.ZIP_DEFLATED)

        self._nav_to_tempfile()
        self._ncx_to_tempfile()

        # write nav nav's js and ncx
        for filename, file in self._temp_files.items():
            z.writestr(ROOT_OF_OPF + os.sep + filename, file.binary, zipfile.ZIP_DEFLATED)

        opf_filename = self._get_unused_filename(None, 'package.opf')
        z.writestr(ROOT_OF_OPF + '/' + opf_filename,
                   self._xmlstr_opf().encode(),
                   zipfile.ZIP_DEFLATED)

        z.writestr(CONTAINER_PATH,
                   self._xmlstr_container(ROOT_OF_OPF + '/' + opf_filename).encode(),
                   zipfile.ZIP_DEFLATED)

        z.close()
