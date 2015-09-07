
import os

from lxml import etree

from epubuilder import Item
from epubuilder import MediaTypeError
from epubuilder import E_GIF, E_JPEG, E_JPG, E_SVG
from PIL import Image
import io


def create_cover_page(item):
    image_es = (E_GIF, E_JPEG, E_JPG, E_SVG)

    if isinstance(item, Item):
        raise TypeError('must be an instance of epub.Item')
    elif os.path.splitext(item.path)[0] not in image_es:
        raise MediaTypeError('item.media_type must be one of: ', image_es)

    width, height = Image.open(io.BytesIO(item.binary)).size

    doc = etree.Element('html', xmlns='http://www.w3.org/1999/xhtml')
    head = etree.SubElement(doc, 'head')
    title = etree.SubElement(head, 'title')
    title.text = 'Cover'
    body = etree.SubElement(doc, 'body')
    div = etree.SubElement(body, 'div', style='text-align: center; padding: 0pt; margin: 0pt;')
    svg = etree.SubElement(div, 'svg', xmlns="http://www.w3.org/2000/svg", height="100%",
                           preserveAspectRatio="xMidYMid meet", version="1.1",
                           viewBox="0 0 {} {}".format(width, height),
                           width="100%")
    svg.set('xmlns:xlink', 'http://www.w3.org/1999/xlink')
    image = etree.SubElement(svg, 'image', width=str(width), height=str(height))
    image.set('xlink:href', item.path)

    return etree.tostring(doc, encoding='utf-8', doctype='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" '
                                                         '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">')
