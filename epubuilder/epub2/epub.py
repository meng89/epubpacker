from hooky import List

from ..epub3 import Epub

import string
import zipfile

import html5lib
import os
import random
from hooky import List

from epubuilder import mimes

# from epubuilder.epubpublic import Toc, Files, File, Spine, Section, _SubSections

import epubuilder.epubpublic as p

import epubuilder.version
from epubuilder.meta.dcmes import Identifier, URI_DC
from epubuilder.meta.dcterms import get
from epubuilder.tools import w3c_utc_date
from epubuilder.xl import Xl, Header, Element, Text, xml_header, URI_XML, pretty_insert
from epubuilder.meta import Base

CONTAINER_PATH = 'META-INF' + os.sep + 'container.xml'
ROOT_OF_OPF = 'EPUB'


class Epub2:
    def __init__(self):
        self._toc

