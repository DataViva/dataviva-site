import StringIO, csv, sys
from sqlalchemy import func
from flask import Blueprint, request, render_template, flash, g, session, \
            redirect, url_for, jsonify, make_response, Response
from visual import db
from visual.utils import exist_or_404, gzip_data, cached_query, parse_years, Pagination
from visual.rais.models import Yb_rais, Yi, Yo, Ybi, Ybo, Yio, Ybio
from visual.attrs.models import Bra, Isic, Cbo

mod = Blueprint('rais', __name__, url_prefix='/rais')

RESULTS_PER_PAGE = 40

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
    if ".show." in bra_str:
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

def get_query(data_table, url_args, **kwargs):
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
    join = kwargs["join"] if "join" in kwargs else False
    cache_id = request.path
    ret = {}
    
    # first lets test if this query is cached
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
    
    # handle year (if specified)
    if "year" in kwargs:
        ret["year"] = parse_years(kwargs["year"])
        # filter query
        query = query.filter(data_table.year.in_(ret["year"]))

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
                query = query.filter(data_table.bra_id.in_([g["id"] for g in ret["location"]]))
            else:
                query = query.filter(data_table.bra_id == ret["location"][0]["id"])
    
    # handle industry (if specified)
    if "isic_id" in kwargs:
        if "show." in kwargs["isic_id"]:
            # the '.' indicates that we are looking for a specific bra nesting
            ret["isic_level"] = kwargs["isic_id"].split(".")[1]
            # filter table by requested nesting level
            query = query.filter(func.char_length(data_table.isic_id) == ret["isic_level"])
        elif "show" not in kwargs["isic_id"]:
            # we allow the user to specify industries separated by '+'
            ret["industry"] = kwargs["isic_id"].split("+")
            # Make sure the isic_id requested actually exists in the DB
            ret["industry"] = [exist_or_404(Isic, isic_id).serialize() for isic_id in ret["industry"]]
            # filter query
            if len(ret["industry"]) > 1:
                query = query.filter(data_table.isic_id.in_([i["id"] for i in ret["industry"]]))
            else:
                query = query.filter(data_table.isic_id == ret["industry"][0]["id"])

    # handle industry (if specified)
    if "cbo_id" in kwargs:
        if "show." in kwargs["cbo_id"]:
            # the '.' indicates that we are looking for a specific bra nesting
            ret["cbo_level"] = kwargs["cbo_id"].split(".")[1]
            # filter table by requested nesting level
            query = query.filter(func.char_length(data_table.cbo_id) == ret["cbo_level"])
        # make sure the user does not want to show all occupations
        if "show" not in kwargs["cbo_id"]:
            # we allow the user to specify occupations separated by '+'
            ret["occupation"] = kwargs["cbo_id"].split("+")
            # Make sure the cbo_id requested actually exists in the DB
            ret["occupation"] = [exist_or_404(Cbo, cbo_id).serialize() for cbo_id in ret["occupation"]]
            # filter query
            if len(ret["occupation"]) > 1:
                query = query.filter(data_table.cbo_id.in_([o["id"] for o in ret["occupation"]]))
            else:
                query = query.filter(data_table.cbo_id == ret["occupation"][0]["id"])
    
    # handle ordering
    if order:
        for o in order:
            direction = "desc"
            if "." in o:
                o, direction = o.split(".")
            if o == "bra":
                # order by bra
                query = query.join(Bra).order_by(Bra.name_en)
            elif o == "isic":
                # order by isic
                query = query.join(Isic).order_by(Isic.name_en)
            elif o == "cbo":
                # order by cbo
                query = query.join(Cbo).order_by(Cbo.name_en)
            else:
                query = query.order_by(getattr(data_table, o) + " " + direction)
    
    # lastly we want to get the actual data held in the table requested
    if join:
        # items = query.paginate(int(kwargs["page"]), RESULTS_PER_PAGE, False).items
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
        '''if the output is larger than 6 mb rais error'''
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
def rais_yb(**kwargs):
    return make_response(get_query(Yb_rais, request.args, **kwargs))

@mod.route('/all/all/<isic_id>/all/')
@mod.route('/<year>/all/<isic_id>/all/')
def rais_yi(**kwargs):
    return make_response(get_query(Yi, request.args, **kwargs))

@mod.route('/all/all/all/<cbo_id>/')
@mod.route('/<year>/all/all/<cbo_id>/')
def rais_yo(**kwargs):
    return make_response(get_query(Yo, request.args, **kwargs))

############################################################
# ----------------------------------------------------------
# 3 variable views
# 
############################################################

@mod.route('/all/<bra_id>/<isic_id>/all/')
@mod.route('/<year>/<bra_id>/<isic_id>/all/')
def rais_ybi(**kwargs):
    
    kwargs["join"] = {
                        "table": Yi.ici,
                        "columns": {"ici": Yi.ici},
                        "on": ('year', 'isic_id')
                    }
    return make_response(get_query(Ybi, request.args, **kwargs))

@mod.route('/recommended/<bra_id>/<isic_id>/all/')
def rais_ybi_recommended(**kwargs):
    raise Exception(get_recommended(Ybi, request.args, **kwargs))

@mod.route('/all/<bra_id>/all/<cbo_id>/')
@mod.route('/<year>/<bra_id>/all/<cbo_id>/')
def rais_ybo(**kwargs):
    return make_response(get_query(Ybo, request.args, **kwargs))

@mod.route('/all/all/<isic_id>/<cbo_id>/')
@mod.route('/<year>/all/<isic_id>/<cbo_id>/')
def rais_yio(**kwargs):
    return make_response(get_query(Yio, request.args, **kwargs))

############################################################
# ----------------------------------------------------------
# 4 variable views
# 
############################################################

@mod.route('/all/<bra_id>/<isic_id>/<cbo_id>/')
@mod.route('/<year>/<bra_id>/<isic_id>/<cbo_id>/')
def rais_ybio(**kwargs):
    return make_response(get_query(Ybio, request.args, **kwargs))