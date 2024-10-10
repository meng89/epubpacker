import posixpath
import zipfile
import datetime

import xl

__version__ = '2.0.2'


def _path2id(s):
    news = ""
    for c in s:
        if c == "_":
            news += "__"
        elif c == "/":
            news += "_s_"
        else:
            news += c
    return news


ROOT_OF_OPF = 'OEBPS'

USER_DIR = "user_dir"


class Epub(object):
    def __init__(self):
        self.cover_img_path = None
        self.meta = Meta()
        self.userfiles = {}
        self.toc_title = None
        self.root_toc = []
        self.spine = []


    def write(self, filename):
        if not self.userfiles:
            raise EpubError

        z = zipfile.ZipFile(filename, 'w', compression=zipfile.ZIP_DEFLATED)
        z.writestr('mimetype', 'application/epub+zip'.encode('ascii'), compress_type=zipfile.ZIP_STORED)

########################################################################################################################
        nav_html = xl.Element("html", {"xmlns:epub": "http://www.idpf.org/2007/ops",
                                       "xmlns": "http://www.w3.org/1999/xhtml",
                                       "xml:lang": self.meta.languages[0]
                                       })
        head = nav_html.ekid("head")
        title_text = self.toc_title or "Table of contents"
        _title = head.ekid("title", kids=[title_text])
        body = nav_html.ekid("body")
        nav = body.ekid("nav", {"epub:type": "toc"})
        _h1 = nav.ekid("h1", kids=[title_text])
        ol = nav.ekid("ol")
        for toc in self.root_toc:
            toc.to_et(ol)

        name = "toc.xhtml"
        i = 1
        toc_xhtml = name
        while toc_xhtml in z.namelist():
            toc_xhtml = "real" + str(i) + name
            i += 1

        z.writestr(posixpath.join(ROOT_OF_OPF, toc_xhtml),
                   xl.Xml(root=nav_html).to_str(do_pretty=True, dont_do_tags=["a"]))


########################################################################################################################

        dc_id_id = "ididid"
        _package = xl.Element("package", {"version": "3.0",
                                          "unique-identifier": dc_id_id,
                                          "xml:lang": self.meta.languages[0],
                                          "xmlns": "http://www.idpf.org/2007/opf"})

        self.meta.to_et(_package, dc_id_id)

        manifest = _package.ekid("manifest")

        _toc_item = manifest.ekid("item", {"media-type": "application/xhtml+xml",
                                              "href": toc_xhtml,
                                              "id": _path2id(toc_xhtml),
                                              "properties": "nav"
                                              })
        for filename in self.userfiles.keys():
            attrib = {}
            _, ext = posixpath.splitext(filename)
            if ext.lower() == ".xhtml":
                media_type = "application/xhtml+xml"

                xml = xl.parse(self.userfiles[filename])
                if xml.root.find_kids("script"):
                    attrib["properties"] = "scripted"
            elif ext.lower() == ".css":
                media_type = "text/css"
            elif ext.lower() == ".js":
                media_type = "text/javascript"
            elif ext.lower() == ".png":
                media_type = "image/png"
            else:
                raise EpubError(ext)

            attrib.update(
                {"media-type": media_type,
                 "href": posixpath.join(USER_DIR, filename),
                 "id": _path2id(filename)
                 }
            )

            if filename == self.cover_img_path:
                if "properties" in attrib.keys():
                    attrib["properties"] = attrib["properties"] + " cover-image"
                else:
                    attrib["properties"] = "cover-image"

            _item = manifest.ekid("item", attrib)

        spine = _package.ekid("spine")
        for one in self.spine:
            spine.ekid("itemref", {"idref": _path2id(one)})

        name = "package.opf"
        i = 1
        package_opf_path = posixpath.join(ROOT_OF_OPF, name)
        while package_opf_path in z.namelist():
            package_opf_path = "real" + str(i) + name
            i += 1

        z.writestr(package_opf_path, xl.Xml(root=_package).to_str(do_pretty=True))


########################################################################################################################

        for filename, data in self.userfiles.items():
            z.writestr(posixpath.join(ROOT_OF_OPF, USER_DIR, filename), data)

########################################################################################################################

        _container = xl.Element("container", {"version": "1.0",
                                              "xmlns": "urn:oasis:names:tc:opendocument:xmlns:container"})
        _rootfiles = _container.ekid("rootfiles")
        _rootfile = _rootfiles.ekid("rootfile", {"media-type": "application/oebps-package+xml",
                                                    "full-path": posixpath.join(ROOT_OF_OPF, "package.opf")})
        z.writestr("META-INF/container.xml", xl.Xml(root=_container).to_str(do_pretty=True))


class Meta(object):
    def __init__(self):
        self.identifier = ""
        self.titles = []
        self.languages = []
        self.creators = []
        self.date = ""
        self.others = []

    def to_et(self, parent: xl.Element, dc_id_id):
        metadata = parent.ekid("metadata", {"xmlns:dc": "http://purl.org/dc/elements/1.1/"})
        _meta = metadata.ekid(
                       "meta",
                       {"property": "dcterms:modified"},
                       [datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")])
        if self.identifier:
            _dc_id = metadata.ekid("dc:identifier", {"id": dc_id_id}, [self.identifier])
        for title in self.titles:
            _title = metadata.ekid("dc:title", kids=[title])
        for lang in self.languages:
            _lang = metadata.ekid("dc:language", kids=[lang])
        for creator in self.creators:
            _creator = metadata.ekid("dc:creator", kids=[creator])
        if self.date:
            _date = metadata.ekid("dc:date", kids=[self.date])

        for other in self.others:
            if not isinstance(other, xl.Element):
                raise TypeError(other)
            metadata.kids.append(other)


class Toc(object):
    def __init__(self, title, href=None):
        self.title = title
        self.href = href
        self.kids = []

    def to_et(self, parent):
        li = parent.ekid("li")
        try:
            li.ekid("a", {"href": posixpath.normpath(posixpath.join(USER_DIR, self.href))}, [self.title])
        except TypeError:
            raise TypeError(self.title, self.href)
        if self.kids:
            ol = li.ekid("ol")
            for kid in self.kids:
                kid.to_et(ol)


class Vertebrae(object):
    def __init__(self, path):
        self.path = path


class EpubError(Exception):
    pass
