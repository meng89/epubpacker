.. toctree::
    :hidden:
    :titlesonly:
    :maxdepth: 2

    user_guide
    api/index


Epubuilder is a Python module to build EPUB 2 or 3 document from web files and related information.


Quick Start
-----------
it's a piece from User Guide:
::

    from epubuilder.epub3 import Epub3
    from epubuilder.public import File, Joint

    book = Epub3()

    page1_path = '1.html'

    book.files[page1_path] = File(open('page1.html', 'rb').read())

    book.spine.append(Joint(page1_path))

    book.write('my_book.epub')


Installing
----------
::

    pip install epubuilder

or on Gentoo/Linux:
::

    layman -a observer
    emerge -av epubuilder


Why Epubuilder?
---------------
* **New**. This module run under Python 2 and 3. It suporrts Epub 3, and Epub 2 too.


* **Clear**. Epubuilder doesn't modify the resource you were given.
  Files, metadata and other things are handled by different members of an Epub object.

