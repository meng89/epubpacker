import zipfile

import html5lib
import os
from hooky import List

from epubuilder import mimes

import epubuilder.public.epub as p

from epubuilder.public.metas.dcmes import Identifier, URI_DC
from .metas.dcterms import get
from epubuilder.tools import w3c_utc_date
from epubuilder.xl import Xl, Header, Element, Text, URI_XML, pretty_insert

# 'cover-image', 'mathml', 'nav', 'remote-resources', 'scripted', 'svg', 'switch'


class Files(p.Files):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_elements(self):
        elements = []

        for item in super().to_elements():
            properties = []

            if item.attributes[(None, 'media-type')] in (mimes.XHTML, mimes.HTML):

                html_string = self[item.attributes[(None, 'href')]].binary.decode()

                if has_element('script', html_string):
                    properties.append('scripted')

                if has_element('math', html_string):
                    properties.append('mathml')

            if properties:
                item.attributes[(None, 'properties')] = ' '.join(properties)

            elements.append(item)

        return elements


###############################################################################
# TOC nav
###############################################################################
class _Toc(p.Toc):
    def __init__(self):
        super().__init__()

    def _before_add(self, key=None, item=None):
        if not isinstance(item, Section):
            raise TypeError


class _SubSections(List):
    __doc__ = _Toc.__doc__
    _before_add = getattr(_Toc, '_before_add')


class Section(p.Section):
    def __init__(self, title, href=None):
        super().__init__(title, href)

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
        li = Element('li')

        if self.href:
            a_or_span = Element((None, 'a'))
            a_or_span.attributes[(None, 'href')] = self.href
        else:
            a_or_span = Element((None, 'span'))

        a_or_span.children.append(Text(self.title))

        li.children.append(a_or_span)

        if self.subs:
            ol = Element('ol')

            if self.hidden_subs:
                ol.attributes[(None, 'hidden')] = ''

            for one in self.subs:
                ol.children.append(one.to_nav_li_element())

            li.children.append(ol)

        return li


class Epub3(p.Epub):
    def __init__(self):
        super().__init__()

        self._files = Files()

        # nav
        self._toc = _Toc()

        # for self.write()
        self._temp_files = Files()

    def _get_nav_element(self):
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
                ol.children.append(section.to_nav_li_element())

            nav.children.append(ol)
            body.children.append(nav)

        return html

    def _get_nav_xmlstring(self):
        html = self._get_nav_element()
        return pretty_insert(html, dont_do_when_one_child=True).string()

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

        manifest.children.extend(self.files.to_elements())

        for item in self._temp_files.to_elements():
            if item.attributes[(None, 'href')] == toc_path:
                item.attributes[(None, 'properties')] = 'nav'

            if item.attributes[(None, 'href')] == self.cover_path:
                item.attributes[(None, 'properties')] = 'cover-image'

            manifest.children.append(item)

        # find toc ncx id for spine
        toc_ncx_item_e_id = None
        for temp_file_e in self._temp_files.to_elements():
            if temp_file_e.attributes[(None, 'media-type')] == mimes.NCX:
                toc_ncx_item_e_id = temp_file_e.attributes[(None, 'id')]

        # spine
        spine = Element('spine')
        package.children.append(spine)

        spine.attributes['toc'] = toc_ncx_item_e_id

        for joint in self.spine:
            itemref = Element('itemref', attributes={(None, 'idref'): self.files[joint.path].identification})

            if joint.linear is True:
                itemref.attributes[(None, 'linear')] = 'yes'
            elif joint.linear is False:
                itemref.attributes[(None, 'linear')] = 'no'

            spine.children.append(itemref)

        x = Xl(header=Header(), root=pretty_insert(package, dont_do_when_one_child=True))
        return x.string()
        # return pretty_insert(package, dont_do_when_one_child=True).string()

    def write(self, filename):
        """write to file.

        :param filename: file name.
        :type filename: str
        """

        z = zipfile.ZipFile(filename, 'w', compression=zipfile.ZIP_DEFLATED)

        z.writestr('mimetype', 'application/epub+zip'.encode('ascii'), compress_type=zipfile.ZIP_STORED)

        # wirte custom files
        for filename, file in self.files.items():
            z.writestr(p.ROOT_OF_OPF + os.sep + filename, file.binary, zipfile.ZIP_DEFLATED)

        # nav
        nav_xmlstring = self._get_nav_xmlstring()
        toc_nav_path = self._get_unused_filename(None, 'nav.xhtml')
        self._temp_files[toc_nav_path] = p.File(nav_xmlstring.encode(), mime='application/xhtml+xml')

        # ncx
        ncx_xmlstring = self._get_ncx_xmlstring()
        toc_ncx_filename = self._get_unused_filename(None, 'toc.ncx')
        self._temp_files[toc_ncx_filename] = p.File(ncx_xmlstring.encode(), mime='application/x-dtbncx+xml')

        # write nav nav's js and ncx
        for filename, file in self._temp_files.items():
            z.writestr(p.ROOT_OF_OPF + os.sep + filename, file.binary, zipfile.ZIP_DEFLATED)

        opf_filename = self._get_unused_filename(None, 'package.opf')
        z.writestr(p.ROOT_OF_OPF + '/' + opf_filename,
                   self._get_opf_xmlstring(toc_nav_path).encode(),
                   zipfile.ZIP_DEFLATED)

        z.writestr(p.CONTAINER_PATH,
                   self._get_container_xmlstring(p.ROOT_OF_OPF + '/' + opf_filename).encode(),
                   zipfile.ZIP_DEFLATED)

        self._temp_files.clear()
        z.close()

    def addons_make_user_toc_xhtml(self):
        """write this function because some EPUB reader not supports nav hidden attribute,
         they just ignor sub section, but not fold

        :returns: xhtml., other_paths
        :rtype: str, tuple
        """
        html = self._get_nav_element()

        def find_element_by_name(name):
            e = None
            for one in html.children:
                if one.name == (None, name):
                    e = one
                    break
            return e

        head = find_element_by_name('head')
        body = find_element_by_name('body')

        js_path = self._get_unused_filename(None, 'epubuilder_addons_user_toc_attach.js')
        self.files[js_path] = p.File(open(os.path.join(dirt(__file__), 'static', 'a.js'), 'rb').read(),
                                     mime='text/javascript')

        head.children.append(Element('script', attributes={'src': js_path}))

        css_path = self._get_unused_filename(None, 'epubuilder_addons_user_toc_attach.css')
        self.files[css_path] = p.File(open(os.path.join(dirt(__file__), 'static', 'a.css'), 'rb').read(),
                                      mime='text/style')

        # 'type': 'text/css',
        head.children.append(Element('link', attributes={'rel': 'stylesheet', 'type': 'text/css', 'href': css_path}))

        script_before_body_close = Element('script', attributes={'type': 'text/javascript'})
        script_before_body_close.children.append(Text('set_button();'))
        body.children.append(script_before_body_close)

        user_toc_path = self._get_unused_filename(None, 'epubuilder_addons_user_toc.xhtml')
        self.files[user_toc_path] = p.File(pretty_insert(html).string().encode(), mime='application/xhtml+xml')

        return user_toc_path, (js_path, css_path)


def has_element(tag, file_string):
    parser = html5lib.HTMLParser(tree=html5lib.getTreeBuilder('dom'))
    minidom_docment = parser.parse(file_string)

    if minidom_docment.getElementsByTagName(tag):
        return True
    else:
        return False


def dirt(file):
    return os.path.dirname(file)
