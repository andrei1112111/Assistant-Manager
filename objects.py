class Student:
    def __init__(self, gitlab, plane, bookstack, kimai):
        self.git = gitlab
        self.plane = plane
        self.bookstack = bookstack
        self.kimai = kimai


def trace(func):
    def wrapper(*args, **kwargs):
        print(f'TRACE: calling {func.__name__}() '
              f'with {args}, {kwargs}')

        original_result = func(*args, **kwargs)

        print(f'TRACE: {func.__name__}() '
              f'returned {original_result!r}')

        return original_result
    return wrapper
