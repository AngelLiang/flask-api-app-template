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


def camelize_for_dict_key(d: dict):
    """把dict的key从下划线转为驼峰"""
    return {camelize(k): v for k, v in d.items()}


def camelize_for_dict_key_in_list(lst: list):
    """把list中的dict的key从下划线转为驼峰"""
    return [camelize_for_dict_key(item) for item in lst]


def uncamelize_for_dict_key(d: dict):
    """把dict的key从驼峰转为下划线"""
    return {uncamelize(k): v for k, v in d.items()}


def uncamelize_for_dict_key_in_list(lst: list):
    """把list中的dict的key从驼峰转为下划线"""
    return [uncamelize_for_dict_key(item) for item in lst]
