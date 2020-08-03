from time import perf_counter
from numpy import array


def bench_time(func, l):
    print(func, l)

    def inner(*args, **kwargs):
        t1 = perf_counter()
        r = func(*args, **kwargs)
        t2 = perf_counter()
        print(f"Time taken for '{func.__name__}': {round(t2-t1, 4)} s")
        return r
    return inner


def _str_to_array(str_values):
    values = []
    for i in str_values.split(","):
        if i != '':
            values.append(int(i))
    return array(values)
