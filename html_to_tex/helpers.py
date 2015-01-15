# -*- coding: utf-8 -*-
from shutil import rmtree
from tempfile import mkdtemp


class TemporaryDirectory(object):

    def __init__(self):
        self.name = mkdtemp()

    def __enter__(self):
        if self.name is None:
            raise ValueError("Cannot enter context with removed directory")
        return self

    def __exit__(self, exc, value, tb):
        rmtree(self.name, ignore_errors=True)
        self.name = None


def min_max(f, *args, **kwargs):
    try:
        result = f(*args, **kwargs)
        if 'key' in kwargs:
            return kwargs['key'](result)
        else:
            return result
    except ValueError:
        return None


def max_soft(*args, **kwargs):
    return min_max(max, *args, **kwargs)


def min_soft(*args, **kwargs):
    return min_max(min, *args, **kwargs)


def cache(function, *args, **kwargs):
    if hasattr(function, "im_self"):
        self = function.im_self
    else:
        self = args[0]
    cache_name = "_cache_" + function.__name__
    if not hasattr(self, cache_name):
        setattr(self, cache_name, function(*args, **kwargs))
    return getattr(self, cache_name)


def cache_result(function, *args, **kwargs):
    def cached_function(*args, **kwargs):
        return cache(function, *args, **kwargs)
    return cached_function


def find_first(iterator, condition, modifier=None, default=None):
    if modifier:
        related = (modifier(x) for x in iterator if condition(x))
    else:
        related = (x for x in iterator if condition(x))
    try:
        return related.next()
    except StopIteration:
        return default


def only_true(iterable):
    return (x for x in iterable if x)


def get_template(template_name, globals=None):
    """Load a template."""
    from libs.misc.jinja2.enviroment import env
    return env.get_template(template_name, globals=globals)
