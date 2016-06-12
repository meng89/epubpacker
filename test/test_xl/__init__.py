
from epubuilder.xl import parse, Element, clear_spaces, pretty_insert

import os

path = os.path.dirname(__file__)


def test_parse():
    # return
    e = parse(open(os.path.join(path, '1.xml')).read())

    e = clear_spaces(e)
    e = pretty_insert(e, dont_do_when_one_child=True)
    print(e.string())


def test_element():
    pass
