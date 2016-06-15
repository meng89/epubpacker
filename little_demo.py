from epubuilder.epub import Epub, File
from epubuilder.epub.metadata.dcmes import Title, Language, Identifier

import uuid

html_template = """
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head></head>
<body>{}</body></html>
"""

book = Epub()

# metadata
book.metadata.append(Title('EPUB demo'))
book.metadata.append(Language('en'))
book.metadata.append(Identifier('uuid_' + uuid.uuid1().hex))

file = File(html_template.format('hello world!'))
file_path = 'hello_world.xhtml'
book.files[file_path] = file_path

