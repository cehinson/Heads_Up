# miscellaneous functions to help widgets go here
import numpy
import time
import os
from functools import wraps
from contextlib import contextmanager


def clear_screen():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')


def qimage_to_numpy_array(q_image):
    '''Convert a QImage to a numpy array'''
    ptr = q_image.constBits()
    arr = numpy.array(ptr).reshape(q_image.width(), q_image.height(), 4)  # Copies the data
    return arr


def timethis(func):
    '''Decorator for profiling functions'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print('{}.{} : {}'.format(func.__module__, func.__name__, end-start))
        return r
    return wrapper


@contextmanager
def timeblock(label):
    '''Context manager to time a block of code'''
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print('{} : {}'.format(label, end-start))
