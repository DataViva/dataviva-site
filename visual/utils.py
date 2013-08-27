import cStringIO, gzip, pickle
from re import sub
from werkzeug.datastructures import CallbackDict
from jinja2 import Markup
from flask import abort, current_app
from datetime import datetime, date, timedelta
from math import ceil
from uuid import uuid4
from redis import Redis

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

    def serialize(self, exclude=("bra", "industry", "wld", "occupation", "product"), extra=()):
        "Returns model's PUBLIC data for jsonify"
        data = {}
        # return data
        keys = self._sa_instance_state.attrs.items()
        public = self.__public__ + extra if self.__public__ else extra
        
        for k, field in keys:
            if (public and k not in public) or k in exclude or hasattr(field.value, '__module__'):
                continue
            data[k] = self._serialize(field.value)
        return data

    @classmethod
    def _serialize(cls, value, follow_fk=False):
        if type(value) in (datetime, date):
            ret = value.isoformat()
        elif hasattr(value, '__iter__'):
            ret = []
            for v in value:
                ret.append(cls._serialize(v))
        elif AutoSerialize in value.__class__.__bases__:
            ret = value.get_public()
        else:
            ret = value

        return ret


''' A helper class for including pagination in templates'''
class Pagination(object):

    def __init__(self, page, per_page, total_count, order=None):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count
        self.order = order

    @property
    def pages(self):
        if str(self.per_page).isdigit():
            return int(ceil(self.total_count / float(self.per_page)))
        else:
            return 0

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    @staticmethod
    def get_per_page_options():
        return [10, 25, 50, 100, "all"]
    
    def serialize(self):
        return {
            "page": self.page, "per_page": self.per_page,
            "total_count": self.total_count, "order": self.order,
            "has_prev": self.has_prev, "has_next": self.has_next,
            "pages": [p for p in self.iter_pages()]
        }
    
    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

''' A helper class for dealing with injecting times into the page using moment.js'''
class Momentjs:
    def __init__(self, timestamp):
        self.timestamp = timestamp

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
        
    def render(self, type, lang):
        if isinstance(self.text,unicode) or isinstance(self.text,str):
            format = "text"
        else:
            format = "number"
            
        return Markup("<script>\ndocument.write(visual.format.%s(\"%s\",\"%s\",\"%s\"))\n</script>" % (format, self.text, type, lang))

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
    c = current_app.config.get('REDIS')
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
            redis = Redis()
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