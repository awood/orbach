

from functools import wraps


def to_unicode(obj, encoding='utf-8'):
    if isinstance(obj, str):
        if not isinstance(obj, str):
            obj = str(obj, encoding)
    return obj


def unicode_out(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        output = func(*args, **kwargs)
        if isinstance(output, str):
            output = to_unicode(output)
        elif isinstance(output, dict):
            output = apply_dict(output, str, to_unicode)
        elif isinstance(output, list):
            output = apply_list(output, str, to_unicode)
        return output

    return wrapper


def unicode_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args = apply_list(args, str, to_unicode)
        kwargs = apply_dict(kwargs, str, to_unicode)
        return func(*args, **kwargs)

    return wrapper


def apply_list(data, cls, func):
    rv = []
    for item in data:
        if isinstance(item, cls):
            item = func(item)
        elif isinstance(item, dict):
            item = apply_dict(item, cls, func)
        elif isinstance(item, list):
            item = apply_list(item, cls, func)
        rv.append(item)
    return rv


def apply_dict(data, cls, func):
    rv = {}
    for key, value in data.items():
        if isinstance(key, cls):
            key = func(key)
        if isinstance(value, cls):
            value = func(value)
        elif isinstance(value, dict):
            value = apply_dict(value, cls, func)
        elif isinstance(value, list):
            value = apply_list(value, cls, func)
        rv[key] = value
    return rv
