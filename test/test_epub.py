import uuid

from epubuilder.epub import epub, File, Section, Itemref

from epubuilder.epub.metadata.dcmes import Title, Language, Identifier

from epubuilder.epub.metadata.meta.dcterms import get_class

from epubuilder.tools import w3c_utc_date


def test_simple_epub():
    book = epub.Epub()

    p1_path = 'html/p1.html'

    page1 = File(b"""<html xmlns="http://www.w3.org/1999/xhtml"><body><p>hello wrold</p></body></html>""")

    book.files[p1_path] = page1

    book.spine.append(Itemref(page1.identification))

    book.toc.append(Section('P1', href=p1_path))

    book.metadata.append(Title('EPUB demo'))
    book.metadata.append(Language('en'))
    book.metadata.append(Identifier(uuid.uuid4().hex))
    book.metadata.append(get_class('modified')(w3c_utc_date()))

    book.write('demo.epub')
