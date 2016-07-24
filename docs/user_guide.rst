User Guide
==========

**First of all, should have a book object:**

epub3:
::

    from epubuilder.epub3 import Epub3

    book = Epub3()


epub2:
::

    from epubuilder.epub2 import Epub2
    book = Epub2()


Add files
---------
Then, put a page into the book:

::

    from epubuilder.public import File

    page1_path = 'p1.xhtml'
    book.files[page1_path] = File(open('page1.xhtml', 'rb').read())


Spine
-----
In print book, pages is just papers, when you open a book, you can see the pages.
But epub book can stone rich media, like audio, picture and other things.
Lot media is only be a part of a page, not show up direct.
So you have to let the book reader software knows what pages your want to show, and the show-pages order:
::

    from epubuilder.public import Joint

    book.spine.append(Joint(page1_path))


That's it! That's minimum requirements of a useful book.



You may notise that we can't locating that page cause we didn't make table of contents like a print book, do this to fix:
::

    from epubuilder.epub3 import Section

    book.toc.append(Seciton('Chapter I', page1_path))


Metadata
--------

Now, we want reader know what's the title of this book, the identifier of this book
and language of this book:
::

    from epubuilder.public.metas.dcmes import Creator, Title, Identifier, Language

    book.metadata.append(Title('simple epub book'))
    book.metadata.append(Language('en'))
    book.metadata.append(Identifier('any_string_different_from_other_identifier_of_other_book'))

epub3 need modified date:
::

    from epubuilder.tools import w3c_utc_date
    from epubuilder.epub3.metas import dcterms

    book.metadata.append(dcterms.get('modified')(w3c_utc_date()))

Cover
-----
Add a image:
::

    book.files['cover.png'] = File(open('cover.png', 'rb').read())


Let reader know which image is the cover:

epub3:
::

    book.cover_path = 'cover.png'


epub2:
::

    from epubuilder.epub2.metas import Cover
    book.metadata.append(Cover('cover.png'))


If the reader or bookshelf didn't show the cover,
you may want to make a xhtml page from cover image, and put it to the first of the book:
::

    cover_page_file = book.addons_make_cover_page(image_path='cover.png')
    book.files['cover.xhtml'] = cover_page_file
    book.spine.insert(0, Joint('cover.xhtml'))



Write to a file
---------------
::

    book.write('simple_book.epub')


