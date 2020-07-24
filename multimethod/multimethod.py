# From https://www.artima.com/weblogs/viewpost.jsp?thread=101605, https://pypi.org/project/multimethod/, etc. but
# re-written in a simple manner for this use case e.g. ignoring some args and simple

from typing import get_type_hints
from functools import wraps

_mm_map = dict()


def multimethod(func):
    # For this usage we just want the first argument type since we're doing this to handle
    # multimethods on different classes, the rest of the arguments get passed with *args / **kwargs
    # This seems pretty gross looking but functional for now and only used here...take the first type hint
    class_type = get_type_hints(func)[list(get_type_hints(func))[0]]
    if func.__name__ not in _mm_map:
        _mm_map[func.__name__] = {}
    _mm_map[func.__name__][class_type] = func

    @wraps(func)
    def wrapper(*args, **kwargs):
        return _mm_map[func.__name__][type(args[0])](*args, **kwargs)

    return wrapper
