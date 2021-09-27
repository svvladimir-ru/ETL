import time
from functools import wraps


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=3):

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            t = start_sleep_time
            count = 0
            while True:
                try:
                    return func()
                except Exception:
                    time.sleep(t)
                    if t >= border_sleep_time:
                        t = border_sleep_time
                    if t < border_sleep_time:
                        t *= factor
                    count += 1
                    print(f'Попытка подключения №{count}')

        return inner

    return func_wrapper


def coroutine(func):
    @wraps(func)
    def inner(*args, **kwargs):
        fn = func(*args, **kwargs)
        next(fn)
        return fn

    return inner