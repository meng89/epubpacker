import epubuilder
from epubuilder.epub import Epub

book = Epub()

# set metadata
book.metadata['language'] = 'en-GB'
book.metadata['title'] = 'This is Title'
book.metadata['identifier'] = ''

# add file
path = book.add_file(data='', filename='/text/1.txt')


# set toc





