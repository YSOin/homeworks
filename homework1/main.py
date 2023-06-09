import pathlib
import os
import random
import time
import timeit
import functools
import requests

import os, psutil

# pid = os.getpid()





class LFUCache:
    def __init__(self, func, max_limit = 10):
        self.func = func
        self.cache = dict()
        self.counter = dict()
        self.max_limit = max_limit

    def add(self, cache_key, result):
        self.cache.update({cache_key:result})

    def update_counter(self, cache_key):
        if cache_key in self.cache:
            self.counter[cache_key]+=1
        else:
            self.counter.update({cache_key:1})

    def remove(self):
        self.cache.pop(min(self.counter))

    def __call__(self, *args, **kwargs):
        cache_key = (args, tuple(kwargs.items()))
        self.update_counter(cache_key)
        if cache_key in self.cache:
                return self.cache[cache_key]
        result = self.func(*args, **kwargs)
        if len(self.cache) >= self.max_limit:
            self.remove()
            self.add(cache_key, result)
        else:
            self.add(cache_key, result)
        return result


def memory_usage(f):
    @functools.wraps(f)
    def deco(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        memory_used = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2
        print('Memory_used', f'({f.__name__}): {memory_used}MiB')
        return result
    return deco





@LFUCache
@memory_usage
def some_function(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    print(url)
    return res.content[:first_n] if first_n else res.content

some_function('https://google.com')
some_function('https://google.com')
some_function('https://google.com')
some_function('https://ithillel.ua')
some_function('https://dou.ua')
some_function('https://ain.ua')
some_function('https://youtube.com')
some_function('https://github.com')
some_function('https://github.com')
some_function('https://github.com')
some_function('https://docs.python.org')
some_function('https://docs.python.org')
some_function('https://docs.python.org')
some_function('https://docs.python.org')
some_function('https://docs.python.org')
some_function('https://pypi.org')
some_function('https://pypi.org')
some_function('https://pypi.org')
some_function('https://www.enjoyalgorithms.com')
some_function('https://stackoverflow.com')
some_function('https://monkeytype.com/')
