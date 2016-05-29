from xl import Element

default_ns = 'http://www.w3.org/1999/xhtml'
epub_ns = 'http://www.idpf.org/2007/ops'

html = Element((None, 'html'), {default_ns: None, epub_ns: 'epub'}, attributes={(epub_ns, 'type'): 'toc'})

# html.namespaces[default_ns] = None
# html.namespaces.update({epub_ns: 'epub'})

print(html.xml_string())
