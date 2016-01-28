# -*- coding: utf-8 -*-
import urllib2
import json
from datetime import datetime as dt
from sqlalchemy import func
from flask import Blueprint, request, render_template, g, Response, make_response, send_file, jsonify, redirect, url_for
from flask.ext.babel import gettext as _

from dataviva import db, view_cache, __year_range__
from dataviva.utils.cached_query import cached_query, api_cache_key
from dataviva.translations.dictionary import dictionary

from dataviva.apps.account.models import User, Starred
from dataviva.apps.general.views import get_locale
from dataviva.apps.graphs.models import UI
from dataviva.api.attrs.models import Bra, Wld, Hs, Cnae, Cbo, University, Course_hedu, Course_sc


mod = Blueprint('data', __name__, url_prefix='/<lang_code>/data')

@mod.before_request
def before_request():
    g.page_type = mod.name
    g.color = "#1abbee"

@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())

@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')

def get_geo_location(ip):
    req = urllib2.Request("http://freegeoip.net/json/" + ip)
    opener = urllib2.build_opener()
    try:
        f = opener.open(req)
    except:
        return None
    json_resp = json.loads(f.read())
    city = json_resp["city"]
    # city = "Viana"
    state = json_resp["region_name"]
    # state = "Espírito Santo"
    # state = "Maranhão"

    # first try to find the exact city within the state
    bra_state = Bra.query.filter_by(name_pt=state).filter(func.char_length(Bra.id) == 2).first()
    bra_cities = Bra.query.filter_by(name_pt=city).filter(func.char_length(Bra.id) == 9)
    if bra_state:
        if bra_cities.count() == 1:
            return bra_cities.first()
        elif bra_cities.count() > 1:
            return bra_cities.filter(Bra.id.like(bra_state.id+'%')).first()
        return None
    return None

@mod.route('/table/')
@mod.route('/table/<data_type>/<year>/<bra_id>/<filter_1>/')
@mod.route('/table/<data_type>/<year>/<bra_id>/<filter_1>/<filter_2>/')
def table(data_type="rais", year="all", bra_id="4mg", filter_1="show.1", filter_2="all"):
    g.page_type = "table"
    data_url = "/{}/{}/{}/{}/{}/".format(data_type,year,bra_id,filter_1,filter_2)
    return render_template("general/table.html",data_url = data_url)

@mod.route('/')
@mod.route('/<data_type>/<year>/<bra_id>/<filter_1>/')
@mod.route('/<data_type>/<year>/<bra_id>/<filter_1>/<filter_2>/')
@view_cache.cached(key_prefix=api_cache_key("dataviewer"))
def index(data_type="rais", year="all", bra_id=None, filter_1=None, filter_2=None):
    # /hedu/all/show.3/01298.show.5/all/

    def get_filter_by_id(f):
        match = [v for v in filters if v["id"] == f]
        if match:
            return match[0]
        return None

    datasets = [["rais", _('Wages and Employment')],
                ["secex", _('International Trade')],
                ["hedu", _('Higher Education')],
                ["sc", _('School Census')]]
    for d in datasets:
        start_year, end_year = __year_range__[d[0]]
        years = reversed(range(int(start_year.split("-")[0]), int(end_year.split("-")[0])+1))
        d.append(years)
        if "-" in start_year:
            months = range(int(start_year.split("-")[1]), int(end_year.split("-")[1])+1)
            months = [(m, dt.strptime(str(m),"%m").strftime("%B")) for m in months]
            d.append(months)

    trans_lookup = dictionary()
    filters = [
        {"id": "bra", "datasets": "rais secex hedu sc", "nestings": [1, 3, 5, 7, 9]},
        {"id": "cbo", "datasets": "rais", "nestings":[1, 4]},
        {"id": "cnae", "datasets": "rais", "nestings":[1, 3, 6]},
        {"id": "hs", "datasets": "secex", "nestings":[2, 6]},
        {"id": "wld", "datasets": "secex", "nestings":[2, 5]},
        {"id": "university", "datasets": "hedu", "nestings":[5]},
        {"id": "course_hedu", "datasets": "hedu", "nestings":[2, 6]},
        {"id": "course_sc", "datasets": "sc", "nestings": [2, 5]}
    ]
    for f in filters:
        if "nestings" in f:
            if "bra" in f["id"]:
                attr_type = f["id"].replace("_r", "").replace("_s", "")
            else:
                attr_type = f["id"]
            f["nestings"] = [(n, trans_lookup["{}_{}".format(attr_type, n)]) for n in f["nestings"]]
            f["name"] = trans_lookup[f["id"]]

    selected_filters = []

    '''
        Determine the selected dataset/filters/output from URL
    '''
    output = {"filters":[]}

    # get selected dataset
    output["dataset"] = [v for v in datasets if v[0] == data_type][0]

    # get filters
    filter_type_lookup = {
        "rais": [("bra", Bra), ("cnae", Cnae), ("cbo", Cbo)],
        "secex": [("bra", Bra), ("hs", Hs), ("wld", Wld)],
        "hedu": [("bra", Bra), ("university", University), ("course_hedu", Course_hedu)],
        "sc": [("bra", Bra), None, ("course_sc", Course_sc)]
    }

    # parse year
    if year == "all":
        output["year"] = year
    elif "-" in year:
        y, m = year.split("-")
        if y != "all":
            output["year"] = int(y)
        else:
            output["year"] = y
        output["month"] = int(m)
    else:
        output["year"] = int(year)

    if bra_id and filter_1:
        for i, f in enumerate([bra_id, filter_1, filter_2]):
            filter = f
            depth = None
            if f == "all" or f is None: continue
            if f == "show": filter = None
            if "show" in f:
                output_filter = filter_type_lookup[output["dataset"][0]][i][0]
                output["output_filter"] = get_filter_by_id(output_filter)
            if "." in f:
                f_split = f.split(".")
                if len(f_split) == 3:
                    filter, show, depth = f_split
                if len(f_split) == 2:
                    filter = None
                    show, depth = f_split
            if depth:
                output["nesting"] = int(depth)
            if filter:
                filter_type = filter_type_lookup[output["dataset"][0]][i]
                possible_datasets = get_filter_by_id(filter_type[0])["datasets"]
                filter = filter_type[1].query.get(filter)
                output["filters"].append({"id":filter_type[0], "datasets":possible_datasets, "filter":filter})
    else:
        output["output_filter"] = get_filter_by_id("bra")
        output["nesting"] = 9
        filter = Bra.query.get("4mg")
        output["filters"].append({"id":"bra", "datasets":"rais secex hedu sc", "filter":filter})

    # raise Exception(output["dataset"], datasets, output["dataset"] == datasets[0])
    return render_template("data/index.html", datasets=datasets, filters=filters, selected_filters=selected_filters, output=output)
