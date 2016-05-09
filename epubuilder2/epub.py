

import os
import time
import uuid
import zipfile

from xl import Element

media_table = [
    ['image/gif', ['.gif'], 'Images'],
    ['image/jpeg', ['.jpg', 'jpeg'], 'Images'],
    ['image/png', ['.png'], 'Images'],
    ['image/svg+xml', ['.svg'], 'Images'],

    ['application/xhtml+xml', ['.html', '.xhtml'], 'Text'],

    ['application/x-dtbncx+xml', ['.ncx'], '?'],

    ['application/vnd.ms-opentype', ['.otf', '.ttf', '.ttc'], 'Fonts'],
    ['application/font-woff', ['.woff'], 'Fonts'],
    ['application/smil+xml', [], ''],
    ['application/pls+xml', [], ''],

    ['audio/mpeg', [], ''],
    ['audio/mp4', ['.mp4'], ''],

    ['text/css', ['.css'], 'Styles'],

    ['text/javascript', ['.js'], 'Scripts'],
]


# TOC


toc = [
    {
        'title': '1 XXX',
        'link': '',  # or None
        'sub_sections':
            [
                {'title': '1.2 XXX', 'link': '', 'sub_sections': [...]}
            ]
    }
]

class Section:
    def __init__(self, title, link=None):
        self._title = title
        self._link = link
        self._subsections = []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        self._link = value

    @property
    def subsections(self):
        return self._subsections


class Epub:
    def __init__(self, filename=None):
        if filename:
            pass

        self.nav_element = None


        self.package_element = Element(name='package')
        self.item
    def add_file(self, data, filename=None):
        pass

    def