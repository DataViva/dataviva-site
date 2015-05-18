import redis, sys, os

r = redis.Redis(host=os.environ.get("DATAVIVA_REDIS_HOST", "localhost"), 
                port=os.environ.get("DATAVIVA_REDIS_PORT", 6379), 
                db=0, 
                password=os.environ.get("DATAVIVA_REDIS_PW", None), 
                socket_timeout=None, 
                connection_pool=None, 
                charset='utf-8', 
                errors='strict', 
                unix_socket_path=None)

reserved = ["session:", ":rais:", ":secex:", ":hedu:", ":sc:"]
force = len(sys.argv) == 2 and sys.argv[1] == "force"

for cache_key in r.keys():
    
    preserve = any(r in cache_key for r in reserved)
    
    if not preserve or force:
        r.delete(cache_key)
    else:
        print cache_key
