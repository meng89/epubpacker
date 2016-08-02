# coding=utf-8

import magic

from epubaker.xl import parse


def relative_path(in_dir, to_file_path):
    """
    if you got file with path "text/cover.xhtml" and it links to "image/cover.png"

    :param in_dir: "text"
    :param to_file_path: "image/cover.png"
    :return: "../image/cover.png"
    """
    paths = to_file_path.split('/')
    dirs = in_dir.split('/')
    if dirs[-1] == '':
        dirs = dirs[0:-1]
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

    if mime == mime.HTML:
        try:
            root = parse(binary.decode()).root
            if root.tag == (None, 'html') and root.prefixs[xhtml_uri] is None:
                return mime.XHTML
        except KeyError:
            return mime.HTML

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
