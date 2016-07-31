# coding=utf-8


class Attrs(object):
    def __init__(self):
        self._attrs = {}


class Id(Attrs):
    @property
    def id(self):
        """xml attributie: `id`
        """
        return self._attrs.setdefault('id')

    @id.setter
    def id(self, value):
        self._attrs['id'] = value


class Scheme(Attrs):
    @property
    def scheme(self):
        """xml attribute: `opf:scheme`"""
        return self._attrs.setdefault('opf:scheme')

    @scheme.setter
    def scheme(self, value):
        self._attrs['opf:scheme'] = value


class AltScript(Attrs):
    @property
    def alt_script(self):
        """xml attribute: `opf:alt-script`"""
        return self._attrs.setdefault('opf:alt-script')

    @alt_script.setter
    def alt_script(self, value):
        self._attrs['opf:alt-script'] = value


class Dir(Attrs):
    @property
    def dir(self):
        """
        "ltr" (left-to-right) or "rtl" (right-to-left)

        xml attribute: `dir`
        """
        return self._attrs.setdefault('dir')

    @dir.setter
    def dir(self, value):
        if value not in ('ltr', 'rtl'):
            raise ValueError('must be "ltr" or "rtl"')

        self._attrs['dir'] = value


class FileAs(Attrs):
    @property
    def file_as(self):
        """xml attribute: `opf:file-as`"""
        return self._attrs.setdefault('opf:file-as')

    @file_as.setter
    def file_as(self, value):
        self._attrs['opf:file-as'] = value


class Role(Attrs):
    @property
    def role(self):
        """xml attribute: `opf:role`"""
        return self._attrs.setdefault('opf:role')

    @role.setter
    def role(self, value):
        self._attrs['opf:role'] = value


class Lang(Attrs):
    @property
    def lang(self):
        """xml attribute: `xml:lang`
        """
        return self._attrs.setdefault('xml:lang')

    @lang.setter
    def lang(self, value):
        self._attrs['xml:lang'] = value


class Authority(Attrs):
    @property
    def authority(self):
        """xml attribute: `authority`"""
        return self._attrs.setdefault('authority')

    @authority.setter
    def authority(self, value):
        self._attrs['authority'] = value
