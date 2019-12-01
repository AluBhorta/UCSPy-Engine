import numpy as np
from numba import jit

@jit(nopython=True)
def numba_pass_arr(arr):
    for i in range(len(arr)):
        print(arr[i])


@jit(nopython=True)
def numba_list_comprehension(n):
    return [i**2 for i in range(n)]


@jit(nopython=True)
def numba_rand_arr(n):
    return np.random.randint(low=n, high=100, size=100)


@jit(nopython=True)
def numba_multidim_arr(arr):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            print(arr[i][j])


@jit(nopython=True)
def numba_exceptions(condition):
    if condition:
        print("yay")
    else:
        raise Exception("Numba handles exceptions")


@jit(nopython=True)
def numba_list_append(n):
    a = []
    for i in range(n):
        a.append(i**3)

    return a
