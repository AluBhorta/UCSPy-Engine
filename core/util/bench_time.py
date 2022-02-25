from time import perf_counter


def bench_time(func):
    def inner(*args, **kwargs):
        t1 = perf_counter()
        r = func(*args, **kwargs)
        t2 = perf_counter()
        print(f"Time taken for '{func.__name__}': {round(t2-t1, 4)}s")
        return r
    return inner
