# coding=utf-8

from __future__ import print_function

from xml.etree import ElementTree as Et

from epubaker.xl import parse, clean_whitespaces, pretty_insert

import os

path = os.path.dirname(__file__)

TEST_XML_PATH = os.path.join(path, 'test.xml')


def test_parse():
    xmlstr = open(TEST_XML_PATH).read()
    xl = parse(xmlstr)

    e = xl.root

    clean_e = clean_whitespaces(e)

    pretty_e = pretty_insert(clean_e, dont_do_when_one_child=True)

    assert clean_e.string() == clean_whitespaces(pretty_e).string()

    assert pretty_e.string() == pretty_insert(clean_e, dont_do_when_one_child=True).string()

    assert clean_e.string() != pretty_e.string()

    Et.fromstring(xl.string())

    xl.root = clean_e
    Et.fromstring(xl.string())

    xl.root = pretty_e
    Et.fromstring(xl.string())
