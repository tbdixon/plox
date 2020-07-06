# From https://www.artima.com/weblogs/viewpost.jsp?thread=101605, https://pypi.org/project/multimethod/, etc. but
# re-written in a simple manner for no reason other than learning...

from typing import get_type_hints
from functools import wraps

_mm_map = dict()


def multimethod(func):
    types = tuple(arg_type for arg_name, arg_type in get_type_hints(func).items() if arg_name != 'return')
    _mm_map[types] = func

    @wraps(func)
    def wrapper(*args, **kwargs):
        k = tuple(map(lambda t: type(t), args))
        return _mm_map[k](*args, **kwargs)

    return wrapper
