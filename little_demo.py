import uuid

from epubuilder import Epub, File, Section
from epubuilder.metadata.dcmes import Title, Language, Identifier

html_template = """
<html>
<head></head>
<body>{}</body></html>
"""

book = Epub()

# metadata
book.metadata.append(Title('EPUB demo'))
book.metadata.append(Language('en'))
book.metadata.append(Identifier('uuid_' + uuid.uuid1().hex))

# add a file
file = File(html_template.format('hello world!'))
file_path = 'hello_world.html'
book.files[file_path] = file

# table of contents
Section('Hello Wrold', href=file_path)


book.write('little-demo.epub')
