# coding=utf-8

import zipfile

import html5lib
import os
from hooky import List

import epubuilder.epub2.epub2

from epubuilder.epub2.epub2 import Toc

from epubuilder.public import mimes

import epubuilder.public.epub as p

from epubuilder.public.epub import Epub

from epubuilder.public.metas.dcmes import Identifier, URI_DC
from .metas.dcterms import get
from epubuilder.tools import w3c_utc_date
from epubuilder.xl import Xl, Element, Text, URI_XML, pretty_insert


########################################################################################################################
# TOC Section
########################################################################################################################
class _Toc(Toc):
    __doc__ = Toc.__doc__

    def __init__(self):
        Toc.__init__(self)

    def to_nav_element(self):
        default_ns = 'http://www.w3.org/1999/xhtml'
        epub_ns = 'http://www.idpf.org/2007/ops'

        html = Element((None, 'html'), prefixes={default_ns: None, epub_ns: 'epub'})

        head = Element((None, 'head'))
        html.children.append(head)

        if self.title:
            _title = Element((None, 'title'))
            head.children.append(_title)
            _title.children.append(Text(self.title))

        body = Element((None, 'body'))
        html.children.append(body)

        if self:
            nav = Element((None, 'nav'), prefixes={epub_ns: 'epub'}, attributes={(epub_ns, 'type'): 'toc'})
            ol = Element((None, 'ol'))

            for section in self:
                ol.children.append(section.to_nav_li_element())

            nav.children.append(ol)
            body.children.append(nav)

        return html

    def _before_add(self, key=None, item=None):
        if not isinstance(item, Section):
            raise TypeError


class _SubSections(List):
    __doc__ = _Toc.__doc__

    def _before_add(self, key=None, item=None):
        if not isinstance(item, Section):
            raise TypeError


class Section(epubuilder.epub2.epub2.Section):
    __doc__ = epubuilder.epub2.epub2.Section.__doc__

    def __init__(self, title, href=None):
        epubuilder.epub2.epub2.Section.__init__(self, title, href)

        self._subs = _SubSections()
        self._hidden_subs = None

    @property
    def hidden_subs(self):
        """bool: True for fold sub sections, False unfold.

        some reader just don't show sub sections when this is True,

        but I think it's mean FOLD sub sections and you can unfold it to show subs"""
        return self._hidden_subs

    @hidden_subs.setter
    def hidden_subs(self, value):
        if value not in (True, False):
            raise ValueError
        else:
            self._hidden_subs = value

    def to_nav_li_element(self):
        li = Element((None, 'li'))

        if self.href:
            a_or_span = Element((None, 'a'))
            a_or_span.attributes[(None, 'href')] = self.href
        else:
            a_or_span = Element((None, 'span'))

        a_or_span.children.append(Text(self.title))

        li.children.append(a_or_span)

        if self.subs:
            ol = Element((None, 'ol'))

            if self.hidden_subs:
                ol.attributes[(None, 'hidden')] = ''

            for one in self.subs:
                ol.children.append(one.to_nav_li_element())

            li.children.append(ol)

        return li


########################################################################################################################
# TOC Section
########################################################################################################################
class Epub3(Epub):
    def __init__(self):
        Epub.__init__(self)

        self._toc = _Toc()
        setattr(self._toc, '_epub', self)

        self._cover_path = None

    toc = property(lambda self: self._toc, doc=str(_Toc.__doc__ if _Toc.__doc__ else ''))

    @property
    def cover_path(self):
        """tag your file as a cover"""
        return self._cover_path

    @cover_path.setter
    def cover_path(self, path):
        if path is not None and path not in self.files.keys():
            raise ValueError()

        self._cover_path = path

    def _get_nav_xmlstring(self):
        html = self.toc.to_nav_element()
        return pretty_insert(html, dont_do_when_one_child=True).string()

    def _process_files_elements_properties(self, elements):
        new_elements = []
        for item in elements:
            properties = []

            if item.attributes[(None, 'media-type')] in (mimes.XHTML, mimes.HTML):

                try:
                    html_string = self.files[item.attributes[(None, 'href')]].binary.decode()
                except KeyError:
                    html_string = self._temp_files[item.attributes[(None, 'href')]].binary.decode()

                if _has_element('script', html_string):
                    properties.append('scripted')

                if _has_element('math', html_string):
                    properties.append('mathml')

            if properties:
                item.attributes[(None, 'properties')] = ' '.join(properties)

            new_elements.append(item)

        return new_elements

    def _get_opf_xmlstring(self, toc_path):

        def_ns = 'http://www.idpf.org/2007/opf'
        # dcterms_ns = 'http://purl.org/metadata/terms/'

        package = Element('package', prefixes={def_ns: None}, attributes={'version': '3.0'})

        package.attributes[(URI_XML, 'lang')] = 'en'

        for m in self.metadata:
            if isinstance(m, Identifier):
                package.attributes['unique-identifier'] = m.to_element().attributes[(None, 'id')]

        # unique - identifier = "pub-id"
        # metadata
        metadata_e = Element('metadata', prefixes={URI_DC: 'dc'})
        package.children.append(metadata_e)
        for m in self.metadata:
            metadata_e.children.append(m.to_element())

        modified = None
        for m in self.metadata:
            if isinstance(m, get('modified')):
                modified = m

        if not modified:
            metadata_e.children.append(get('modified')(w3c_utc_date()).to_element())

        # manifest
        manifest = Element('manifest')
        package.children.append(manifest)

        manifest.children.extend(self._process_files_elements_properties(self.files.to_elements()))

        for item in self._process_files_elements_properties(self._temp_files.to_elements()):

            if item.attributes[(None, 'href')] == toc_path:
                item.attributes[(None, 'properties')] = 'nav'

            if item.attributes[(None, 'href')] == self.cover_path:
                item.attributes[(None, 'properties')] = 'cover-image'

            manifest.children.append(item)

        # find ncx id for spine
        toc_ncx_item_e_id = self._find_ncx_id(manifest.children)

        # spine
        spine = self.spine.to_element()
        package.children.append(spine)
        spine.attributes['toc'] = toc_ncx_item_e_id

        return Xl(root=pretty_insert(package, dont_do_when_one_child=True)).string()

    def write(self, filename):

        z = zipfile.ZipFile(filename, 'w', compression=zipfile.ZIP_DEFLATED)

        z.writestr('mimetype', 'application/epub+zip'.encode('ascii'), compress_type=zipfile.ZIP_STORED)

        # wirte custom files
        for filename, _file in self.files.items():
            z.writestr(p.ROOT_OF_OPF + os.sep + filename, _file.binary, zipfile.ZIP_DEFLATED)

        # nav
        nav_xmlstring = self._get_nav_xmlstring()
        toc_nav_path = self._get_unused_filename(None, 'nav.xhtml')
        self._temp_files[toc_nav_path] = p.File(nav_xmlstring.encode(), mime='application/xhtml+xml')

        # ncx
        ncx_xmlstring = pretty_insert(self.toc.to_ncx_element(), dont_do_when_one_child=True).string()
        toc_ncx_filename = self._get_unused_filename(None, 'toc.ncx')
        self._temp_files[toc_ncx_filename] = p.File(ncx_xmlstring.encode(), mime='application/x-dtbncx+xml')

        # write nav nav's js and ncx
        for filename, _file in self._temp_files.items():
            z.writestr(p.ROOT_OF_OPF + os.sep + filename, _file.binary, zipfile.ZIP_DEFLATED)

        opf_filename = self._get_unused_filename(None, 'package.opf')
        z.writestr(p.ROOT_OF_OPF + '/' + opf_filename,
                   self._get_opf_xmlstring(toc_nav_path).encode(),
                   zipfile.ZIP_DEFLATED)

        z.writestr(p.CONTAINER_PATH,
                   self._get_container_xmlstring(p.ROOT_OF_OPF + '/' + opf_filename).encode(),
                   zipfile.ZIP_DEFLATED)

        self._temp_files.clear()
        z.close()

    write.__doc__ = p.Epub.write.__doc__

    def addons_make_user_toc_xhtml(self):
        """write this function because some EPUB reader not supports nav hidden attribute,
         they just ignor sub section, but not fold

        :returns: xhtml., other_paths
        :rtype: str, tuple
        """
        html = self.toc.to_nav_element()

        def find_element_by_name(tag):
            e = None
            for one in html.children:
                if one.tag == tag:
                    return one

            return e

        head = find_element_by_name((None, 'head'))
        body = find_element_by_name((None, 'body'))

        js_path = self._get_unused_filename(None, 'epubuilder_addons_user_toc_attach.js')
        self.files[js_path] = p.File(open(os.path.join(_dirt(__file__), 'static', 'a.js'), 'rb').read(),
                                     mime='text/javascript')

        head.children.append(Element('script', attributes={'src': js_path}))

        css_path = self._get_unused_filename(None, 'epubuilder_addons_user_toc_attach.css')
        self.files[css_path] = p.File(open(os.path.join(_dirt(__file__), 'static', 'a.css'), 'rb').read(),
                                      mime='text/style')

        head.children.append(Element('link', attributes={'rel': 'stylesheet', 'type': 'text/css', 'href': css_path}))

        script_before_body_close = Element('script', attributes={'type': 'text/javascript'})
        script_before_body_close.children.append(Text('set_button();'))
        body.children.append(script_before_body_close)

        user_toc_path = self._get_unused_filename(None, 'epubuilder_addons_user_toc.xhtml')
        self.files[user_toc_path] = p.File(pretty_insert(html).string().encode(), mime='application/xhtml+xml')

        return user_toc_path, (js_path, css_path)


def _has_element(tag, file_string):
    parser = html5lib.HTMLParser(tree=html5lib.getTreeBuilder('dom'))
    minidom_docment = parser.parse(file_string)

    if minidom_docment.getElementsByTagName(tag):
        return True
    else:
        return False


def _dirt(_file):
    return os.path.dirname(_file)
