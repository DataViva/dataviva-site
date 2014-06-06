from flask import current_app

''' Get/Sets a given ID in the cache. If data is not supplied, 
    used as getter'''
def cached_query(id, data=None):
    c = current_app.config.get('REDIS_CACHE')
    if c is None:
        return None
    if data is None:
        return c.get(id)
    return c.set(id, data)
