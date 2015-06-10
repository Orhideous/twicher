from contextlib import contextmanager
from copy import deepcopy
from functools import wraps
from flask.ext.restful.fields import Integer, String

from pony.orm import db_session


COLORS = {
    'BLUE': '\033[94m',
    'GREEN': '\033[92m',
    'ORANGE': '\033[93m',
    'RED': '\033[91m',
    'END': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m'
}

quote_marshaller = {'id': Integer, 'text': String}


@contextmanager
def perform(name, before, fail, after, kwargs=None):
    kwargs = deepcopy(kwargs) if kwargs else {}
    kwargs.update(
        COLORS,
        name=name,
        before=before.format(**kwargs),
        fail=fail.format(**kwargs),
        after=after.format(**kwargs),
    )
    print("{BLUE}[{name}]{END} {before}".format(**kwargs))
    try:
        yield
    except Exception as e:
        print("{RED}[{name}]{END} {fail}".format(**kwargs))
        print("{RED}[{name}]{END} Reason: {e}".format(e=e, **kwargs))
        exit(1)
    else:
        print("{GREEN}[{name}]{END} {after}".format(**kwargs))


def with_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with db_session:
            return func(*args, **kwargs)
    return wrapper
