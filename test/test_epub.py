import uuid

from epubuilder.epub import epub, File, Section, Itemref

from epubuilder.epub.metadata.dcmes import Title, Language, Identifier

from epubuilder.epub.metadata.meta.dcterms import get_class

from epubuilder.tools import w3c_utc_date

import xl

xhtml_template = """
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>{}</title></head>
<body>{}</body></html>
"""


def test_simple_epub():
    book = epub.Epub()

    p1_path = 'p1.xhtml'
    p1 = File(xhtml_template.format('p1 title', 'p1 text'), mime='application/xhtml+xml')
    book.files[p1_path] = p1
    book.spine.append(Itemref(p1.identification))
    sec1 = Section('P1', href=p1_path)
    sec1.hidden_sub = True

    p1_1_path = 'p1_1.xhtml'
    p1_1 = File(xhtml_template.format('p1_1 title', 'p1_1 text'), mime='application/xhtml+xml')
    book.files[p1_1_path] = p1_1
    book.spine.append(Itemref(p1_1.identification))
    sec1_1 = Section('P1_1', href=p1_1_path)

    sec1.subsections.append(sec1_1)

    book.toc.append(sec1)

    book.toc.add_js_for_nav_flod = True

    book.metadata.append(Title('EPUB demo'))
    book.metadata.append(Language('en'))
    book.metadata.append(Identifier(uuid.uuid4().hex))
    book.metadata.append(get_class('modified')(w3c_utc_date()))

    book.write('demo.epub')

    print(xl.pretty_insert(sec1.to_toc_element(), dont_do_when_one_child=False).xml_string())
