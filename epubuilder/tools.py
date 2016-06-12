import magic


def relative_path(full_path, dirt):
    paths = full_path.split('/')
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
    return magic.from_buffer(binary, mime=True).decode()


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
