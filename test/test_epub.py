import uuid

from epubuilder.epub import epub, File, Section, Joint

from epubuilder.epub.metadata.dcmes import Title, Language, Identifier

from epubuilder.epub.metadata.meta.dcterms import get_class

from epubuilder.tools import w3c_utc_date

from epubuilder import xl

xhtml_template = """
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>{}</title></head>
<body>{}</body></html>
"""


def test_simple_epub():
    book = epub.Epub()

    def make_page(title, html_path=None, content=None):
        if html_path and content:
            p = File(xhtml_template.format(title, content), mime='application/xhtml+xml')
            book.files[html_path] = p

            book.spine.append(Joint(html_path))

        sec = Section(title, href=html_path)
        return sec

    sec1 = make_page('Part I', 'Part_I.xhtml',  content='This is Part I content')
    sec1_1 = make_page('Chapter 1', 'pi_c1.xhtml', content='This is Chapter 1 content')
    sec1_2 = make_page('Chapter 2', 'pi_c2.xhtml', content='This is Chapter 2 content')
    sec1.hidden_sub = True
    sec1.subsections.extend([sec1_1, sec1_2])

    sec2 = make_page('Part II')
    sec2_1 = make_page('Chapter 1', 'pii_c1.xhtml', content='This is Chapter 1 content')
    sec2_2 = make_page('Chapter 2', 'pii_c2.xhtml', content='This is Chapter 2 content')
    sec2.subsections.extend([sec2_1, sec2_2])

    sec3 = make_page('Part III', 'Part_III.xhtml', content='This is Part III content')
    sec3_1 = make_page('Chapter 1', 'piii_c1.xhtml', content='This is Chapter 1 content')
    sec3_2 = make_page('Chapter 2', 'piii_c2.xhtml', content='This is Chapter 2 content')
    sec3.subsections.extend([sec3_1, sec3_2])

    book.toc.extend([sec1, sec2, sec3])

    book.toc.add_js_for_nav_flod = True

    book.metadata.append(Title('EPUB demo'))
    book.metadata.append(Language('en'))
    book.metadata.append(Identifier('identifier_' + uuid.uuid4().hex))
    book.metadata.append(get_class('modified')(w3c_utc_date()))

    user_toc_path, other_paths = book.addons_make_user_toc()

    book.spine.insert(0, Joint(user_toc_path))

    book.toc.insert(0, Section('Table of Contents', href=user_toc_path))

    book.write('demo.epub')

    print(xl.pretty_insert(sec1.to_toc_element(), dont_do_when_one_child=False).string())

