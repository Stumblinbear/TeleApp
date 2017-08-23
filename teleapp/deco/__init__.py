import inspect


def get_default_args(func):
    args, varargs, keywords, defaults = inspect.getargspec(func)
    if defaults is None:
        return {}
    return dict(zip(args[-len(defaults):], defaults))
