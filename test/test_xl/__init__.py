
from xl import parse, Element

import os

path = os.path.dirname(__file__)


def test_parse():
    doc = parse(open(os.path.join(path, '1.xml')).read())

    print(doc.to_string())


def test_element():
    print('hello nose')
