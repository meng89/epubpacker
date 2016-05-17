import os
import time
import uuid
import zipfile

import hooky

from xl import Element


from epubl import Epubl


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


class Meta:
    def __init__(self):
        self._text = None
        self._attr = {}

    @property
    def text(self):
        return self._text


def make_meta(key):
    pass


class Metadata(hooky.Dict):
    def __init__(self):
        super().__init__()

    def __getitem__(self, key):
        if key not in self.data.keys():
            self.data[key] = make_meta(key)
        return self.data[key]


class Section:
    def __init__(self, title, link=None):
        self._title = title
        self._link = link
        self._subsections = []

        self._hidden_sub = None

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

    #
    @property
    def hidden_sub(self):
        return self._hidden_sub

    @hidden_sub.setter
    def hidden_sub(self, value):
        if value not in (True, False):
            raise ValueError
        else:
            self._hidden_sub = value


class Epubm:
    def __init__(self, filename=None):
        self._epubm = Epubl(filename)

        if filename:
            pass

        self.package_element = Element(name='package')

        self._metadata = Metadata()

        self._spine = None

        # nav
        self._toc = None
        self._landmark = None
        self._pagelist = None

    def add_file(self, data, path, media_type):
        pass

    @property
    def metadata(self):
        return self._metadata

    @property
    def spine(self):
        return self._spine

    @property
    def toc(self):
        return self._toc

    @property
    def landmark(self):
        return self._landmark

    @property
    def pagelist(self):
        return self._pagelist

    def write(self, filename):
        self._epubm.package_element

        self._epubm.write(filename)
