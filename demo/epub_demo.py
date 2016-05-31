
from epub import Epub

from epub.metadata import Identifier, Title, Language, Meta


ebook = Epub()

ebook.metadata.extend([Identifier('this is metadata:identifire'),
                       Title('this is metadata:title'),
                       Language('en'),
                       Meta(text='', attrs={'property': 'dcterms:modified'})])

