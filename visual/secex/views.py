import re, operator, sys
from sqlalchemy import func
from flask import Blueprint, request, render_template, flash, g, session, \
            redirect, url_for, jsonify, abort, make_response, Response
from visual import db
from visual.utils import exist_or_404, gzip_data, cached_query, parse_years, Pagination
from visual.attrs.models import Bra, Hs, Wld
from visual.secex.models import Yb_secex, Yw, Yp, Ybw, Ybp, Ypw, Ybpw

mod = Blueprint('secex', __name__, url_prefix='/secex')

RESULTS_PER_PAGE = 40
ops = {">": operator.gt,
       ">=": operator.ge,
       "<": operator.lt,
       "<=": operator.le}

@mod.errorhandler(404)
def page_not_found(error):
    return error, 404

@mod.after_request
def per_request_callbacks(response):
    if response.status_code != 302 and response.mimetype != "text/csv":
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = str(len(response.data))
    return response

''' Given a "bra" string from URL, turn this into an array of Bra
    objects'''
def parse_bras(bra_str):
    if "mgpr" in bra_str:
        planning_region = Bra.query.get(bra_str)
        bras = [b.serialize() for b in planning_region.pr.all()]
    elif ".show." in bra_str:
        # the '.show.' indicates that we are looking for a specific nesting
        bar_id, nesting = bra_str.split(".show.")
        # filter table by requested nesting level
        bras = Bra.query \
                .filter(Bra.id.startswith(bra_id)) \
                .filter(func.char_length(Attr.id) == nesting).all()
        bras = [b.serialize() for b in bras]
    elif "." in bra_str:
        # the '.' indicates we are looking for bras within a given distance
        bra_id, distance = bra_str.split(".")
        bras = exist_or_404(Bra, bra_id)
        neighbors = bras.get_neighbors(distance)
        bras = [g.bra.serialize() for g in neighbors]
    else:
        # we allow the user to specify bras separated by '+'
        bras = bra_str.split("+")
        # Make sure the bra_id requested actually exists in the DB
        bras = [exist_or_404(Bra, bra_id).serialize() for bra_id in bras]
    return bras

agg = {'val_usd':func.sum, 'eci':func.avg, 'eci_wld':func.avg, 'pci':func.avg,
        'val_usd_growth_pct':func.avg, 'val_usd_growth_pct_5':func.avg, 
        'val_usd_growth_val':func.avg, 'val_usd_growth_val_5':func.avg,
        'distance':func.avg, 'distance_wld':func.avg,
        'opp_gain':func.avg, 'opp_gain_wld':func.avg,
        'rca':func.avg, 'rca_wld':func.avg}

def make_query(data_table, url_args, **kwargs):
    query = data_table.query
    download = url_args.get("download", None)
    raw = True if "raw" in kwargs else None
    order = url_args.get("order", None)
    if order:
        order = url_args.get("order").split(" ")
    offset = url_args.get("offset", None)
    limit = url_args.get("limit", None)
    if offset:
        limit = limit or 50
    filter = url_args.get("filter", None)
    if filter:
        filter = re.split("(>=|>|<=|<)", filter)
    join = kwargs["join"] if "join" in kwargs else False
    cache_id = request.path
    ret = {}
    unique_keys = ["year", "hs_id", "wld_id"]

    # first lets test if this query is cached (be sure we are not paginating
    # results) as these should not get cached
    if limit is None and download is None and raw is None:
        cached_q = cached_query(cache_id)
        if cached_q:
            return cached_q

    if join:
        join_table = join["table"]
        # check if given a whole table of just a table's column
        if hasattr(join_table, 'parent'):
            join_table = join_table.parent.class_
        query = db.session.query(data_table, join["table"])
        for col in join["on"]:
            query = query.filter(getattr(data_table, col) == getattr(join_table, col))

    # handle location (if specified)
    if "bra_id" in kwargs:
        if "show." in kwargs["bra_id"]:
            # the '.' indicates that we are looking for a specific bra nesting
            ret["bra_level"] = kwargs["bra_id"].split("show.")[1]
            # filter table by requested nesting level
            query = query.filter(func.char_length(data_table.bra_id) == ret["bra_level"])
            if ".show." in kwargs["bra_id"]:
                bra_filter = kwargs["bra_id"].split(".show.")[0]
                if bra_filter != "all":
                    query = query \
                        .filter(data_table.bra_id.startswith(bra_filter))
        elif "show" not in kwargs["bra_id"]:
            # otherwise we have been given specific bra(s)
            ret["location"] = parse_bras(kwargs["bra_id"])
            # filter query
            if len(ret["location"]) > 1:
                col_names = [c.name for c in list(data_table.__table__.columns)]
                col_vals = [agg[c](getattr(data_table, c)) if c in agg else getattr(data_table, c) for c in col_names]
                if join:
                    col_names = join["columns"].keys() + col_names
                    col_vals.insert(0, join["table"])
                    query = db.session.query(*col_vals)
                    for col in join["on"]:
                        query = query.filter(getattr(data_table, col) == getattr(join_table, col))
                else:
                    query = db.session.query(*col_vals)
                query = query.filter(data_table.bra_id.in_([g["id"] for g in ret["location"]]))
            else:
                query = query.filter(data_table.bra_id == ret["location"][0]["id"])

    # handle year (if specified)
    if "year" in kwargs:
        ret["year"] = parse_years(kwargs["year"])
        # filter query
        query = query.filter(data_table.year.in_(ret["year"]))

    # handle industry (if specified)
    if "hs_id" in kwargs:
        if "show." in kwargs["hs_id"]:
            # the '.' indicates that we are looking for a specific bra nesting
            ret["hs_level"] = kwargs["hs_id"].split(".")[1]
            # filter table by requested nesting level
            query = query.filter(func.char_length(data_table.hs_id) == ret["hs_level"])
        # make sure the user does not want to show all occupations
        if "show" not in kwargs["hs_id"]:
            # we allow the user to specify occupations separated by '+'
            ret["product"] = kwargs["hs_id"].split("+")
            # Make sure the cbo_id requested actually exists in the DB
            ret["product"] = [exist_or_404(Hs, hs_id).serialize() for hs_id in ret["product"]]
            # filter query
            if len(ret["product"]) > 1:
                query = query.filter(data_table.hs_id.in_([p["id"] for p in ret["product"]]))
            else:
                query = query.filter(data_table.hs_id == ret["product"][0]["id"])
    else:
        unique_keys.remove('hs_id')

    # handle industry (if specified)
    if "wld_id" in kwargs:
        if "show." in kwargs["wld_id"]:
            # the '.' indicates that we are looking for a specific bra nesting
            ret["wld_level"] = kwargs["wld_id"].split(".")[1]
            # filter table by requested nesting level
            query = query.filter(func.char_length(data_table.wld_id) == ret["wld_level"])
        # make sure the user does not want to show all occupations
        if "show" not in kwargs["wld_id"]:
            # we allow the user to specify occupations separated by '+'
            ret["wld"] = kwargs["wld_id"].split("+")
            # Make sure the cbo_id requested actually exists in the DB
            ret["wld"] = [exist_or_404(Wld, wld_id).serialize() for wld_id in ret["wld"]]
            # filter query
            if len(ret["wld"]) > 1:
                query = query.filter(data_table.wld_id.in_([o["id"] for o in ret["wld"]]))
            else:
                query = query.filter(data_table.wld_id == ret["wld"][0]["id"])
    else:
        unique_keys.remove('wld_id')

    # handle ordering
    if order:
        for o in order:
            direction = "desc"
            if "." in o:
                o, direction = o.split(".")
            if o == "bra":
                # order by bra
                query = query.join(Bra).order_by(Bra.name_en)
            elif o == "hs":
                # order by product
                query = query.join(Hs).order_by(Hs.name_en)
            elif o == "wld":
                # order by wld
                query = query.join(Wld).order_by(Wld.name_en)
            else:
                query = query.order_by(o + " " + direction)

    if filter:
        query = query.filter(ops[filter[1]](getattr(data_table, filter[0]), float(filter[2])))

    # lastly we want to get the actual data held in the table requested
    if "location" in ret and len(ret["location"]) > 1:
        # raise Exception(unique_keys)
        for uk in unique_keys:
            query = query.group_by(getattr(data_table, uk))
        # raise Exception(join["columns"].keys())
        ret["data"] = [dict(zip(col_names, d)) for d in query.all()]
        # raise Exception(col_names, query.all()[0])
        # raise Exception(ret["data"])
    elif join:
        ret["data"] = []
        if limit:
            items = query.limit(limit).offset(offset).all()
        else:
            items = query.all()
        for row in items:
            datum = row[0].serialize()
            for value, col_name in zip(row[1:], join["columns"].keys()):
                extra = {}
                extra[col_name] = value
                datum = dict(datum.items() + extra.items())
            ret["data"].append(datum)
    elif limit:
        ret["data"] = [d.serialize() for d in query.limit(limit).offset(offset).all()]
    elif raw:
        return query.all()
    else:
        ret["data"] = [d.serialize() for d in query.all()]

    if download is not None:
        def generate():
            for i, data_dict in enumerate(ret["data"]):
                row = [str(n) if n is not None else '' for n in data_dict.values()]
                if i == 0:
                    header = data_dict.keys()
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

    if limit is None and download is None:
        cached_query(cache_id, ret)

    return ret

############################################################
# ----------------------------------------------------------
# 2 variable views
# 
############################################################

@mod.route('/all/<bra_id>/all/all/')
@mod.route('/<year>/<bra_id>/all/all/')
def secex_yb(**kwargs):
    return make_response(make_query(Yb_secex, request.args, **kwargs))

@mod.route('/all/all/<hs_id>/all/')
@mod.route('/<year>/all/<hs_id>/all/')
def secex_yp(**kwargs):
    return make_response(make_query(Yp, request.args, **kwargs))

@mod.route('/all/all/all/<wld_id>/')
@mod.route('/<year>/all/all/<wld_id>/')
def secex_yw(**kwargs):
    return make_response(make_query(Yw, request.args, **kwargs))

############################################################
# ----------------------------------------------------------
# 3 variable views
# 
############################################################

@mod.route('/all/<bra_id>/all/<wld_id>/')
@mod.route('/<year>/<bra_id>/all/<wld_id>/')
def secex_ybw(**kwargs):
    return make_response(make_query(Ybw, request.args, **kwargs))

@mod.route('/all/<bra_id>/<hs_id>/all/')
@mod.route('/<year>/<bra_id>/<hs_id>/all/')
def secex_ybp(**kwargs):
    kwargs["join"] = {
                        "table": Yp.pci,
                        "columns": {"pci": Yp.pci},
                        "on": ('year', 'hs_id')
                    }
    return make_response(make_query(Ybp, request.args, **kwargs))

@mod.route('/all/all/<hs_id>/<wld_id>/')
@mod.route('/<year>/all/<hs_id>/<wld_id>/')
def secex_ypw(**kwargs):
    return make_response(make_query(Ypw, request.args, **kwargs))

############################################################
# ----------------------------------------------------------
# 4 variable views
# 
############################################################

@mod.route('/all/<bra_id>/<hs_id>/<wld_id>/')
@mod.route('/<year>/<bra_id>/<hs_id>/<wld_id>/')
def secex_ybpw(**kwargs):
    return make_response(make_query(Ybpw, request.args, **kwargs))