# -*- coding: utf-8 -*-
import urllib2
import json
from datetime import datetime
from itertools import groupby
from sqlalchemy import func
from flask import Blueprint, request, render_template, g, Response, make_response, send_file, jsonify, redirect, url_for

from dataviva import db, __year_range__
from dataviva.apps.general.views import get_locale
from dataviva.utils.make_query import make_query
from dataviva.apps.account.models import User, Starred
from dataviva.apps.graphs.models import UI
from dataviva.api.rais.models import Yb_rais, Yi, Yo
from dataviva.api.secex.models import Ymb, Ymp, Ymw
from dataviva.api.hedu.models import Yu, Yc_hedu
from dataviva.api.sc.models import Yc_sc
from dataviva.api.attrs.models import Yb

import json

mod = Blueprint('rankings', __name__, url_prefix='/<lang_code>/rankings')

@mod.before_request
def before_request():
    g.page_type = mod.name
    g.color = "#752277"

@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())

@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')

@mod.after_request
def per_request_callbacks(response):
    if hasattr(g,"json"):
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = str(len(response.data))
    return response

@mod.route('/')
@mod.route('/<year>/<type>/<depth>/')
def index(year=2012,type="bra",depth=3):

    def parse_years(ys):
        ys = [int(y.split("-")[0]) for y in ys]
        return range(ys[0], ys[1]+1)

    all_years = {k: parse_years(v) for k, v in __year_range__.iteritems()}

    def get_years(t):
        if t == "bra":
            years_rais = all_years["rais"]
            years_secex = all_years["secex"]
            return years_secex + list(set(years_rais) - set(years_secex))
        elif t == "cnae" or t == "cbo":
            return all_years["rais"]
        elif t == "hs" or t == "wld":
            return all_years["secex"]
        elif t == "university" or t == "course_hedu":
            return all_years["hedu"]
        elif t == "school" or t == "course_sc":
            return all_years["sc"]

    years = get_years(type)
    year = int(year)

    if year not in years:
        year = years[-1]

    depths = {}
    depths["bra"] = [1,3,5,7,9]
    depths["cnae"] = [1,3,6]
    depths["cbo"] = [1,4]
    depths["hs"] = [2,6]
    depths["wld"] = [2,5]
    depths["course_hedu"] = [2,6]
    depths["university"] = [5]
    depths["course_sc"] = [2,5]

    latest_year = {}
    for k in depths:
        latest_year[k] = get_years(k)[-1]

    order = {}
    order["bra"] = "export_val"
    order["cnae"] = "wage_avg"
    order["cbo"] = "wage_avg"
    order["hs"] = "export_val"
    order["wld"] = "export_val"
    order["university"] = "enrolled"
    order["course_hedu"] = "enrolled"
    order["course_sc"] = "enrolled"

    order = request.args.get("order","{0}.desc".format(order[type]))

    return render_template("rankings/index.html",type = type, depths = depths[type], depth = int(depth), year = year, years = years, order = order, latest_year = latest_year)

@mod.route('/table/<year>/<type>/<depth>/')
def table(year=None,type="bra",depth=None):
    g.page_type = "rankings"

    data_url = "/rankings/data/{0}/{1}/{2}/".format(year,type,depth)
    return render_template("general/table.html",data_url = data_url)

@mod.route('/data/<year>/<type>/<depth>/')
def data(year=None, type="bra", depth=None):

    g.json = True

    args = {}
    args["{0}_id".format(type)] = u"show.{0}".format(depth)
    args["year"] = year

    request_args = dict(request.args)
    request_args = {x:request_args[x][0] for x in request_args}

    if type == "bra":
        request_args["excluding"] = {"bra_id": "xx"}
        request_args["cols"] = ["bra_id","id_ibge","name","wage","wage_avg","export_val","import_val","population","eci","hs_diversity","hs_diversity_eff","cnae_diversity","cnae_diversity_eff"]
        args["join"] = []
        ry = [int(y) for y in __year_range__["rais"]]
        ry = range(ry[0], ry[1]+1)
        if int(year) in ry:
            args["join"].append({
                "table": Yb_rais,
                "columns": ["wage","wage_avg","cnae_diversity","cnae_diversity_eff"],
                "on": ["year","bra_id"]
            })
        py = [int(y) for y in __year_range__["population"]]
        py = range(py[0], py[1]+1)
        if int(year) in py:
            args["join"].append({
                "table": Yb,
                "columns": ["population"],
                "on": ["year","bra_id"]
            })
        table = Ymb
    elif type == "cnae":
        request_args["excluding"] = {"cnae_id": "xx"}
        request_args["cols"] = ["cnae_id","name","wage","wage_avg","num_jobs","num_jobs_est","cbo_diversity","cbo_diversity_eff"]
        table = Yi
    elif type == "cbo":
        request_args["excluding"] = {"cbo_id": "xx"}
        request_args["cols"] = ["cbo_id","name","wage","wage_avg","num_jobs","num_jobs_est","cnae_diversity","cnae_diversity_eff"]
        table = Yo
    elif type == "hs":
        request_args["excluding"] = {"hs_id": "xx"}
        request_args["cols"] = ["hs_id","name","export_val","import_val","pci","wld_diversity","wld_diversity_eff"]
        table = Ymp
    elif type == "wld":
        request_args["excluding"] = {"wld_id": "xx"}
        request_args["cols"] = ["wld_id","id_mdic","name","export_val","import_val","hs_diversity","hs_diversity_eff"]
        table = Ymw
    elif type == "university":
        request_args["excluding"] = {}
        request_args["cols"] = ["university_id","name","enrolled","graduates","entrants"]
        table = Yu
    elif type == "course_hedu":
        request_args["excluding"] = {"course_hedu_id": "00"}
        request_args["cols"] = ["course_hedu_id","name","enrolled","graduates","entrants"]
        table = Yc_hedu
    elif type == "course_sc":
        request_args["excluding"] = {"course_sc_id": "00"}
        request_args["cols"] = ["course_sc_id","name","enrolled","classes","age"]
        table = Yc_sc

    return make_response(make_query(table, request_args, g.locale, **args))
