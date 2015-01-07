from dataviva.utils.cached_query import cached_query
from flask import request

def cache_api(namespace):
    def api_decorator(func):
        def func_wrapper(**kwargs):
            params = ["%s=%s" % (k,v) for k,v in kwargs.items()]
            cache_key = namespace + ":" + "-".join(params)
            if request.args:
                cache_key += str(request.args)

            prev = cached_query(cache_key)
            if prev:
                return prev
            result = func(**kwargs)
            cached_query(cache_key, result)
            return result
        return func_wrapper
    return api_decorator
