import zipfile
import os
import io

from PIL import Image


import epubuilder.public.epub as p

from epubuilder.public.meta.dcmes import Identifier, URI_DC

from epubuilder.xl import Xl, Header, Element, pretty_insert

from epubuilder import mimes

from epubuilder.tools import relative_path


class Epub2(p.Epub):
    def __init__(self):
        super().__init__()

        self._cover_path = None

        # for self.write()
        self._temp_files = p.Files()

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

        z = zipfile.ZipFile(filename, 'w', compression=zipfile.ZIP_DEFLATED)

        z.writestr('mimetype', 'application/epub+zip'.encode('ascii'), compress_type=zipfile.ZIP_STORED)

        # wirte custom files
        for filename, file in self.files.items():
            z.writestr(p.ROOT_OF_OPF + os.sep + filename, file.binary, zipfile.ZIP_DEFLATED)

        # ncx
        ncx_xmlstring = self._get_ncx_xmlstring()
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

    def make_cover_page(self, image_path, cover_page_path=None, width=None, heigth=None):
        if cover_page_path:
            if cover_page_path in self.files.keys():
                raise FileExistsError
        else:
            cover_page_path or self._get_unused_filename(None, 'cover.xhtml')

        img = Image.open(io.BytesIO(self.files[image_path]))
        width = width or img.size[0]
        heigth = heigth or img.size[1]

        page_string = open(os.path.join(os.path.dirname(__file__), 'static')).read().format(title='Cover',
                                                                                            width=width,
                                                                                            heigth=heigth,
                                                                                            )
