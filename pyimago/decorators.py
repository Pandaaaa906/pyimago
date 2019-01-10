from functools import wraps


def ensure_session_id(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.set_session_id()
        return func(self, *args, **kwargs)

    return wrapper


def decode_result(decode='u8'):
    def _decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            b = func(*args, **kwargs)
            return b.decode(decode)

        return wrapper

    return _decorator


def check_error(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        res = func(self, *args, **kwargs)
        if res != 1:
            err = self.get_last_error()
            raise ValueError(err)
        return None

    return wrapper
