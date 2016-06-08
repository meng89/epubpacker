from epubuilder.epub import epub, File

from epubuilder.epub.metadata.dcmes import Title, Language, Identifier

from epubuilder.epub.metadata.meta.dcterms import get_class

import uuid

book = epub.Epub()

book.files['html/hi.html'] = File(b"""<html><body><p>hello wrold</p></body></html>""")

book.spine

book.toc

book.metadata.append(Title('EPUB demo'))
book.metadata.append(Language('en'))
book.metadata.append(Identifier(uuid.uuid4().hex))
book.metadata.append(get_class(''))
