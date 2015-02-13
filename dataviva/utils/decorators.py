from dataviva.utils.cached_query import cached_query
from flask import request, g

def cache_api(namespace, timeout=None):
    def api_decorator(func):
        def func_wrapper(**kwargs):
            params = ["%s=%s" % (k,v) for k,v in kwargs.items()]
            cache_key = namespace + ":" + "-".join(params)

            if request.args:
                lang = request.args.get('lang', '') or g.locale
                cache_key += str(request.args) + lang
            else:
                cache_key += g.locale

            prev = cached_query(cache_key)
            if prev:
                return prev
            result = func(**kwargs)
            cached_query(cache_key, result, timeout=timeout)
            return result
        return func_wrapper
    return api_decorator
