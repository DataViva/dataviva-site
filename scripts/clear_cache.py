import redis
r = redis.Redis()
for cache_key in r.keys():
    if "session:" not in cache_key:
        r.delete(cache_key)
    else:
        print cache_key
