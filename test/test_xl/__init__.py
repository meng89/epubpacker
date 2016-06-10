
from xl import parse, Element, clear_spaces, insert_spaces_for_pretty

import os

path = os.path.dirname(__file__)


def test_parse():
    return
    e = parse(open(os.path.join(path, '1.xml')).read())

    e = clear_spaces(e)
    e = insert_spaces_for_pretty(e)
    print(e.xml_string())


def test_element():
    pass
