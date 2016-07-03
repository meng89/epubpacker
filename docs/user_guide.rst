User Guide
==========

What is a ebook needed?
-----------------------

First of all, should have a book object:
::

    from epubuilder.epub3 import Epub

    book = Epub()


Then, put a page into the book:
::

    from epubuilder.public import File

    page1 = File(open('page1.html', 'rb').read())
    book.files['1.html'] = page1

In print book, pages is just papers, when you open a book, you can see the pages.
But epub book can stone rich media, like audio, picture and other things.
So you have to let the book reader software knows what pages your want to show, and the show-pages order:
::

    from epubuilder.public import Joint

    book.spine.append(Joint(page1))


That's it! it's minimum requirements of a useful book.

You may notise that we can't locating that page cause we didn't make table of contents like a print book, do this to fix:
::

    from epubuilder.epub3 import Section

    book.toc.append(Seciton('Chapter I', '1.html'))


Now, we want reader know who made this book, what's the title of this book, the identifier of this book
and language of this book:
::

    from epubuilder.public.metas.dcmes import Creator, Title, Identifier, Language

    book.metadata.append(Creator('a name'))
    book.metadata.append(Title('simple epub book'))
    book.metadata.append(Identifier('any_string_different_from_other_identifier_of_other_book'))
    book.metadata.append(Language('en'))

A book have a cover is looks more professional:
::

    book.files['cover.png'] = File(open('cover.png', 'rb').read())
    book.cover_path = 'cover.png'


finally, write to a file:
::

    book.write('simple_book.epub')
