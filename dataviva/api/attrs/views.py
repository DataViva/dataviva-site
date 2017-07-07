import gzip
import json
import requests
from StringIO import StringIO

from sqlalchemy import func, asc, desc, and_
from flask import (Blueprint, request, jsonify, g,
                   render_template, make_response, Response)

from dataviva import db, __year_range__, view_cache
from dataviva.api.attrs.models import Bra, Wld, Hs, Cnae, Cbo, Yb, Course_hedu, Course_sc, University, School, bra_pr, Search
from dataviva.api.attrs.mocks import attrs_datasets
from dataviva.api.secex.models import Ymp, Ymw
from dataviva.api.rais.models import Yi, Yo
from dataviva.api.hedu.models import Yu, Yc_hedu
from dataviva.api.sc.models import Yc_sc, Ys, Ybs
from dataviva.apps.ask.models import Question

from dataviva.utils.gzip_data import gzip_data
from dataviva.utils.cached_query import cached_query
from dataviva.utils.exist_or_404 import exist_or_404
from dataviva.utils.title_case import title_case
from sqlalchemy import desc
from dataviva.utils.gzip_data import gzipped
from dataviva.utils.cached_query import api_cache_key
from dataviva.translations.translate import translate

mod = Blueprint('attrs', __name__, url_prefix='/attrs')


def fix_name(attr, lang):

    for col in ["desc", "name", "gender", "article", "keywords"]:
        # raise Exception("{}_{}".format(col, lang) in attr)
        if "{}_{}".format(col, lang) in attr:
            attr[col] = title_case(attr["{}_{}".format(col, lang)])
        else:
            attr[col] = False
        if "{}_en".format(col) in attr:
            del attr["{}_en".format(col)]
        if "{}_pt".format(col) in attr:
            del attr["{}_pt".format(col)]

    school_type_lang = "school_type_" + lang
    if school_type_lang in attr:
        attr["school_type"] = attr[school_type_lang]
    if "school_type_en" in attr:
        del attr["school_type_en"]
    if "school_type_pt" in attr:
        del attr["school_type_pt"]

    if "is_vocational" in attr:
        del attr["is_vocational"]
    return attr

############################################################
# ----------------------------------------------------------
# All attribute views
#
############################################################


def get_planning_region_map():
    prs = db.session.query(bra_pr).all()
    pr_map = {k: v for k, v in prs}
    return pr_map


@mod.route("/school/")
@view_cache.cached(key_prefix=api_cache_key("attrs"))
def voc_schools():
    attrs = School.query.filter(School.is_vocational == 1).all()
    lang = request.args.get('lang', None) or g.locale
    data = [fix_name(a.serialize(), lang) for a in attrs]
    return jsonify(data=data)


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

    data = [{'id': row[0], 'school_type_id': row[1], 'name': row[2], 'color': row[3],
             'icon': '/static/img/icons/school/school_{}.png'.format(row[1].lower())} for row in results]

    return jsonify(data=data)


@mod.route('/<attr>/')
@mod.route('/<attr>/<Attr_id>/')
def attrs(attr="bra", Attr_id=None, depth=None):
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
    depths["bra"] = [1, 3, 5, 7, 9]
    depths["cnae"] = [1, 3, 6]
    depths["cbo"] = [1, 4]
    depths["hs"] = [2, 6]
    depths["wld"] = [2, 5]
    depths["course_hedu"] = [2, 6]
    depths["university"] = [5]
    depths["course_sc"] = [2, 5]
    depths["school"] = [8]

    depth = request.args.get('depth', depth)
    order = request.args.get('order', None)
    offset = request.args.get('offset', None)
    limit = request.args.get('limit', None)
    full_year = request.args.get('full_year', None)

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

    cache_id = "attrs:" + request.path + lang
    if depth:
        cache_id = cache_id + "/" + depth

    if full_year:
        cache_id = cache_id + "/full_year"

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

        # if secex, get last full year.
        conds = []
        if latest_month:
            conds = [Attr_weight_tbl.month == latest_month]
            if full_year:
                conds = [Attr_weight_tbl.month == '0']
                if latest_month != 12:
                    latest_year -= 1

        conds += [getattr(Attr_weight_tbl, "{0}_id".format(attr)) == Attr.id, Attr_weight_tbl.year == latest_year]

        query = db.session.query(Attr, Attr_weight_tbl).outerjoin(Attr_weight_tbl, and_(*conds))
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
                order_table = Attr_weight_tbl
            else:
                order_table = Attr

            if direction == "asc":
                query = query.order_by(asc(getattr(order_table, o)))
            elif direction == "desc":
                query = query.order_by(desc(getattr(order_table, o)))

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
            if attr == "bra":
                if "id_ibge" not in a:
                    a["id_ibge"] = False
                if "abbreviation" not in a:
                    a["abbreviation"] = False
            attrs.append(fix_name(a, lang))

        ret["data"] = attrs

    ret = jsonify(ret)
    ret.data = gzip_data(ret.data)

    if limit is None and cached_q is None:
        cached_query(cache_id, ret.data)

    ret.headers['Content-Encoding'] = 'gzip'
    ret.headers['Content-Length'] = str(len(ret.data))

    return ret


def wrapcsv(x):
    if "," in x or u"," in x:
        return u'"{}"'.format(x)
    return x


@mod.route('/download/', methods=['GET'])
def dl_csv():
    attr_type = request.args.get('attr_type')
    depth = request.args.get('depth')

    req = attrs(attr=attr_type, depth=depth)
    data = req.get_data()
    buf = StringIO(data)
    f = gzip.GzipFile(fileobj=buf)
    data = json.load(f)

    cvs = ""
    lineArray = []
    linesArray = []
    headerArray = []
    checkHeader = []

    for item in data['data']:
        for h in item:
            if h not in checkHeader:
                checkHeader.append(h)
                headerArray.append(wrapcsv(h))

    for item in data['data']:
        lineArray = []
        for header in checkHeader:
            if header in item:
                if (type(item[header]) is unicode):
                    lineArray.append(wrapcsv(item[header]))
                else:
                    lineArray.append(wrapcsv(str(item[header])))
            else:
                lineArray.append("")

        linesArray.append(','.join(lineArray))

    csv_str = ','.join(headerArray) + '\n' + '\n'.join(linesArray)

    response = make_response(csv_str)
    response.headers['Content-Disposition'] = "attachment; filename=dataviva_attr_{}_{}.csv".format(attr_type, depth)
    response.headers["Content-type"] = "text/csv"

    return response


@mod.route('/table/<attr>/<depth>/')
def attrs_table(attr="bra", depth="2"):
    g.page_type = "attrs"
    data_url = "{0}/attrs/{1}/?depth={2}".format(g.locale, attr, depth)
    return render_template("general/table.html", data_url=data_url)


@mod.route('/search/<term>/')
@view_cache.cached(key_prefix=api_cache_key("search"))
def attrs_search(term=None):
    result = []
    lang = request.args.get('lang', 'en') or g.locale
    name_col = Search.name_en if lang == 'en' else Search.name_pt
    profiles = Search.query.filter(name_col.like(u'%{}%'.format(term))).order_by(Search.weight.desc()).limit(20)
    result = [p.serialize(lang == "pt") for p in profiles]
    ret = jsonify({"activities": result})
    return ret


def collection_by_depth(base, depth=None):
    return db.session.query(base).filter(
        func.char_length(base.id) == depth
    )


@mod.route('/location/')
@view_cache.cached(key_prefix=api_cache_key("attrs_location"))
def location():

    depth = request.args.get('depth', None)
    if not depth:
        return Response("You must specify a querying parameter!", status=400)
    returned_entries = collection_by_depth(Bra, depth)

    return Response(
        json.dumps(map(lambda x: x.serialize(), returned_entries)),
        status=(200 if returned_entries.count() else 404)
    )


@mod.route('/product/')
@view_cache.cached(key_prefix=api_cache_key("attrs_product"))
def product():

    depth = request.args.get('depth', None)
    if not depth:
        return Response("You must specify a querying parameter!", status=400)
    returned_entries = collection_by_depth(Hs, depth)

    return Response(
        json.dumps(map(lambda x: x.serialize(), returned_entries)),
        status=(200 if returned_entries.count() else 404)
    )


@mod.route('/basic_course/')
@view_cache.cached(key_prefix=api_cache_key("attrs_basic_course"))
def basic_course():

    depth = request.args.get('depth', None)
    if not depth:
        return Response("You must specify a querying parameter!", status=400)
    returned_entries = collection_by_depth(Course_sc, depth)

    return Response(
        json.dumps(map(lambda x: x.serialize(), returned_entries)),
        status=(200 if returned_entries.count() else 404)
    )


@mod.route('/major/')
@view_cache.cached(key_prefix=api_cache_key("attrs_major"))
def major():

    depth = request.args.get('depth', None)
    if not depth:
        return Response("You must specify a querying parameter!", status=400)
    returned_entries = collection_by_depth(Course_hedu, depth)
    return Response(
        json.dumps(map(lambda x: x.serialize(), returned_entries)),
        status=(200 if returned_entries.count() else 404)
    )


@mod.route('/industry/')
@view_cache.cached(key_prefix=api_cache_key("attrs_industry"))
def industry():

    depth = request.args.get('depth', None)
    if not depth:
        return Response("You must specify a querying parameter!", status=400)
    returned_entries = collection_by_depth(Cnae, depth)

    return Response(
        json.dumps(map(lambda x: x.serialize(), returned_entries)),
        status=(200 if returned_entries.count() else 404)
    )


@mod.route('/occupation/')
@view_cache.cached(key_prefix=api_cache_key("attrs_occupation"))
def occupation():

    depth = request.args.get('depth', None)
    if not depth:
        return Response("You must specify a querying parameter!", status=400)
    returned_entries = collection_by_depth(Cbo, depth)

    return Response(
        json.dumps(map(lambda x: x.serialize(), returned_entries)),
        status=(200 if returned_entries.count() else 404)
    )


@mod.route('/trade_partner/')
@view_cache.cached(key_prefix=api_cache_key("attrs_trade_partner"))
def trade_partner():

    depth = request.args.get('depth', None)
    if not depth:
        return Response("You must specify a querying parameter!", status=400)
    returned_entries = collection_by_depth(Wld, depth)

    return Response(
        json.dumps(map(lambda x: x.serialize(), returned_entries)),
        status=(200 if returned_entries.count() else 404)
    )

@mod.route('/health_region/')
@view_cache.cached(key_prefix=api_cache_key("attrs_health_region"))
def health_region():
    r = requests.get('http://api.staging.dataviva.info/metadata/health_region')
    data = []
    response = r.json()
    lang = request.args.get('lang', 'pt')

    for key in response:
        region = {}
        region['id'] = key
        region['name'] = response[key]['name_' + lang]  
        region['color'] = '-'
        data.append(region)

    return Response(
        json.dumps({'data': data}),
        status=200
    )

@mod.route('/demographic_information/<attr>/')
@view_cache.cached(key_prefix=api_cache_key("attrs_demographic_information"))
def demographic_information(attr):
    r = requests.get('http://api.staging.dataviva.info/metadata/' + attr)
    data = []
    response = r.json()
    lang = request.args.get('lang', 'pt')

    for key in response:
        region = {}
        region['id'] = key
        region['name'] = response[key]['name_' + lang]
        data.append(region)

    return Response(
        json.dumps({'data': data}),
        status=200
    )

@mod.route('/establishment_information/<attr>/')
@view_cache.cached(key_prefix=api_cache_key("attrs_establishment_information"))
def establishment_information(attr):
    r = requests.get('http://api.staging.dataviva.info/metadata/' + attr)
    data = []
    response = r.json()
    lang = request.args.get('lang', 'pt')

    for key in response:
        region = {}
        region['id'] = key
        region['name'] = response[key]['name_' + lang]
        data.append(region)

    return Response(
        json.dumps({'data': data}),
        status=200
    )

@mod.route('/datasets/')
def datasets():
    return jsonify({'data': attrs_datasets})
