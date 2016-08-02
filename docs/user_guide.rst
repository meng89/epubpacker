User Guide
==========

**First of all, should have a book object:**

epub3:
::

    from epubaker import Epub3

    book = Epub3()


epub2:
::

    from epubaker import Epub2

    book = Epub2()


Add files
---------
Then, put a page into the book:

::

    from epubaker import File

    page1_path = 'p1.xhtml'
    book.files[page1_path] = File(open('page1.xhtml', 'rb').read())


Spine
-----
In print book, pages is just papers, when you open a book, you can see the pages.
But epub book can stone lot of type of media, like audio, picture, fonts, and other things.
Lot media is only be a part of a page, it not show up direct.
So you have to let the book reader software knows what pages your want to show, and the show-pages order:
::

    from epubaker import Joint

    book.spine.append(Joint(page1_path))

That's it! That's minimum requirements of a useful book.


You may notise that we can't locating that page because we didn't make table of contents like a print book, do this to fix:
::

    from epubaker import Section

    book.toc.append(Seciton('Chapter I', page1_path))


Metadata
--------

Now, we want reader know what's the title of this book, the identifier of this book
and language of this book:
::

    from epubaker.metas import Title, Identifier, Language

    book.metadata.append(Title('simple epub book'))
    book.metadata.append(Language('en'))
    book.metadata.append(Identifier('any_string_different_from_other_identifier_of_other_book'))

epub3 need modified date:
::

    from epubaker.tools import w3c_utc_date
    from epubaker.metas import get_dcterm

    book.metadata.append(get_dcterm('modified')(w3c_utc_date()))


Cover
-----
Add a image first:
::

    book.files['cover.png'] = File(open('cover.png', 'rb').read())


Let reader know which image is the cover:

epub3:
::

    book.cover_path = 'cover.png'


epub2:
::

    from epubaker.metas import Cover
    book.metadata.append(Cover('cover.png'))


If the reader or bookshelf didn't show the cover,
you may want to make a xhtml page from the cover image, and put it as the first of the book pages:
::

    cover_page_file = book.addons_make_image_page(image_path='cover.png')
    book.files['cover.xhtml'] = cover_page_file
    book.spine.insert(0, Joint('cover.xhtml'))


Write it!
---------
::

    book.write('simple_book.epub')


