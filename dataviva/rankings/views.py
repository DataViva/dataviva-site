# -*- coding: utf-8 -*- 
import urllib2
import json
from datetime import datetime
from itertools import groupby
from sqlalchemy import func
from flask import Blueprint, request, render_template, g, Response, make_response, send_file, jsonify, redirect, url_for

from dataviva import db
from dataviva.utils import make_query
from dataviva.data.forms import DownloadForm
from dataviva.account.models import User, Starred
from dataviva.apps.models import UI
from dataviva.rais.models import Yb_rais, Yi, Yo
from dataviva.secex.models import Yb_secex, Yp, Yw
from dataviva.attrs.models import Yb

from dataviva.utils import crossdomain

import json

mod = Blueprint('rankings', __name__, url_prefix='/rankings')

@mod.before_request
def before_request():
    g.page_type = mod.name
    g.color = "#752277"

@mod.after_request
def per_request_callbacks(response):
    if hasattr(g,"json"):
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = str(len(response.data))
    return response

@mod.route('/')
@mod.route('/<year>/<type>/<depth>/')
def index(year=2012,type="bra",depth=2):
    
    if type == "bra":
        years_rais = eval(UI.query.get(1).values)
        years_secex = eval(UI.query.get(2).values)
        years = years_secex + list(set(years_rais) - set(years_secex))
    elif type == "isic" or type == "cbo":
        years = eval(UI.query.get(1).values)
    elif type == "hs" or type == "wld":
        years = eval(UI.query.get(2).values)
        
    year = int(year)
        
    if year not in years:
        year = years[-1]
    
    depths = {}
    depths["bra"] = [2,4,7,8]
    depths["isic"] = [1,3,5]
    depths["cbo"] = [1,2,4]
    depths["hs"] = [2,4,6]
    depths["wld"] = [2,5]
    return render_template("rankings/index.html",type = type, depths = depths[type], depth = int(depth), year = year, years = years)

@mod.route('/table/<year>/<type>/<depth>/')
def table(year=None,type="bra",depth=None):
    g.page_type = "table"
    
    data_url = "/rankings/data/{0}/{1}/{2}/".format(year,type,depth)
    return render_template("general/table.html",data_url = data_url)

@mod.route('/data/<year>/<type>/<depth>/')
def data(year=None,type="bra",depth=None):
    
    g.json = True
    
    args = {}
    args["{0}_id".format(type)] = u"show.{0}".format(depth)
    args["year"] = year
    
    request_args = dict(request.args)
    request_args = {x:request_args[x][0] for x in request_args}
    
    if type == "bra":
        request_args["cols"] = ["bra_id","wage","wage_avg","val_usd","population","hs_diversity","hs_diversity_eff","isic_diversity","isic_diversity_eff"]
        args["join"] = [{
                "table": Yb,
                "columns": ["population"],
                "on": ["year","bra_id"]
            }]
        if int(year) > 2001:
            args["join"].append({
                "table": Yb_rais,
                "columns": ["wage","wage_avg","isic_diversity","isic_diversity_eff"],
                "on": ["year","bra_id"]
            })
        table = Yb_secex
    elif type == "isic":
        request_args["cols"] = ["isic_id","wage","wage_avg","num_emp","num_emp_est","cbo_diversity","cbo_diversity_eff"]
        table = Yi
    elif type == "cbo":
        request_args["cols"] = ["cbo_id","wage","wage_avg","num_emp","num_emp_est","isic_diversity","isic_diversity_eff"]
        table = Yo
    elif type == "hs":
        request_args["cols"] = ["hs_id","val_usd","pci","wld_diversity","wld_diversity_eff"]
        table = Yp
    elif type == "wld":
        request_args["cols"] = ["wld_id","val_usd","hs_diversity","hs_diversity_eff"]
        table = Yw
        
    return make_response(make_query(table, request_args, **args))