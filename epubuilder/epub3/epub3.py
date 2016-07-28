# coding=utf-8
from __future__ import unicode_literals

import zipfile

import html5lib
import os
import io

from hooky import List

from epubuilder.public.epub import Toc

from epubuilder.public import File

import epubuilder.public.mimes as mimes

import epubuilder.public.epub as p

from epubuilder.public.epub import Epub

from epubuilder.public.metas.dcmes import URI_DC

from epubuilder.xl import Xl, Element, URI_XML, pretty_insert


########################################################################################################################
# TOC Section
########################################################################################################################
class _Toc(Toc):
    __doc__ = Toc.__doc__

    def __init__(self):
        super(_Toc, self).__init__()

    def _before_add(self, key=None, item=None):
        if not isinstance(item, p.Section):
            raise TypeError


class _SubSections(List):
    __doc__ = _Toc.__doc__

    def _before_add(self, key=None, item=None):
        if not isinstance(item, p.Section):
            raise TypeError


class Section(p.Section):
    __doc__ = p.Section.__doc__

    def __init__(self, title, href=None):
        super(Section, self).__init__(title, href)

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

        a_or_span.children.append(self.title)

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
# Epub3
########################################################################################################################

XML_URI = 'http://www.w3.org/1999/xhtml'
OPS_URI = 'http://www.idpf.org/2007/ops'


class Epub3(Epub):

    def __init__(self):
        Epub.__init__(self)

        self._toc = _Toc()
        setattr(self._toc, '_epub', self)

        self._cover_image = None

    toc = property(lambda self: self._toc, doc=str(_Toc.__doc__ if _Toc.__doc__ else ''))

    @property
    def cover_image(self):
        """Tag your cover image path as a cover"""
        return self._cover_image

    @cover_image.setter
    def cover_image(self, path):
        if path is not None and path not in self.files.keys():
            raise ValueError()

        self._cover_image = path

    def _make_metadata_element(self):
        """
        :return: Metadata element
        :rtype: Element
        """
        metadata = Element('metadata', prefixes={URI_DC: 'dc'})
        for m in self.metadata:
            metadata.children.append(m.to_element())

        return metadata

    def _make_nav_element(self):
        """
        :return: Nav html element
        :rtype: Element
        """

        html = Element((None, 'html'), prefixes={XML_URI: None, OPS_URI: 'epub'})

        head = Element((None, 'head'))
        html.children.append(head)

        if self.toc.title:
            _title = Element((None, 'title'))
            head.children.append(_title)
            _title.children.append(self.toc.title)

        body = Element((None, 'body'))
        html.children.append(body)

        if self.toc:
            nav = Element((None, 'nav'), prefixes={OPS_URI: 'epub'}, attributes={(OPS_URI, 'type'): 'toc'})
            ol = Element((None, 'ol'))

            for section in self.toc:
                ol.children.append(section.to_nav_li_element())

            nav.children.append(ol)
            body.children.append(nav)

        return html
        # return pretty_insert(html, dont_do_when_one_child=True).string()

    def _process_items_properties(self, manifest):
        for item in manifest.children:
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

    def _get_opf_xmlstring(self, toc_path):

        package = Element('package', prefixes={p.OPF_NS: None}, attributes={'version': '3.0'})

        package.attributes[(URI_XML, 'lang')] = 'en'

        # unique - identifier = "pub-id"
        if self._find_unique_id():
            package.attributes['unique-identifier'] = self._find_unique_id()

        # Metadata
        package.children.append(self._make_metadata_element())

        # manifest
        manifest = self._make_manifest_element()
        package.children.append(manifest)
        self._process_items_properties(manifest)

        for item in manifest.children:
            if item.attributes[(None, 'href')] == toc_path:
                item.attributes[(None, 'properties')] = 'nav'

            if item.attributes[(None, 'href')] == self.cover_image:
                item.attributes[(None, 'properties')] = 'cover-image'

        # Find ncx id for spine
        toc_ncx_item_e_id = self._find_ncx_id(manifest.children)

        # Spine
        spine = self._make_spine_element()
        package.children.append(spine)
        spine.attributes['toc'] = toc_ncx_item_e_id

        return Xl(root=pretty_insert(package, dont_do_when_one_child=True)).string()

    def write(self, filename):

        # put nav to temp files
        nav_xmlstring = pretty_insert(self._make_nav_element(), dont_do_when_one_child=True).string()
        toc_nav_path = self._get_unused_filename(None, 'nav.xhtml')
        self._temp_files[toc_nav_path] = p.File(nav_xmlstring.encode(), mime='application/xhtml+xml')

        # put ncx to temp files
        ncx_xmlstring = pretty_insert(self._make_ncx_element(), dont_do_when_one_child=True).string()
        toc_ncx_filename = self._get_unused_filename(None, 'toc.ncx')
        self._temp_files[toc_ncx_filename] = p.File(ncx_xmlstring.encode(), mime='application/x-dtbncx+xml')

        # get opf name & data
        opf_data = self._get_opf_xmlstring(toc_nav_path).encode()
        opf_filename = self._get_unused_filename(None, 'package.opf')

        # get container data
        container_data = self._get_container_xmlstring(p.ROOT_OF_OPF + '/' + opf_filename).encode()

        # make zipfile
        z = zipfile.ZipFile(filename, 'w', compression=zipfile.ZIP_DEFLATED)

        # write mimetype as first file in zip
        z.writestr('mimetype', 'application/epub+zip'.encode('ascii'), compress_type=zipfile.ZIP_STORED)

        # wirte files
        for filename, _file in self.files.items():
            z.writestr(p.ROOT_OF_OPF + os.sep + filename, _file.binary, zipfile.ZIP_DEFLATED)

        # write temp files
        for filename, _file in self._temp_files.items():
            z.writestr(p.ROOT_OF_OPF + os.sep + filename, _file.binary, zipfile.ZIP_DEFLATED)

        # write opf data
        z.writestr(p.ROOT_OF_OPF + '/' + opf_filename, opf_data, zipfile.ZIP_DEFLATED)

        # write container
        z.writestr(p.CONTAINER_PATH, container_data, zipfile.ZIP_DEFLATED)

        z.close()

        self._temp_files.clear()

    write.__doc__ = p.Epub.write.__doc__

    ####################################################################################################################
    # Add-ons
    def addons_make_toc_page(self):
        """Some EPUB reader not supports nav hidden attribute, they just ignor sub section, not fold.
        So, this member function can make a toc page, with it's little JS code, it can fold and unfold sections.

        You must put the returned file to Epub3.files by yourself.

        :returns: xhtml page file
        :rtype: File
        """

        html = self._make_nav_element()

        def find_element_by_name(tag):
            e = None
            for one in html.children:
                if one.tag == tag:
                    return one

            return e

        head = find_element_by_name((None, 'head'))
        body = find_element_by_name((None, 'body'))

        css_string = open(os.path.join(_dirt(__file__), 'static', 'a.css')).read()
        css = Element('style', attributes={'type': 'text/css'})
        css.children.append(css_string)

        head.children.append(css)

        js_string = io.open(os.path.join(_dirt(__file__), 'static', 'a.js'), encoding='utf-8').read()
        script = Element('script')
        script.children.append(js_string)

        head.children.append(script)

        script_before_body_close = Element('script', attributes={'type': 'text/javascript'})
        script_before_body_close.children.append('set_button();')
        body.children.append(script_before_body_close)

        toc_page = pretty_insert(html).string().encode()
        return File(toc_page)


def _has_element(tag, file_string):
    parser = html5lib.HTMLParser(tree=html5lib.getTreeBuilder('dom'))
    minidom_docment = parser.parse(file_string)

    if minidom_docment.getElementsByTagName(tag):
        return True
    else:
        return False


def _dirt(_file):
    return os.path.dirname(_file)
