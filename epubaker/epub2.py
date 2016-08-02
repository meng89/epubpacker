# coding=utf-8

import os
import zipfile


from epubaker.epub import Epub, File, OPF_NS, ROOT_OF_OPF, CONTAINER_PATH

from epubaker.metas.dcmes import URI_DC

from epubaker.metas.epub2_meta import Cover

from epubaker.xl import Xl, Element, pretty_insert


class Epub2(Epub):
    def __init__(self):
        Epub.__init__(self)

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

        package = Element('package', prefixes={OPF_NS: None}, attributes={'version': '2.0'})

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

        # put ncx to temp files
        ncx_xmlstring = pretty_insert(self._make_ncx_element(), dont_do_when_one_child=True).string()
        toc_ncx_filename = self._get_unused_filename(None, 'toc.ncx')
        self._temp_files[toc_ncx_filename] = File(ncx_xmlstring.encode(), mime='application/x-dtbncx+xml')

        # get opf name & data
        opf_data = self._get_opf_xmlstring().encode()
        opf_filename = self._get_unused_filename(None, 'package.opf')

        # get container data
        container_data = self._get_container_xmlstring(ROOT_OF_OPF + '/' + opf_filename).encode()

        # make zip file
        z = zipfile.ZipFile(filename, 'w', compression=zipfile.ZIP_DEFLATED)

        # write mimetype as first file in zip
        z.writestr('mimetype', 'application/epub+zip'.encode('ascii'), compress_type=zipfile.ZIP_STORED)

        # wirte custom files
        for filename, fil in self.files.items():
            z.writestr(ROOT_OF_OPF + os.sep + filename, fil.binary, zipfile.ZIP_DEFLATED)

        # write temp files
        for filename, fil in self._temp_files.items():
            z.writestr(ROOT_OF_OPF + os.sep + filename, fil.binary, zipfile.ZIP_DEFLATED)

        # write opf data
        z.writestr(ROOT_OF_OPF + '/' + opf_filename, opf_data, zipfile.ZIP_DEFLATED)

        # write container
        z.writestr(CONTAINER_PATH, container_data, zipfile.ZIP_DEFLATED)

        z.close()

        self._temp_files.clear()

    write.__doc__ = Epub.write.__doc__
