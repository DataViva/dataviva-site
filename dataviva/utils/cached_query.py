from flask import abort, current_app, make_response, Flask, jsonify, request, \
                    Response, session, g, get_flashed_messages

from dataviva import view_cache

''' Get/Sets a given ID in the cache. If data is not supplied, 
    used as getter'''
def cached_query(id, data=None, timeout=None):
    if data is None:
        return view_cache.get(id)
    return view_cache.set(id, data, timeout=timeout)

def make_cache_key(*args, **kwargs):
    path = request.path
    lang = g.locale
    cache_key = (path + lang).encode('utf-8')
    
    if get_flashed_messages():
        msgs = "|".join([msg[0] for msg in get_flashed_messages(with_categories=True)])
        cache_key += "/"+msgs
    
    return cache_key

def api_cache_key(namespace, *args, **kwargs):
    def gen_key(**kwargs):
        path = request.path
        lang = g.locale
        reqstr = ""
        if request.args:
            for k,v in request.args.items():
                reqstr += "&{}={}".format(str(k), str(v))
        key = namespace + ":" + path + lang + reqstr
        cache_key = key.encode('utf-8')

        if get_flashed_messages():
            msgs = "|".join([msg[0] for msg in get_flashed_messages(with_categories=True)])
            cache_key += "/"+msgs

        return cache_key
    return gen_key
