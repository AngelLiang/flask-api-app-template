# coding=utf-8

import re
import string


def camelize(uncamelized, sep="_"):
    """
    Usage:

        camelize('camel_cap')  # 'camelCap'

    """
    uncamelized = sep + uncamelized.lower().replace(sep, " ")
    return string.capwords(uncamelized).replace(" ", "").lstrip(sep)


def uncamelize(camelCaps, sep='_'):
    """
    Usage:

        uncamelize('camelCap')  # 'camel_cap'

    """
    pattern = re.compile(r'([A-Z]{1})')
    sub = re.sub(pattern, sep + r'\1', camelCaps).lower()
    return sub
