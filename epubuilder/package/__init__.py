# opf

from epubuilder.xl import Element, Text


class Package:
    def __init__(self, file=None):
        self.metadata = Metadata()
        if file:
            pass


class Metadata(object):
    """child of Package
    """

    def __init__(self):
        pass


class _E:
    def __init__(self, element):
        self._e = element


# start xml attributes


class _Id(_E):
    @property
    def id(self):
        """option"""
        return self._e.attributes['id']

    @id.setter
    def id(self, v):
        self._e.attributes['id'].value = v


class _XmlLang(_E):
    @property
    def xml__lang(self):
        return self._e.attributes['xml:lang']

    @xml__lang.setter
    def xml__lang(self, value):
        self._e.attributes['xml:lang'] = value


class _Dir(_E):
    @property
    def dir(self):
        return self._e.attributes['dir']

    @dir.setter
    def dir(self, value):
        if value in ('ltr', 'rtl'):
            self._e.attributes['dir'] = value
        else:
            raise Exception


class _FileAs(_E):
    @property
    def file_as(self):
        return self._e.attributes['file-as']

    @file_as.setter
    def file_as(self, value):
        self._e.attributes['file-as'] = value


# end xml attributes


class _Text(_E):
    @property
    def text(self):
        return self._e.children[0].to_string()

    @text.setter
    def text(self, v):
        self._e.children[0] = Text(v)


#######
# start Required child of metadata. Repeatable.

class DcIdentifier(_Id, _Text):
    """dc:identifier, child of Metadata
    """
    def __init__(self, element=None):
        super().__init__(element or Element('dc:identifier'))


class DcTitle(_Id, _XmlLang, _Dir, _FileAs, _Text):
    def __init__(self, element=None):
        super().__init__(element or Element('dc:title'))


class DcLanguage(_Id, _Text):
    def __init__(self, element=None):
        super().__init__(element or Element('dc:language'))

# end Required child of metadata. Repeatable.
#######


#######
# start Optional child of metadata.

class DcCreator(_Id, _XmlLang, _Dir, _FileAs, _Text):
    def __init__(self, element=None):
        super().__init__(element or Element('dc:creator'))


class DcType(_Id, _Text):
    def __init__(self, element=None):
        super().__init__(element or Element('dc:type'))

# up is Repeatable. down is not


class DcPublisher(_Id, _XmlLang, _Dir, _FileAs, _Text):
    def __init__(self, element=None):
        super().__init__(element or Element('dc:publisher'))

# end Optional child of metadata.
#######


class _Property(_E):
    @property
    def property(self):
        """option"""
        return self._e.attributes['property']

    @property.setter
    def property(self, v):
        self._e.attributes['property'].value = v


class _Scheme(_E):
    @property
    def scheme(self):
        """option"""
        return self._e.attributes['scheme']

    @scheme.setter
    def scheme(self, v):
        self._e.attributes['scheme'].value = v


class Meta(_Property, _Id, _Scheme, _XmlLang, _Dir, _Text):
    def __init__(self, element=None):
        super().__init__(element or Element('meta'))


class _Href(_E):
    @property
    def href(self):
        """option"""
        return self._e.attributes['href']

    @href.setter
    def href(self, v):
        self._e.attributes['href'].value = v


class _Rel(_E):
    @property
    def rel(self):
        """option"""
        return self._e.attributes['rel']

    @rel.setter
    def rel(self, v):
        self._e.attributes['rel'].value = v


class _MediaType(_E):
    @property
    def media_type(self):
        """option"""
        return self._e.attributes['media-type']

    @media_type.setter
    def media_type(self, v):
        self._e.attributes['media-type'].value = v


class _Properties(_E):
    @property
    def properties(self):
        """option"""
        return self._e.attributes['properties']

    @properties.setter
    def properties(self, v):
        self._e.attributes['properties'].value = v


class Link(_Href, _Rel, _Id, _MediaType, _Properties):
    def __init__(self, element=None):
        super().__init__(element or Element('link'))


class Manifest(_Id):
    def __init__(self, element=None):
        super().__init__(element or Element('manifest'))


class _Fallback(_E):
    @property
    def fallback(self):
        """option"""
        return self._e.attributes['fallback']

    @fallback.setter
    def fallback(self, v):
        self._e.attributes['fallback'].value = v


class _MediaOverlay(_E):
    @property
    def media_overlay(self):
        """option"""
        return self._e.attributes['media-overlay']

    @media_overlay.setter
    def media_overlay(self, v):
        self._e.attributes['media-overlay'].value = v


class _Duration(_E):
    @property
    def duration(self):
        """option"""
        return self._e.attributes['duration']

    @duration.setter
    def duration(self, v):
        self._e.attributes['duration'].value = v


class Item(_Id, _Href, _MediaType, _Fallback, _Properties, _MediaOverlay, _Duration):
    def __init__(self, element=None):
        super().__init__(element or Element('item'))


class PageProgressionDirection(_E):
    @property
    def page_propression_direction(self):
        """option"""
        return self._e.attributes['page-propression-direction']

    @page_propression_direction.setter
    def page_propression_direction(self, v):
        if v in ('ltr', 'rtl', 'default'):
            self._e.attributes['duration'].value = v
        else:
            raise Exception


class Spine(_Id):
    def __init__(self, element=None):
        super().__init__(element or Element('spine'))


class _Idref(_E):
    @property
    def idref(self):
        """option"""
        return self._e.attributes['idref']

    @idref.setter
    def idref(self, v):
        self._e.attributes['idref'].value = v


class _Linear(_E):
    @property
    def linear(self):
        """option"""
        return self._e.attributes['linear']

    @linear.setter
    def linear(self, v):
        if v not in ('yes', 'no'):
            raise Exception

        self._e.attributes['linear'].value = v


class Itemref(_Idref, _Linear, _Id, _Properties):
    def __init__(self, element=None):
        super().__init__(element or Element('itemref'))


class Collection(_XmlLang, _Dir, _Id, ):
