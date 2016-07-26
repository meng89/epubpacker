# coding=utf-8

import zipfile
import os

import epubuilder.public.epub as p
from epubuilder.public.epub import Epub, Toc
from epubuilder.public.metas.dcmes import URI_DC

from epubuilder.epub2.metas import Cover


from epubuilder.xl import Xl, Element, pretty_insert


########################################################################################################################
# Epub2
########################################################################################################################
class Epub2(Epub):
    def __init__(self):
        Epub.__init__(self)

        self._toc = Toc()
        setattr(self._toc, '_epub', self)

    toc = property(lambda self: self._toc, doc=str(Toc.__doc__ if Toc.__doc__ else ''))

    def _make_metadata_element(self):
        """
        :return: Metadata Element
        :rtype: Element
        """
        metadata = Element('metadata', prefixes={URI_DC: 'dc'})

        for m in self.metadata:
            if isinstance(m, Cover):
                cover = Element('meta', attributes={'name': 'cover', 'content': self._find_id(m.filepath)})
                metadata.children.append(cover)
            else:
                metadata.children.append(m.to_element())

        return metadata

    def _get_opf_xmlstring(self):

        def_ns = 'http://www.idpf.org/2007/opf'

        package = Element('package', prefixes={def_ns: None}, attributes={'version': '2.0'})

        # unique - identifier = "pub-id"
        if self._find_unique_id():
            package.attributes['unique-identifier'] = self._find_unique_id()

        # Metadata
        package.children.append(self._make_metadata_element())

        # Manifest
        manifest = self._make_manifest_element()
        package.children.append(manifest)

        # Find ncx id for spine
        toc_ncx_item_e_id = self._find_ncx_id(manifest.children)

        # Spine
        spine = self._make_spine_element()
        package.children.append(spine)
        spine.attributes['toc'] = toc_ncx_item_e_id

        return Xl(root=pretty_insert(package, dont_do_when_one_child=True)).string()

    def write(self, filename):

        z = zipfile.ZipFile(filename, 'w', compression=zipfile.ZIP_DEFLATED)

        z.writestr('mimetype', 'application/epub+zip'.encode('ascii'), compress_type=zipfile.ZIP_STORED)

        # wirte custom files
        for filename, fil in self.files.items():
            z.writestr(p.ROOT_OF_OPF + os.sep + filename, fil.binary, zipfile.ZIP_DEFLATED)

        # ncx
        ncx_xmlstring = pretty_insert(self.toc.to_ncx_element(), dont_do_when_one_child=True).string()
        toc_ncx_filename = self._get_unused_filename(None, 'toc.ncx')
        self._temp_files[toc_ncx_filename] = p.File(ncx_xmlstring.encode(), mime='application/x-dtbncx+xml')

        # write nav nav's js and ncx
        for filename, fil in self._temp_files.items():
            z.writestr(p.ROOT_OF_OPF + os.sep + filename, fil.binary, zipfile.ZIP_DEFLATED)

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
