
from epubuilder.xl import parse, clean_whitespaces, pretty_insert

import os

path = os.path.dirname(__file__)


def test_parse():
    # return
    x = parse(open(os.path.join(path, 'et.xml')).read())

    e = x.root
    e = clean_whitespaces(e)
    e = pretty_insert(e, dont_do_when_one_child=True)
    print(e.string())


def test_element():
    pass
