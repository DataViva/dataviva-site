import cStringIO, gzip, pickle, re, operator, sys
from re import sub
from itertools import groupby
from werkzeug.datastructures import CallbackDict
from jinja2 import Markup
from flask import abort, current_app, make_response, Flask, jsonify, request, Response, session
from functools import update_wrapper
from datetime import datetime, date, timedelta
from math import ceil
from uuid import uuid4
from config import REDIS
from decimal import *
from sqlalchemy import func, and_, or_, asc, desc, not_
from uuid import uuid4

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
            
            if isinstance(value,Decimal) or \
                isinstance(value,long):
                value = float(value)
            
            if isinstance(value,unicode) or \
                isinstance(value,float) or \
                isinstance(value,int) or \
                isinstance(value,str):
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
        # we allow a set of years (with '_' between)
        years = [int(y) for y in year_str.split("_")]
    return years
    
''' Titlecase Function '''
def title_case(string):
    exceptions = ['A', 'An', 'And', 'As', 'At', 'But', 'By', 'For', 'From', 'If', \
              'In', 'Into', 'Near', 'Nor', 'Of', 'On', 'Onto', 'Or', 'That', \
              'The', 'To', 'With', 'Via', 'Vs', 'Vs.', \
              'Um', 'Uma', 'E', 'Como', 'Em', 'No', 'Na', 'Mas', 'Por', \
              'Para', 'Pelo', 'Pela', 'De', 'Do', 'Da', 'Se', 'Perto', 'Nem', \
              'Ou', 'Que', 'O', 'A', 'Com']
    uppers = ['Id', 'Tv', 'R&d', "P&d", "It", "Ti"]
    words = re.split('(\s|-|\/|\()', string)
    
    def detect_string(s):
        if s in exceptions or s.capitalize() in exceptions:
            return s.lower()
        elif s in uppers or s.capitalize() in uppers:
            return s.upper()
        else:
            return s.capitalize()
    
    for i, word in enumerate(words):
        words[i] = detect_string(word)
        
    words[0] = words[0].capitalize()
    
    return "".join(words)

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

''' Returns array of ECIs given location '''
def location_values(ret,cat):

    from dataviva.secex.models import Yb_secex
    from dataviva.rais.models import Yb_rais
    
    bra_id = ret[cat][0]["id"]
    if bra_id != "all":
        ecis = Yb_secex.query.filter_by(bra_id=bra_id).all()
        ret["eci"] = {}
        for yb in ecis:
            ret["eci"][yb.year] = yb.eci
    return ret

''' Returns modified query and return variable for data calls '''       
def parse_filter(kwargs,id_type,query,data_table,ret):

    from dataviva.attrs.models import Bra, Isic, Cbo, Hs, Wld

    query = query.group_by(getattr(data_table, id_type))
    cat = id_type.split("_")[0]
    table = locals()[cat.title()]
    ids = kwargs[id_type].split("_")
        
    id_list = []
    depth = None
    for id in ids:
        
        split_obj = id.split(".")

        kms = None
        if split_obj[0] != "all" and split_obj[0] != "show":
            obj_id = split_obj[0]
            if len(split_obj) > 1 and split_obj[1] != "show":
                kms = split_obj[1]
            ret_obj = table.query.get_or_404(obj_id).serialize()
        elif split_obj[0] == "all":
            obj_id = "all"
            if cat == "bra":
                ret_obj = Wld.query.get_or_404("sabra").serialize()
                ret_obj["id"] = "all"
        else:
            obj_id = None
            ret_obj = None
        
        split_depth = id.split("show.")
        if len(split_depth) > 1:
            obj_depth = int(split_depth[1])
        else:
            obj_depth = None
            
        if obj_id:
            if kms:
                neighbors = table.query.get(obj_id).get_neighbors(kms)
                obj_list = []
                for m in neighbors:
                    if m.bra_id_dest == obj_id:
                        obj_list.append(m.bra_id_origin)
                    else:
                        obj_list.append(m.bra_id_dest)
                if "show" not in id:
                    ret_obj["aggregates"] = obj_list
                    ret["aggregate"] = True
                id_list = id_list + obj_list
            elif obj_depth and obj_depth > len(obj_id):
                if "plr" in obj_id:
                    obj_list = table.query.get(obj_id).pr.all()
                    obj_list = [m.id for m in obj_list]
                    id_list = id_list + obj_list
                else:
                    obj_list = table.query.filter(\
                        and_(func.char_length(getattr(table,"id")) == obj_depth, \
                        getattr(table,"id").startswith(obj_id)))
                    munic_list = [d.id for d in obj_list.all()]
                    id_list = id_list + munic_list
            elif obj_id == "all":
                if cat == "bra" or cat == "hs" or cat == "wld":
                    parent_depth = 2
                else:
                    parent_depth = 1
                obj_list = table.query.filter(func.char_length(getattr(table,"id")) == parent_depth)
                obj_list = [d.id for d in obj_list.all()]
                ret_obj["aggregates"] = obj_list
                ret["aggregate"] = True
                id_list = id_list + obj_list
            else:
                id_list.append(obj_id)
        elif obj_depth:
            depth = obj_depth
            
        if ret_obj:
            if cat not in ret:
                ret[cat] = []
            ret[cat].append(ret_obj)
            
    if len(id_list) > 0:
        query = query.filter(getattr(data_table,id_type).in_(id_list))
    elif depth:
        query = query.filter(func.char_length(getattr(data_table,id_type)) == depth)
        
    if cat == "bra" and obj_id:
        if len(ret[cat]) == 0:
            ret[cat].append(Wld.query.get_or_404("sabra").serialize())
        ret = location_values(ret,cat)
        
    return {"query": query, "ret": ret}
    
def merge_objects(objs):

    averages = ['eci', 'eci_wld', 'pci', 'unique_isic', 'unique_cbo',
                'unique_hs', 'unique_wld', 'importance', "wage_avg", "num_emp_est",
                'val_usd_growth_pct', 'val_usd_growth_pct_5', 
                'wage_growth_pct', 'wage_growth_pct_5',
                'num_emp_growth_pct', 'num_emp_growth_pct_5',
                'distance', 'distance_wld',
                'opp_gain', 'opp_gain_wld',
                'rca', 'rca_wld']

    ret_obj = {}
    for obj in objs:
        for k in obj:
            values = []
            for obj2 in objs:
                if k in obj2:
                    if isinstance(obj2[k],str) or isinstance(obj2[k],unicode):
                        values = obj2[k]
                    elif isinstance(obj2[k],Decimal) or isinstance(obj2[k],long) \
                      or isinstance(obj2[k],float) or isinstance(obj2[k],int):
                        values.append(float(obj2[k]))
            if len(values) > 0:
                if not isinstance(values,str) and not isinstance(values,unicode):
                    if k in averages:
                        ret_obj[k] = sum(values)/len(values)
                    else:
                        ret_obj[k] = sum(values)
                else:
                    ret_obj[k] = values
            else:
                ret_obj[k] = None
    return ret_obj

def make_query(data_table, url_args, lang, **kwargs):
    
    from dataviva import db
    from dataviva.attrs.models import Bra, Isic, Cbo, Hs, Wld
            
    ops = {">": operator.gt,
           ">=": operator.ge,
           "<": operator.lt,
           "<=": operator.le}

    check_keys = ["bra_id", "isic_id", "cbo_id", "hs_id", "wld_id"]
    unique_keys = []
    
    download = url_args.get("download", None)
    raw = True if "raw" in kwargs else None
    order = url_args.get("order", None)
    offset = url_args.get("offset", None)
    limit = url_args.get("limit", None)
    cols = url_args.get("cols", None)
    if type(cols) == str or type(cols) == unicode:
        cols = cols.split(".")
    excluding = url_args.get("excluding", None)
    if offset:
        offset = float(offset)
        limit = limit or 50
    filter = url_args.get("filter", None)
    if filter:
        filter = re.split("(>=|>|<=|<)", filter)
    join = kwargs["join"] if "join" in kwargs else False
    show_id = None
    cache_id = request.path
    ret = {}
    # first lets test if this query is cached (be sure we are not paginating
    # results) as these should not get cached
    if limit is None and download is None and raw is None and cols is None:
        cached_q = cached_query(cache_id)
        if cached_q:
            return cached_q
    
    query = db.session.query(data_table)
    if join:
        for j in join:
            query = query.add_entity(j["table"])
            for col in j["on"]:
                query = query.filter(getattr(data_table, col) == getattr(j["table"], col))
                
    query = query.group_by(data_table.year)

    # handle year (if specified)
    if "year" in kwargs:
        ret["year"] = parse_years(kwargs["year"])
        query = query \
            .filter(data_table.year.in_(ret["year"]))
        
    # parse all filters
    for key in check_keys:
        if key in kwargs:
            if key != "bra_id":
                unique_keys.append(key)
            if "show" in kwargs[key]:
                show_id = key
            parse_results = parse_filter(kwargs,key,query,data_table,ret)
            query = parse_results["query"]
            ret = parse_results["ret"]
            
    if filter:
        query = query.filter(ops[filter[1]](getattr(data_table, filter[0]), float(filter[2])))
        
    if excluding:
        for e in excluding:
            query = query.filter(not_(getattr(data_table, e).startswith(excluding[e])))
        
    # lastly we want to get the actual data held in the table requested
    if "aggregate" not in ret:
        # handle ordering
        if order:
            direction = "asc"
            
            if "." in order:
                o, direction = order.split(".")
            else:
                o = order
                
            order_table = None
            if join:
                for j in join:
                    if o in j["columns"]:
                        order_table = j["table"]
                
            if order_table == None:
                order_table = data_table
                
            if direction == "asc":
                query = query.order_by(asc(getattr(order_table,o)))
            elif direction == "desc":
                query = query.order_by(desc(getattr(order_table,o)))
                
        if limit:
            query = query.limit(limit).offset(offset)
    
    if join:
        ret["data"] = []
        items = query.all()
        for row in items:
            datum = row[0].serialize()
            join_data = []
            for i, r in enumerate(row):
                if i != 0:
                    serialized = r.serialize()
                    for k in serialized:
                        if k in join[i-1]["columns"]:
                            datum[k] = serialized[k]
            ret["data"].append(datum)
    elif raw:
        return query.all()
    else:
        ret["data"] = [d.serialize() for d in query.all()]
    
    if "aggregate" in ret:
            
        agg_data = []
        ret["data"] = sorted(ret["data"],key=lambda x: x["year"])
        for bra in ret["bra"]:
            if "aggregates" in bra:
                filtered_objs = []
                for key, group in groupby(ret["data"],lambda x: x["year"]):
                    year_data = []
                    for obj in group:
                        if obj["bra_id"] in bra["aggregates"]:
                            year_data.append(obj)
                            
                    if len(unique_keys) > 0:
                        
                        def check_filter(d,keys,i):
                            if i == len(keys):
                                merged_data = merge_objects(d)
                                merged_data["year"] = key
                                merged_data["bra_id"] = bra["id"]
                                agg_data.append(merged_data)
                            else:
                                d = sorted(d,key=lambda x: x[keys[i]])
                                for x, g in groupby(d,lambda x: x[keys[i]]):
                                    new_array = []
                                    for o in g:
                                        new_array.append(o)
                                    check_filter(new_array,keys,i+1)
                                    
                        check_filter(year_data,unique_keys,0)
                    else:
                        merged_data = merge_objects(year_data)
                        merged_data["year"] = key
                        merged_data["bra_id"] = bra["id"]
                        agg_data.append(merged_data)
            else:
                bra_data = [obj for obj in ret["data"] if obj["bra_id"] == bra["id"]]
                agg_data = agg_data + bra_data
        ret["data"] = agg_data

        # handle ordering
        if order:
            direction = "asc"
            if "." in order:
                o, direction = order.split(".")
            else:
                o = order
            if direction == "asc":
                ret["data"].sort(key=lambda x: x[o] if o in x else None)
            elif direction == "desc":
                ret["data"].sort(key=lambda x: x[o] if o in x else None, reverse=True)
        
        if limit:
            ret["data"] = ret["data"][int(offset):int(offset)+int(limit)]

    if cols:
        cols = ["year","bra_id"]+unique_keys+cols
        new_return = []
        attrs = None
        if ("name" or "id_ibge" or "id_mdic" in cols) and show_id:
            attr_table = locals()[show_id.split("_")[0].title()]
            attrs = [x.serialize() for x in attr_table.query.all()]
            attrs = {x["id"]:x or None for x in attrs}
        for d in ret["data"]:
            new_obj = {}
            for k in d:
                if k in cols:
                    new_obj[k] = d[k]
            if attrs:
                if "name" in cols and "name_{0}".format(lang) in attrs[d[show_id]]:
                    new_obj["name"] = attrs[d[show_id]]["name_{0}".format(lang)]
                if "id_ibge" in cols and "id_ibge" in attrs[d[show_id]]:
                    new_obj["id_ibge"] = attrs[d[show_id]]["id_ibge"]
                if "id_mdic" in cols and "id_mdic" in attrs[d[show_id]]:
                    new_obj["id_mdic"] = attrs[d[show_id]]["id_mdic"]
            new_return.append(new_obj)
        ret["data"] = new_return
        
    if order:
        for i, d in enumerate(ret["data"]):
            r = i+1
            if offset:
                r = r+offset
            d["rank"] = int(r)
    
    if download is not None:
        header = [str(c).split(".")[1] for c in data_table.__table__.columns]
        if cols:
            stickies = [c for c in header if c in unique_keys]
            header = stickies+cols
            
        def generate():
            for i, data_dict in enumerate(ret["data"]):
                row = [str(data_dict[c]) if c in data_dict else '' for c in header]
                if i == 0:
                    yield ','.join(header) + '\n' + ','.join(row) + '\n'
                yield ','.join(row) + '\n'

        content_disposition = "attachment;filename=%s.csv" % (cache_id[1:-1].replace('/', "_"))
        
        if sys.getsizeof(ret["data"]) > 10485760:
            resp = Response(['Unable to download, request is larger than 10mb'], 
                            mimetype="text/csv;charset=UTF-8", 
                            headers={"Content-Disposition": content_disposition})
        else:
            resp = Response(generate(), mimetype="text/csv;charset=UTF-8", 
                            headers={"Content-Disposition": content_disposition})
        return resp

    # gzip and jsonify result
    ret = gzip_data(jsonify(ret).data)

    if limit is None and download is None and raw is None and cols is None:
        cached_query(cache_id, ret)

    return ret