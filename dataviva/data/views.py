# -*- coding: utf-8 -*-
import urllib2
import json
from datetime import datetime
from sqlalchemy import func
from flask import Blueprint, request, render_template, g, Response, make_response, send_file, jsonify, redirect, url_for

from dataviva import db, view_cache
from dataviva.account.models import User, Starred
from dataviva.attrs.models import Bra, Wld, Hs, Cnae, Cbo
from dataviva.apps.models import UI

from dataviva.utils.cached_query import cached_query, make_cache_key

import json

mod = Blueprint('data', __name__, url_prefix='/data')

@mod.before_request
def before_request():
    g.page_type = mod.name
    g.color = "#1abbee"

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
@mod.route('/table/<data_type>/<year>/<bra_id>/<filter_1>/<filter_2>/')
def table(data_type="rais", year="all", bra_id="4mg", filter_1="show.1", filter_2="all"):
    g.page_type = "table"
    data_url = "/{0}/{1}/{2}/{3}/{4}/".format(data_type,year,bra_id,filter_1,filter_2)
    return render_template("general/table.html",data_url = data_url)

@mod.route('/')
@mod.route('/<data_type>/<year>/<bra_id>/<filter_1>/<filter_2>/')
#@view_cache.cached(timeout=604800, key_prefix=make_cache_key)
def index(data_type="rais", year="all", bra_id=None, filter_1=None, filter_2=None):

    filters = {}
    filters["bra"] = {"items": [], "depths": [1,3,5,8,9]}
    filters["cnae"] = {"items": [], "depths": [1,3,6]}
    filters["cbo"] = {"items": [], "depths": [1,2,4]}
    filters["hs"] = {"items": [], "depths": [2,4,6]}
    filters["wld"] = {"items": [], "depths": [2,5]}
    filters["university"] = {"items": [], "depths": [5]}
    filters["course_hedu"] = {"items": [], "depths": [2,6]}
    filters["course_sc"] = {"items": [], "depths": [2,5]}
    filter_order = ["bra","cnae","cbo","hs","wld"]

    datasets = {"rais": {"filters": ["bra","cnae","cbo"], "years": 1},
                "secex_export": {"filters": ["bra","hs","wld"], "years": 2},
                "hedu": {"filters": ["bra","university","course_hedu"], "years": 1},
                "sc": {"filters": ["bra","course_sc"], "years": 1}}

    for d in datasets:
        datasets[d]["years"] = eval(UI.query.get(datasets[d]["years"]).values)
        if data_type == d:
            datasets[d]["active"] = 1
        else:
            datasets[d]["active"] = 0
        if year != "all":
            if int(year) in datasets[d]["years"]:
                datasets[d]["year"] = int(year)
            elif int(year) > datasets[d]["years"][-1]:
                datasets[d]["year"] = datasets[d]["years"][-1]
            elif int(year) < datasets[d]["years"][0]:
                datasets[d]["year"] = datasets[d]["years"][0]
        else:
            datasets[d]["year"] = "all"

    g.page_type = "query"
    filters_json = {}

    def parse_filter(list,type):
        table = globals()[type.capitalize()]
        ids = list.split("_")
        filters_json[type] = {}
        for id in ids:
            obj_split = id.split(".")
            obj = {}
            obj_id = obj_split[0]

            if obj_id == "show":
                filters[type]["active"] = True
                filters[type]["depth"] = float(obj_split[1])
                filters_json[type]["show"] = float(obj_split[1])
            else:
                obj["item"] = table.query.get_or_404(obj_id)
                if len(obj_split) == 3 and float(obj_split[2]) > len(obj_id):
                    obj["depth"] = obj_split[2]
                else:
                    obj["depth"] = str(len(obj_id))
                filters[type]["active"] = True
                filters[type]["depth"] = filters[type]["depths"][0]
                filters[type]["items"].append(obj)
                if len(obj_split) >= 2 and obj_split[1] != "show":
                    obj["kms"] = int(obj_split[1])
                    json_id = "distance".join([obj["item"].id,obj_split[1]])
                else:
                    obj["kms"] = 0
                    json_id = obj["item"].id
                filters_json[type][json_id] = obj["depth"]

    if not bra_id:
        '''try getting the user's ip address, since the live server is using
            proxy nginx, we need to use the "X-Forwarded-For" remote address
            otherwise this will always be 127.0.0.1 ie localhost'''
        # if not request.headers.getlist("X-Forwarded-For"):
        #     ip = request.remote_addr
        # else:
        #     ip = request.headers.getlist("X-Forwarded-For")[0]

        # next try geolocating the user's ip
        # bra = get_geo_location(ip) or None

        '''if the city or region is not found in the db use Belo Horizonte as
            default'''
        bra_id = "4mg.show.8"
        # if not bra:
        #     bra_id = "4mg.show.8"
        # else:
        #     bra_id = bra.id

    parse_filter(bra_id,"bra")

    if filter_1 and filter_1 != "all":
        if data_type == "rais":
            parse_filter(filter_1,"cnae")
        elif data_type.startswith("secex"):
            parse_filter(filter_1,"hs")
        elif data_type == "hedu":
            parse_filter(filter_1,"university")

    if filter_2 and filter_2 != "all":
        if data_type == "rais":
            parse_filter(filter_2,"cbo")
        elif data_type.startswith("secex"):
            parse_filter(filter_2,"wld")
        elif data_type == "hedu":
            parse_filter(filter_2,"course_hedu")
        elif data_type == "sc":
            parse_filter(filter_2,"course_sc")

    for f in filters:
        if f not in filters_json:
            filters_json[f] = {"active": 0, "show": filters[f]["depths"][0]}
        else:
            if "show" not in filters_json[f]:
                filters_json[f]["show"] = filters[f]["depths"][0]
            if len(filters_json[f]) == 0:
                filters_json[f]["active"] = 0
            else:
                filters_json[f]["active"] = 1

    return render_template("data/index.html",
        datasets = datasets, filters = filters, filter_order = filter_order, filters_json = json.dumps(filters_json))
