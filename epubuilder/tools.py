import magic

from epubuilder import mimes
from epubuilder.xl import parse


def relative_path(file_path, dirt):
    paths = file_path.split('/')
    dirs = dirt.split('/')
    l = len(paths) if len(paths) >= len(dirs) else len(dirs)
    for i in range(l):
        if len(paths) == i or len(dirs) == i or paths[i] != dirs[i]:
            return '/'.join(['..'] * len(dirs[i:]) + list(paths[i:]))


def identify_mime(binary):
    """

    :param binary: bytes html
    :return: mime
    """
    mime = magic.from_buffer(binary, mime=True).decode()

    xhtml_uri = 'http://www.w3.org/1999/xhtml'

    if mime == mimes.HTML:
        try:
            root = parse(binary.decode())
            if root.name == (None, 'html') and root.prefixs[xhtml_uri] is None:
                return mimes.XHTML
        except KeyError:
            return mimes.HTML

    return mime


def w3c_utc_date(date_time=None):
    """

    :param date_time: instance of datetime, default is datetime.utcnow()
    :return: like 'CCYY-MM-DDThh:mm:ssZ'
    """
    from datetime import datetime

    if date_time is not None:
        if not isinstance(date_time, datetime):
            raise TypeError
    else:
        date_time = datetime.utcnow()

    return '{:0>4d}-{:0>2d}-{:0>2d}T{:0>2d}:{:0>2d}:{:0>2d}Z'.format(date_time.year,  date_time.month, date_time.day,
                                                                     date_time.hour, date_time.minute, date_time.second)
