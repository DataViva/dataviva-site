import urllib2

from sqlalchemy import func, distinct, asc, desc, and_, or_
from flask import Blueprint, request, jsonify, abort, g, render_template, make_response, redirect, url_for, flash

from dataviva import db, __year_range__, view_cache
from dataviva.attrs.models import Bra, Wld, Hs, Cnae, Cbo, Yb, Course_hedu, Course_sc, University, School, bra_pr, Search
from dataviva.secex.models import Ymp, Ymw
from dataviva.rais.models import Yi, Yo
from dataviva.hedu.models import Yu, Yc_hedu
from dataviva.sc.models import Yc_sc, Ys, Ybs
from dataviva.ask.models import Question

from dataviva.utils.gzip_data import gzip_data
from dataviva.utils.cached_query import cached_query
from dataviva.utils.exist_or_404 import exist_or_404
from dataviva.utils.title_case import title_case
from sqlalchemy import desc
from dataviva.utils.gzip_data import gzipped
from dataviva.utils.cached_query import api_cache_key

mod = Blueprint('attrs', __name__, url_prefix='/attrs')

@mod.errorhandler(404)
def page_not_found(error):
    return error, 404

def fix_name(attr, lang):

    for col in ["desc", "name", "gender", "article", "keywords"]:
        # raise Exception("{}_{}".format(col, lang) in attr)
        if "{}_{}".format(col, lang) in attr:
            attr[col] = title_case(attr["{}_{}".format(col, lang)])
        else:
            attr[col] = False
        if "{}_en".format(col) in attr: del attr["{}_en".format(col)]
        if "{}_pt".format(col) in attr: del attr["{}_pt".format(col)]

    school_type_lang = "school_type_" + lang
    if school_type_lang in attr:
        attr["school_type"] = attr[school_type_lang]
    if "school_type_en" in attr: del attr["school_type_en"]
    if "school_type_pt" in attr: del attr["school_type_pt"]

    if "is_vocational" in attr: del attr["is_vocational"]
    return attr

############################################################
# ----------------------------------------------------------
# All attribute views
#
############################################################
def get_planning_region_map():
    prs = db.session.query(bra_pr).all()
    pr_map = {k:v for k,v in prs}
    return pr_map

@mod.route("/school/in/<bra_id>/")
@gzipped
@view_cache.cached(key_prefix=api_cache_key("attrs"))
def school_attrs(bra_id):
    results = db.engine.execute('''
        SELECT id, school_type_id, name_pt, color
        FROM attrs_school
        LEFT JOIN sc_ybs
        ON attrs_school.id=sc_ybs.school_id
        WHERE sc_ybs.bra_id = %s;
    ''', bra_id)

    data = [{'id': row[0], 'school_type_id': row[1], 'name': row[2], 'color': row[3], 'icon': '/static/img/icons/school/school_{}.png'.format(row[1].lower())} for row in results]

    return jsonify(data=data)

@mod.route('/<attr>/')
@mod.route('/<attr>/<Attr_id>/')
def attrs(attr="bra",Attr_id=None):

    Attr = globals()[attr.capitalize()]
    Attr_weight_mergeid = "{0}_id".format(attr)

    if attr == "bra":
        Attr_weight_tbl = Yb
        Attr_weight_col = "population"
    elif attr == "cnae":
        Attr_weight_tbl = Yi
        Attr_weight_col = "num_jobs"
    elif attr == "cbo":
        Attr_weight_tbl = Yo
        Attr_weight_col = "num_jobs"
    elif attr == "hs":
        Attr_weight_tbl = Ymp
        Attr_weight_col = "export_val"
    elif attr == "wld":
        Attr_weight_tbl = Ymw
        Attr_weight_col = "export_val"
    elif attr == "course_hedu":
        Attr_weight_tbl = Yc_hedu
        Attr_weight_col = "enrolled"
    elif attr == "university":
        Attr_weight_tbl = Yu
        Attr_weight_col = "enrolled"
    elif attr == "school":
        Attr_weight_tbl = Ys
        Attr_weight_col = "enrolled"
    elif attr == "course_sc":
        Attr_weight_tbl = Yc_sc
        Attr_weight_col = "enrolled"

    depths = {}
    depths["bra"] = [1,3,5,7,9]
    depths["cnae"] = [1,3,6]
    depths["cbo"] = [1,4]
    depths["hs"] = [2,6]
    depths["wld"] = [2,5]
    depths["course_hedu"] = [2,6]
    depths["university"] = [5]
    depths["course_sc"] = [2,5]
    depths["school"] = [8]

    depth = request.args.get('depth', None)
    order = request.args.get('order', None)
    offset = request.args.get('offset', None)
    limit = request.args.get('limit', None)
    if offset:
        offset = float(offset)
        limit = limit or 50
    elif limit:
        offset = float(0)

    lang = request.args.get('lang', None) or g.locale
    ret = {}
    dataset = "rais"
    if Attr == Wld or Attr == Hs:
        dataset = "secex"
    elif Attr == Course_hedu or Attr == University:
        dataset = "hedu"
    elif Attr == Course_sc or Attr == School:
        dataset = "sc"
    elif Attr == Bra:
        dataset = "population"

    cache_id = request.path + lang
    if depth:
        cache_id = cache_id + "/" + depth
    # first lets test if this query is cached
    cached_q = cached_query(cache_id)
    if cached_q and limit is None:
        ret = make_response(cached_q)
        ret.headers['Content-Encoding'] = 'gzip'
        ret.headers['Content-Length'] = str(len(ret.data))
        return ret

    # if an ID is supplied only return that
    if Attr_id:

        # the '.show.' indicates that we are looking for a specific nesting
        if ".show." in Attr_id:
            this_attr, ret["nesting_level"] = Attr_id.split(".show.")
            # filter table by requested nesting level
            attrs = Attr.query \
                    .filter(Attr.id.startswith(this_attr)) \
                    .filter(func.char_length(Attr.id) == ret["nesting_level"]).all()

        # the 'show.' indicates that we are looking for a specific nesting
        elif "show." in Attr_id:
            ret["nesting_level"] = Attr_id.split(".")[1]
            # filter table by requested nesting level
            attrs = Attr.query.filter(func.char_length(Attr.id) == ret["nesting_level"]).all()

        # the '.' here means we want to see all attrs within a certain distance
        elif "." in Attr_id:
            this_attr, distance = Attr_id.split(".")
            this_attr = Attr.query.get_or_404(this_attr)
            attrs = this_attr.get_neighbors(distance)

        else:
            attrs = [Attr.query.get_or_404(Attr_id)]

        ret["data"] = [fix_name(a.serialize(), lang) for a in attrs]
    # an ID/filter was not provided
    else:
        latest_year = __year_range__[dataset][-1]
        latest_month = False
        if "-" in latest_year:
            latest_year, latest_month = latest_year.split("-")
            latest_month = int(latest_month)
        latest_year = int(latest_year)

        conds = [getattr(Attr_weight_tbl,"{0}_id".format(attr)) == Attr.id, Attr_weight_tbl.year == latest_year]
        if latest_month:
            conds.append(Attr_weight_tbl.month == latest_month)

        query = db.session.query(Attr,Attr_weight_tbl).outerjoin(Attr_weight_tbl, and_(*conds))
        if Attr == School:
            query = query.filter(Attr.is_vocational == 1)


        if depth:
            query = query.filter(func.char_length(Attr.id) == depth)
        else:
            query = query.filter(func.char_length(Attr.id).in_(depths[attr]))

        if order:
            direction = "asc"

            if "." in order:
                o, direction = order.split(".")
            else:
                o = order

            if o == "name":
                o = "name_{0}".format(lang)

            if o == Attr_weight_col:
                order_table  = Attr_weight_tbl
            else:
                order_table = Attr

            if direction == "asc":
                query = query.order_by(asc(getattr(order_table,o)))
            elif direction == "desc":
                query = query.order_by(desc(getattr(order_table,o)))

        if limit:
            query = query.limit(limit).offset(offset)

        attrs_all = query.all()

        # just get items available in DB
        attrs_w_data = None
        if depth is None and limit is None:
            attrs_w_data = db.session.query(Attr, Attr_weight_tbl) \
                .filter(getattr(Attr_weight_tbl, Attr_weight_mergeid) == Attr.id) \
                .group_by(Attr.id)
            attrs_w_data = [a[0].id for a in attrs_w_data]

        attrs = []

        # all_planning_regions = {}

        for i, a in enumerate(attrs_all):
            b = a[0].serialize()
            if a[1]:
                c = a[1].serialize()
                if Attr_weight_col in c:
                    b[Attr_weight_col] = c[Attr_weight_col]
                else:
                    b[Attr_weight_col] = 0
            else:
                b[Attr_weight_col] = 0
            a = b
            if attrs_w_data:
                a["available"] = False
                if a["id"] in attrs_w_data:
                    a["available"] = True
            # if Attr_weight_col == "population" and len(a["id"]) == 9 and a["id"][:3] == "4mg":
            #     if not all_planning_regions:
            #         all_planning_regions = get_planning_region_map()
            #     if a["id"] in all_planning_regions:
            #         plr = all_planning_regions[a["id"]]
            #         a["plr"] = plr
            if order:
                a["rank"] = int(i+offset+1)
            if attr == "bra" and "id_ibge" not in a:
                a["id_ibge"] = False
            attrs.append(fix_name(a, lang))

        ret["data"] = attrs

    ret = jsonify(ret)
    ret.data = gzip_data(ret.data)

    if limit is None and cached_q is None:
        cached_query(cache_id, ret.data)

    ret.headers['Content-Encoding'] = 'gzip'
    ret.headers['Content-Length'] = str(len(ret.data))

    return ret

@mod.route('/table/<attr>/<depth>/')
def attrs_table(attr="bra",depth="2"):
    g.page_type = "attrs"
    data_url = "/attrs/{0}/?depth={1}".format(attr,depth)
    return render_template("general/table.html", data_url=data_url)

@mod.route('/search/<term>/')
@view_cache.cached(timeout=86400, key_prefix=api_cache_key("search"))
def attrs_search(term=None):
    result = []
    lang = request.args.get('lang', 'en') or g.locale
    name_col = Search.name_en if lang == 'en' else Search.name_pt
    profiles = Search.query.filter(name_col.like(u'%{}%'.format(term))).order_by(Search.weight.desc()).limit(20)
    result = [p.serialize(lang == "pt") for p in profiles]
    ret = jsonify({"activities":result})
    return ret
