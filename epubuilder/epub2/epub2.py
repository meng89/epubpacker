import uuid
import zipfile

import io
import os
from PIL import Image
from hooky import List

import epubuilder.public.epub as p
from epubuilder.public.epub import Toc
from epubuilder.public.metas.dcmes import Identifier, URI_DC
from epubuilder.tools import relative_path
from epubuilder.xl import Xl, Header, Element, pretty_insert, Text


class _Toc(Toc):
    def _before_add(self, key=None, item=None):
        if not isinstance(item, Section):
            raise TypeError


class _SubSections(List):
    __doc__ = _Toc.__doc__
    _before_add = getattr(_Toc, '_before_add')


class Section:
    """
    store title, href and sub :class:`Section` objects.
    """
    def __init__(self, title, href=None):
        """
        :param title: title of content.
        :type title: str
        :param href: html link to a file path in :class:`Epub.files`, can have a bookmark. example: `text/a.html#hello`
        :type href: str
        """
        self._title = title
        self._href = href
        self._subs = _SubSections()

    @property
    def title(self):
        """as class parameter"""
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def href(self):
        """ as class parmeter"""
        return self._href

    @href.setter
    def href(self, value):
        self._href = value

    @property
    def subs(self):
        return self._subs

    def to_toc_ncx_element(self):
        nav_point = Element('navPoint', attributes={'id': 'id_' + uuid.uuid4().hex})

        nav_label = Element('navLabel')
        nav_point.children.append(nav_label)

        text = Element('text')
        nav_label.children.append(text)

        text.children.append(Text(self.title))

        content = Element('content')
        nav_point.children.append(content)

        first_sub = None
        for subsection in self.subs:
            sub = subsection.to_toc_ncx_element()
            nav_point.children.append(sub)

            first_sub = first_sub or sub

        if self.href:
            content.attributes[(None, 'src')] = self.href

        elif first_sub:
            content.attributes[(None, 'src')] = first_sub.children[1].attributes[(None, 'src')]

        return nav_point


class Epub(p.Epub):
    def __init__(self):
        super().__init__()

        self._toc = _Toc()

        self._cover_path = None

        # for self.write()
        self._temp_files = p.Files()

    toc = property(lambda self: self._toc, doc=str(_Toc.__doc__ if _Toc.__doc__ else ''))

    def _get_opf_xmlstring(self):

        def_ns = 'http://www.idpf.org/2007/opf'
        # dcterms_ns = 'http://purl.org/metadata/terms/'

        package = Element('package', prefixes={def_ns: None}, attributes={'version': '2.0'})

        # unique - identifier = "pub-id"
        for m in self.metadata:
            if isinstance(m, Identifier):
                package.attributes['unique-identifier'] = m.to_element().attributes[(None, 'id')]

        # metadata
        metadata_e = Element('metadata', prefixes={URI_DC: 'dc'})
        package.children.append(metadata_e)
        for m in self.metadata:
            metadata_e.children.append(m.to_element())

        # manifest
        manifest = Element('manifest')
        package.children.append(manifest)

        manifest.children.extend(self.files.to_elements())

        manifest.children.extend(self._temp_files.to_elements())

        # find ncx id for spine
        toc_ncx_item_e_id = self._find_ncx_id(manifest.children)

        # spine
        spine = self.spine.to_element()
        package.children.append(spine)
        spine.attributes['toc'] = toc_ncx_item_e_id

        x = Xl(header=Header(), root=pretty_insert(package, dont_do_when_one_child=True))
        return x.string()
        # return pretty_insert(package, dont_do_when_one_child=True).string()

    def write(self, filename):

        z = zipfile.ZipFile(filename, 'w', compression=zipfile.ZIP_DEFLATED)

        z.writestr('mimetype', 'application/epub+zip'.encode('ascii'), compress_type=zipfile.ZIP_STORED)

        # wirte custom files
        for filename, file in self.files.items():
            z.writestr(p.ROOT_OF_OPF + os.sep + filename, file.binary, zipfile.ZIP_DEFLATED)

        # ncx
        ncx_xmlstring = self.toc.to_ncx_element()
        toc_ncx_filename = self._get_unused_filename(None, 'toc.ncx')
        self._temp_files[toc_ncx_filename] = p.File(ncx_xmlstring.encode(), mime='application/x-dtbncx+xml')

        # write nav nav's js and ncx
        for filename, file in self._temp_files.items():
            z.writestr(p.ROOT_OF_OPF + os.sep + filename, file.binary, zipfile.ZIP_DEFLATED)

        opf_filename = self._get_unused_filename(None, 'package.opf')
        z.writestr(p.ROOT_OF_OPF + '/' + opf_filename,
                   self._get_opf_xmlstring().encode(),
                   zipfile.ZIP_DEFLATED)

        z.writestr(p.CONTAINER_PATH,
                   self._get_container_xmlstring(p.ROOT_OF_OPF + '/' + opf_filename).encode(),
                   zipfile.ZIP_DEFLATED)

        self._temp_files.clear()
        z.close()

    write.__doc__ = p.Epub.write.__doc__

    def make_cover_page(self, image_path, cover_page_path=None, width=None, heigth=None):
        if cover_page_path:
            if cover_page_path in self.files.keys():
                raise FileExistsError
        else:
            cover_page_path or self._get_unused_filename(None, 'cover.xhtml')

        img = Image.open(io.BytesIO(self.files[image_path].binary))
        width = width or img.size[0]
        height = heigth or img.size[1]

        relative = relative_path(os.path.split(cover_page_path)[0], image_path)

        xhtml_string = open(os.path.join(os.path.dirname(__file__), 'static', 'cover.xhtml')).read()
        page_string = xhtml_string.format(title='Cover', width=width, height=height, image_href=relative)
        self.files[cover_page_path] = p.File(page_string.encode())

        return cover_page_path
