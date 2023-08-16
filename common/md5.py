import hashlib


def md5(string):
    m = hashlib.md5(string.encode(encoding='utf-8'))

    return m.hexdigest()
