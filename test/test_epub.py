import uuid
import os

from epubuilder.public import Joint, File

from epubuilder.public.metas.dcmes import Title, Language, Identifier

xhtml_template = """
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>{title}</title>
</head>
<body><p>{content}</p></body></html>
"""

cur_path = os.path.dirname(__file__)


def make_epub(epub, section):
    book = epub()

    # metadata
    book.metadata.append(Title('EPUB demo'))
    book.metadata.append(Language('en'))
    book.metadata.append(Identifier('identifier_' + uuid.uuid4().hex))

    # book.metadata.append(get('modified')(w3c_utc_date()))

    def make_page(title, html_path=None, content=None):
        if html_path and content:
            file = File(xhtml_template.format(title=title, content=content).encode(), mime='application/xhtml+xml')
            book.files[html_path] = file

            book.spine.append(Joint(html_path))

        sec = section(title, href=html_path)
        return sec

    sec1 = make_page('Part I', 'Part_I.xhtml',  content='This is Part I content')
    sec1_1 = make_page('Chapter 1', 'pi_c1.xhtml', content='This is Chapter 1 content')
    sec1_2 = make_page('Chapter 2', 'pi_c2.xhtml', content='This is Chapter 2 content')
    sec1.hidden_subs = True
    sec1.subs.extend([sec1_1, sec1_2])

    sec2 = make_page('Part II')
    sec2_1 = make_page('Chapter 1', 'pii_c1.xhtml', content='This is Chapter 1 content')
    sec2_2 = make_page('Chapter 2', 'pii_c2.xhtml', content='This is Chapter 2 content')
    sec2.subs.extend([sec2_1, sec2_2])

    sec3 = make_page('Part III', 'Part_III.xhtml', content='This is Part III content')
    sec3_1 = make_page('Chapter 1', 'piii_c1.xhtml', content='This is Chapter 1 content')
    sec3_2 = make_page('Chapter 2', 'piii_c2.xhtml', content='This is Chapter 2 content')
    sec3.subs.extend([sec3_1, sec3_2])

    book.toc.extend([sec1, sec2, sec3])

    return book


def write_epub(book, filename):
    dirt = '_built_book'
    os.makedirs(dirt, exist_ok=True)
    book.write(os.path.join(dirt, filename))


def test_epub3():
    from epubuilder.epub3 import Epub3, Section

    book = make_epub(Epub3, Section)
    book.files['cover.png'] = File(open(os.path.join(cur_path, 'cover', 'cover.png'), 'rb').read())
    book.cover_path = 'cover.png'

    # make user toc
    user_toc_path, other_paths = book.addons_make_user_toc_xhtml()
    book.spine.insert(0, Joint(user_toc_path))
    book.toc.insert(0, Section('Table of Contents', href=user_toc_path))

    write_epub(book, '3.epub')


def test_epub2():
    from epubuilder.epub2 import Epub2, Section
    from epubuilder.epub2.metas import Cover

    book = make_epub(Epub2, Section)

    cover_file = File(open(os.path.join(cur_path, 'cover', 'cover.png'), 'rb').read())
    book.files['cover.png'] = cover_file
    book.metadata.append(Cover(cover_file))

    cover_page_path = 'cover.xhtml'
    book.make_cover_page(image_path='cover.png', cover_page_path=cover_page_path)

    book.spine.insert(0, Joint(cover_page_path))

    book.toc.ncx_depth = 1

    write_epub(book, '2.epub')
