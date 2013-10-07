import cStringIO, gzip, pickle, re
from re import sub
from werkzeug.datastructures import CallbackDict
from jinja2 import Markup
from flask import abort, current_app, make_response, Flask, jsonify, request
from functools import update_wrapper
from datetime import datetime, date, timedelta
from math import ceil
from uuid import uuid4
from config import REDIS

from flask.sessions import SessionInterface, SessionMixin

############################################################
# ----------------------------------------------------------
# Utility methods for entire site
# 
############################################################

''' A Mixin class for retrieving public fields from a model
    and serializing them to a json-compatible object'''
class AutoSerialize(object):
    __public__ = None

    def serialize(self):
        
        data = self.__dict__
        allowed = []
        
        for key, value in data.iteritems():
            
            if isinstance(value,unicode) or \
                isinstance(value,float) or \
                isinstance(value,int) or \
                isinstance(value,str) or \
                isinstance(value,long):
                allowed.append((key,value))
        
        data = dict(allowed)
        
        return data

''' A helper class for dealing with injecting times into the page using moment.js'''
class Momentjs:
    def __init__(self, timestamp):
        self.timestamp = timestamp
        
    def __call__(self, *args):
        return self.format(*args)

    def render(self, format):
        return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")
        
class formatter:
    def __init__(self, text):
        self.text = text
        
    def __call__(self, *args):
        return self.format(*args)
        
    def render(self, type, lang):
        if isinstance(self.text,unicode) or isinstance(self.text,str):
            format = "text"
        else:
            format = "number"
            
        return Markup("<script>\ndocument.write(dataviva.format.%s(\"%s\",\"%s\",\"%s\"))\n</script>" % (format, self.text, type, str(lang)))

''' A helper funciton for stripping out html tags for showing snippets of user submitted content'''
def strip_html(s):
    return sub('<[^<]+?>', '', s)

def jinja_split(s, char):
    return s.split(char)

''' A helper function for retrieving a specific item from the given model that
    will raise a 404 error if not found in the DB'''
def exist_or_404(Model, id):
    item = Model.query.get(id)
    if item:
        return item
    abort(404, 'Entry not found in %s with id: %s' % (Model.__tablename__, id))

''' Helper function to gzip JSON data (used in data API views)'''
def gzip_data(json):
    # GZip all requests for lighter bandwidth footprint
    gzip_buffer = cStringIO.StringIO()
    gzip_file = gzip.GzipFile(mode='wb', compresslevel=6, fileobj=gzip_buffer)
    gzip_file.write(json)
    gzip_file.close()
    return gzip_buffer.getvalue()

''' Get/Sets a given ID in the cache. If data is not supplied, 
    used as getter'''
def cached_query(id, data=None):
    c = current_app.config.get('REDIS_CACHE')
    if data is None:
        return c.get(id)
    return c.set(id, data)

''' Given a "year" string from URL, turn this into an array of years 
    as integers'''
def parse_years(year_str):
    year_str = str(year_str)
    if "-" in year_str:
        # we allow a range of years w/ or w/o interval (using '.' as sep)
        year_start, year_end = year_str.split("-")
        if "." in year_end:
            year_end, year_interval = year_end.split(".")
        else:
            year_interval = "1"
        years = range(int(year_start), int(year_end)+1, int(year_interval))
    else:
        # we allow a set of years (with '+' between)
        years = [int(y) for y in year_str.split("+")]
    return years
    
''' Titlecase Function '''
def title_case(string):
    exceptions = ['A', 'An', 'And', 'As', 'At', 'But', 'By', 'For', 'From', 'If', \
              'In', 'Into', 'Near', 'Nor', 'Of', 'On', 'Onto', 'Or', 'That', \
              'The', 'To', 'With', 'Via', 'Vs', 'Vs.', \
              'Um', 'Uma', 'E', 'Como', 'Em', 'No', 'Na', 'Mas', 'Por', \
              'Para', 'Pelo', 'Pela', 'De', 'Do', 'Da', 'Se', 'Perto', 'Nem', \
              'Ou', 'Que', 'O', 'A', 'Com']
    words = re.split(" ",string)
    final = [words[0].capitalize()]
    for word in words[1:]:
        if word in exceptions or word.capitalize() in exceptions:
            final.append(word.lower())
        else:
            final.append(word.capitalize())
    return " ".join(final)

''' We are using a custom class for storing sessions on the serverside instead
    of clientside for persistance/security reasons. See the following:
    http://flask.pocoo.org/snippets/75/ '''
class RedisSession(CallbackDict, SessionMixin):

    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False

class RedisSessionInterface(SessionInterface):
    serializer = pickle
    session_class = RedisSession

    def __init__(self, redis=None, prefix='session:'):
        if redis is None:
            redis = REDIS
        self.redis = redis
        self.prefix = prefix

    def generate_sid(self):
        return str(uuid4())

    def get_redis_expiration_time(self, app, session):
        if session.permanent:
            return app.permanent_session_lifetime
        return timedelta(days=1)

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid)
        val = self.redis.get(self.prefix + sid)
        if val is not None:
            data = self.serializer.loads(val)
            return self.session_class(data, sid=sid)
        return self.session_class(sid=sid, new=True)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            self.redis.delete(self.prefix + session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                                       domain=domain)
            return
        redis_exp = self.get_redis_expiration_time(app, session)
        cookie_exp = self.get_expiration_time(app, session)
        val = self.serializer.dumps(dict(session))
        self.redis.setex(self.prefix + session.sid, val,
                         int(redis_exp.total_seconds()))
        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=cookie_exp, httponly=True,
                            domain=domain)
                            
def crossdomain(origin="*", methods=None, headers=['Content-Type','x-requested-with'],
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    #if not isinstance(origin, basestring):
    #    origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()
        
    def get_methods():
        if methods is not None:
            return methods
            
        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']
        
    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp
                
            h = resp.headers
            
            h['Access-Control-Allow-Origin'] = "*"
            
            # if "Origin" not in request.headers:
            #     h['Access-Control-Allow-Origin'] = request.environ["HTTP_HOST"]
            # elif request.headers["Origin"] in origin:
            #     h['Access-Control-Allow-Origin'] = request.headers["Origin"]
            #         
            # if origin == '*':
            #     h['Access-Control-Allow-Origin'] = origin
                    
            #h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
                
            return resp
            
        f.provide_automatic_options = False
        f.required_methods = ['OPTIONS']
        return update_wrapper(wrapped_function, f)
    return decorator