# cover-image  specify by user
# nav specify by epubuilder.epub

# mathml
# scripted
# remote-resources

# svg

from epubuilder.xl import parse, Element


def _have_tag(element, tag):
    if element.name == tag:
        return True

    for one in element.children:
        if isinstance(element, Element):
            if _have_tag(one, tag):
                return True

    return False


def identify(data, ):
    properties = []
    e = parse(data.decode())

    if _have_tag(e, (None, 'math')):
        properties.append('mathml')
    if _have_tag(e, (None, 'script')):
        properties.append('scrpted')

    return properties
