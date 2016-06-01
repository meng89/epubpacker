import time


def data():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
