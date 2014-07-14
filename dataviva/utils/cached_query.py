from flask import abort, current_app, make_response, Flask, jsonify, request, \
                    Response, session, g, get_flashed_messages

''' Get/Sets a given ID in the cache. If data is not supplied, 
    used as getter'''
def cached_query(id, data=None):
    c = current_app.config.get('REDIS_CACHE')
    if c is None:
        return None
    if data is None:
        return c.get(id)
    return c.set(id, data)

def make_cache_key(*args, **kwargs):
    path = request.path
    lang = g.locale
    cache_key = (path + lang).encode('utf-8')
    
    if get_flashed_messages():
        msgs = "|".join([msg[0] for msg in get_flashed_messages(with_categories=True)])
        cache_key += "/"+msgs
    
    return cache_key
