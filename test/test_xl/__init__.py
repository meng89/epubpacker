
from epubuilder.xl import parse, clear_spaces, pretty_insert

import os

path = os.path.dirname(__file__)


def test_parse():
    # return
    x = parse(open(os.path.join(path, 'et.xml')).read())

    e = x.root
    e = clear_spaces(e)
    e = pretty_insert(e, dont_do_when_one_child=True)
    print(e.string())


def test_element():
    pass
