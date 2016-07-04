#!/usr/bin/env python3
import os
import uuid

from epubuilder.public import Joint, File

from epubuilder.public.metas.dcmes import Title, Language, Identifier

from epubuilder.epub3 import Epub3, Section


script_dir = cur_path = os.path.dirname(__file__)

xhtml_template = """
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>{title}</title>
    </head>
    <body>
        <p>{content}</p>
    </body>
</html>
"""


book = Epub3()


# set book's metadata
book.metadata.append(Title('EPUB 3 sample book'))
book.metadata.append(Language('en'))
book.metadata.append(Identifier('identifier_' + uuid.uuid4().hex))


# add a file
file_1 = File(xhtml_template.format(title='chapter I', content='This is chapter i').encode())
path_1 = '1.xhtml'
book.files[path_1] = file_1


# add to book's spine
book.spine.append(Joint(file_1))


# add to books's table of contents
chapter1 = Section(title='Chapter I', href=path_1)
book.toc.append(chapter1)


# other files
file_1_1 = File(xhtml_template.format(title='Section 1', content='This is section 1').encode())
path_1_1 = '1.1.xhtml'
book.files[path_1_1] = file_1_1
book.spine.append(Joint(file_1_1))


# add sub sections to chapter1
chapter1.subs.append(Section('Section 1', href=path_1_1))


# set book's cover image
cover_image = File(open(os.path.join(script_dir, 'cover.png'), 'rb').read())
book.files['cover.png'] = cover_image
book.cover_path = 'cover.png'


book.write('sample_3.epub')
