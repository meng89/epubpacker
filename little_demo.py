import uuid

from epubuilder.epub3 import Epub3, Section
from epubuilder.public import Joint, File
from epubuilder.public.metas.dcmes import Title, Language, Identifier

html_template = """
<html>
<head></head>
<body>{}</body></html>
"""

book = Epub3()

# metadata
book.metadata.append(Title('EPUB Demo Book'))
book.metadata.append(Language('en'))
book.metadata.append(Identifier('uuid_' + uuid.uuid1().hex))

# add a file
file = File(html_template.format('hello world').encode())
file_path = 'hello_world.html'
book.files[file_path] = file


joint = Joint(file_path)
book.spine.append(joint)

# table of contents
sec = Section('Hello Wrold', href=file_path)
book.toc.append(sec)

book.write('little-demo.epub')
