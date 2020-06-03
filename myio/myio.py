from os import PathLike
import contextlib


@contextlib.contextmanager
def make_open(path_or_file, mode='r'):
    """ For a file or a pathlike, yield an open file.
    If it's not yet open, the mode will be honored.
    If it is open and the mode doesn't match,
    behavior is unspecified.
    """

    if isinstance(path_or_file, (str, PathLike)):
        f = file_to_close = open(path_or_file, mode)
    else:
        f = path_or_file
        file_to_close = None

    try:
        yield f
    finally:
        if file_to_close:
            file_to_close.close()


def auto_make_open(kwarg_name, mode='r'):
    """ Decorator to open a pathlike as a file, if one is passed
    where a file object is expected.

    The file must be referenced as a keyword arg, not a positional arg.
    This is so that it can be stacked on the same function for multiple files.
    """
    # base code:
    #     https://stackoverflow.com/questions/6783472/python-function-that-accepts-file-object-or-path
    # decorator decorators template:
    #     https://stackoverflow.com/questions/5929107/decorators-with-parameters

    def decorator(func):
        def wrapper(*args, **kwargs):
            with make_open(kwargs[kwarg_name], mode) as f:
                kwargs[kwarg_name] = f
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator
