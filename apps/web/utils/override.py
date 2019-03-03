# coding=utf-8

from functools import wraps


def override(func):
    """
    Usage:

        from ... import override

        class Child(Parent):

            @override
            def parend_method(self):
                pass

    """
    @wraps(func)
    def _override(*args, **kw):
        IS_OVERRIDE = True  # noqa
        return func(*args, **kw)
    return _override
