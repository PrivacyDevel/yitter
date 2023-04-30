import functools
import json

import redis


conn = redis.Redis()

def cache(func=None, *, ttl_secs=None):
    if func is None:
        return functools.partial(cache, ttl_secs=ttl_secs)

    def wrapper(*args, **kwargs):
        key = (func.__name__ + str(args) + str(kwargs)).lower()
        res = conn.get(key)
        if res is None:
            res = func(*args, **kwargs)
            conn.set(key, json.dumps(res), ttl_secs)
        else:
            res = json.loads(res)
        return res
        
        def invalidate_cache():
            print('invalidating', key)
            conn.delete(key)

    return wrapper

