# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, g, url_for
from sqlalchemy import func, distinct

from dataviva import db
from dataviva.attrs import models as attrs
from dataviva.rais import models as rais
from dataviva.secex import models as secex

from dataviva.general.models import Plan
from dataviva.attrs.models import Bra, Isic, Cbo, Hs, Wld
from dataviva.rais.views import get_query as rais_get_query
from dataviva.rais.models import Ybi, Ybo, Yio
from dataviva.secex.views import make_query as secex_get_query
from dataviva.secex.models import Ybp, Ybw, Ypw

from dataviva.apps.models import Build, App

import time

mod = Blueprint('profiles', __name__, url_prefix='/profiles')

@mod.before_request
def before_request():
    t1 = time.time()
    g.page_type = mod.name
    g.path = request.path
    
    g.color = "#e0902d"
    
    t2 = time.time()
    g.timing.append("Before Profile: {0:.4f}s".format((t2-t1)))

@mod.route('/')
@mod.route('/<category>/select/')
def index(category = None, id = None):
    
    selector = category
    
    article = None
    
    if g.locale == "pt":
        if category == "cbo":
            article = "uma profissão"
        elif category == "isic":
            article = "uma indústria"
        elif category == "hs":
            article = "um produto"
        elif category == "bra":
            article = "um local"
        elif category == "wld":
            article = "um país"
    else:
        if category == "cbo":
            article = "an occupation"
        elif category == "isic":
            article = "an industry"
        elif category == "hs":
            article = "a product"
        elif category == "bra":
            article = "a location"
        elif category == "wld":
            article = "a country"

    if category:
        page = "general/selector.html"
    else:
        page = "profiles/index.html"
        
    return render_template(page,
        selector = selector,
        article = article)

@mod.route('/<category>/<id>/')
def profiles(category = None, id = None):
          
    t1 = time.time()
    category_type = "<"+category+">"
        
    t2 = time.time()
    g.timing.append("Initializing Profile: {0:.4f}s".format((t2-t1)))
    t1 = time.time()
    
    # Attr = globals()[category.title()]()
    
    # data_tables = []
    # rais_latest_year = db.session.query(Yio.year.distinct()) \
    #                     .order_by(Yio.year.desc()).all()[0][0]
    # secex_latest_year = db.session.query(Ypw.year.distinct()) \
    #                     .order_by(Ypw.year.desc()).all()[0][0]
    # app = App.query.filter_by(type="tree_map").first_or_404()
    # query_kwargs = {"raw":True}

    # if category == "isic" or category == "cbo":
    #     query_kwargs["year"] = rais_latest_year
    # elif category == "hs" or category == "wld":
    #     query_kwargs["year"] = secex_latest_year
        
    t2 = time.time()
    g.timing.append("Getting Table: {0:.4f}s".format((t2-t1)))
    t1 = time.time()
    
    Attr = globals()[category.title()]()
    item = Attr.query.get_or_404(id)
    
    # if category == "cbo":
    #     item = Cbo.query.get_or_404(id)
    # elif category == "hs":
    #     item = Hs.query.get_or_404(id)
    # elif category == "isic":
    #     item = Isic.query.get_or_404(id)
    # elif category == "wld":
    #     item = Wld.query.get_or_404(id)
        
    t2 = time.time()
    g.timing.append("Getting Item: {0:.4f}s".format((t2-t1)))
    t1 = time.time()
    
    plan = Plan.query.filter_by(category=category, category_type=category_type, 
                                    option=None).first()
        
    t2 = time.time()
    g.timing.append("Getting Plan: {0:.4f}s".format((t2-t1)))
    t1 = time.time()
        
    plan.set_attr(id, category)
    
    if category != "bra":
        plan.set_attr("all", "bra")
        
    t2 = time.time()
    g.timing.append("Setting Plan Variables: {0:.4f}s".format((t2-t1)))
    t1 = time.time()
            
    builds = [0]*len(plan.builds.all())
    for pb in plan.builds.all():
        
        build = pb.build.first()
        b = {}
        
        # this_query_kwargs = query_kwargs.copy()
        # data_table = build.data_table()
        # data_url = build.data_url().split("/")
        # output = build.output
        # bra = data_url[2]
        # filter1 = data_url[3]
        # filter2 = data_url[4]
        # data_set = data_url[0]
        # this_query_kwargs[category+"_id"] = id
        # if "show" in bra:
        #     this_query_kwargs["bra_id"] = bra
        # if "show" in filter1:
        #     if data_set == "rais":
        #         this_query_kwargs["isic_id"] = filter1
        #     elif data_set == "secex":
        #         this_query_kwargs["hs_id"] = filter1
        # if "show" in filter2:
        #     if data_set == "rais":
        #         this_query_kwargs["cbo_id"] = filter2
        #     elif data_set == "secex":
        #         this_query_kwargs["wld_id"] = filter2
        # if data_set == "rais":
        #     data = rais_get_query(data_table, request.args, **this_query_kwargs)
        #     table_headers = ["year", "_id", "wage", "num_emp", "num_est"]
        # else:
        #     data = secex_get_query(data_table, request.args, **this_query_kwargs)
        #     table_headers = ["year", "_id", "val_usd"]
        # table_headers[1] = output + table_headers[1]
        # 
        # table_data = [[getattr(d, h) for h in table_headers] for d in data]
        # b["data"] = { "table_headers":table_headers, "build":build, \
        # "table_data":table_data}
        
        b["url"] = "/apps/embed/{0}{1}".format(build.url(),pb.variables)
        b["title"] = build.title()
        b["type"] = build.app.type
        b["position"] = pb.position
        b["output"] = build.output
        b["color"] = build.app.color
        builds[pb.position-1] = b
        
    t2 = time.time()
    g.timing.append("Formatting Plan: {0}s".format((t2-t1)))
    
    return render_template("profiles/profile.html", 
                category=category,
                item=item, 
                builds=builds)

# @mod.route('/<category>/<id>/')
def profiles_old(category = None, id = None):
    category_type = "<"+category+">"
    
    plan = Plan.query.filter_by(category=category, category_type=category_type, option=None, option_type=None, option_id=None).first()

    page = "profiles/profile.html"

    plan.set_attr(id,category)
        
    if category == "bra":
        plan.set_attr(id,"bra")
    else:
        plan.set_attr("all","bra")
        
    builds = [0]*len(plan.builds.all())
    for pb in plan.builds.all():
        build = {}
        build["url"] = "/apps/embed/{0}{1}".format(pb.build.all()[0].url(),pb.variables)
        builds[pb.position-1] = build

    plan = {"title": plan.title(), "builds": builds}
        
    return render_template(page,
        plan = plan)