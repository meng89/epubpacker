
from epub import Epub

from epub.metadata import Identifier, Title, Language, Meta


ebook = Epub()

ebook.metadata.extend([Identifier('this is dc:identifire'), Title('this is dc:title'), Language('en'),
                       Meta()])

ebook.metadata.append()