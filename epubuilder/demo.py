import epubuilder

book = epubuilder.EasyEpub()

book.set_language('en-GB')
book.set_title('Title of book')

# make Cover image, format should be png/jpg/gif/svg
book.make_cover(open('cover.png', 'rb').read())

# add a page, must be a xhtml file
chapter1_path = book.add_page(open('chapter1.xhtml', 'rb').read())
chapter1_1_path = book.add_page(open('chapter1_1.xhtml', 'rb').read())

# Set table of contents
book.set_toc(('Chapter 1',), chapter1_path)
book.set_toc(('Chapter 1', '1'), chapter1_1_path)

# book.wirte('demo.epub')

book.add_file(path='', xmlstr='', filename='/text/1.txt')

book.metadata['language'] = 'en-GB'
book.metadata['title'] = 'This is Title'
book.metadata['identifier'] = ''

