#!/usr/bin/env python3

from epubuilder.epub3 import Epub, File, Joint, Section
from epubuilder.public import File, Joint
from epubuilder.epub2.epub2 import Section

from PIL import Image

import io

img_bytes = open('test/cover/cover.svg', 'rb').read()

img = Image.open(io.BytesIO(img_bytes))

print(img.size)
