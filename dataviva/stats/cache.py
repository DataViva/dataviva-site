# cache.py
from dataviva import view_cache as cache
import pickle

def object_cache(key, value=None):
    if not value:
        tmp = cache.get(key)
        if not tmp: 
            return None
        return pickle.loads(tmp)
    else:
        cache.set(key, pickle.dumps(value))
        return value

def profile_cache_serialized(ptype, attrs):
    key = "profile_" + str(attrs)
    obj = object_cache(key)
    if not obj:
        if type(attrs) is list:
            obj = ptype(*attrs)
        else:
            obj = ptype(attrs)
        obj = obj.serialize()
        object_cache(key, obj)
    return obj