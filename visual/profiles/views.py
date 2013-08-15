# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, g, url_for
from sqlalchemy import func, distinct

from visual import db
from visual.attrs import models as attrs
from visual.rais import models as rais
from visual.secex import models as secex

from visual.general.models import Plan
from visual.attrs.models import Bra, Isic, Cbo, Hs, Wld
from visual.rais.views import get_query as rais_get_query
from visual.rais.models import Ybi, Ybo, Yio
from visual.secex.views import make_query as secex_get_query
from visual.secex.models import Ybp, Ybw, Ypw

from visual.apps.models import Build, App

mod = Blueprint('profiles', __name__, url_prefix='/profiles')

@mod.before_request
def before_request():
    g.page_type = mod.name
    g.path = request.path
    
    g.color = "#e0902d"

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
    
    data_tables = []
    rais_latest_year = db.session.query(Yio.year.distinct()) \
                        .order_by(Yio.year.desc()).all()[0][0]
    secex_latest_year = db.session.query(Ypw.year.distinct()) \
                        .order_by(Ypw.year.desc()).all()[0][0]
    app = App.query.filter_by(type="tree_map").first_or_404()
    query_kwargs = {"raw":True}

    if category == "bra":
        category_type = "<bra>"
        Attr = Bra
    elif category == "isic":
        category_type = "<isic>"
        Attr = Isic
        query_kwargs["year"] = rais_latest_year
    elif category == "cbo":
        category_type = "<cbo>"
        Attr = Cbo
        query_kwargs["year"] = rais_latest_year
    elif category == "hs":
        category_type = "<hs>"
        Attr = Hs
        query_kwargs["year"] = secex_latest_year
    elif category == "wld":
        category_type = "<wld>"
        Attr = Wld
        query_kwargs["year"] = secex_latest_year
    
    item = Attr.query.get_or_404(id)
    
    plan = Plan.query.filter_by(category=category, category_type=category_type, 
                                    option=None).first()
    if category == "cbo":
        plan.set_attr(id, "cbo")
    elif category == "hs":
        plan.set_attr(id, "hs")
    elif category == "isic":
        plan.set_attr(id, "isic")
    elif category == "wld":
        plan.set_attr(id, "wld")
    
    if category == "bra":
        plan.set_attr(id, "bra")
    else:
        plan.set_attr("all", "bra")  
          
    builds = [0]*len(plan.builds.all())
    for i, pb in enumerate(plan.builds.all()):
        this_query_kwargs = query_kwargs.copy()
        build = pb.build.first()
        data_table = build.data_table()
        data_url = build.data_url().split("/")
        output = build.output
        bra = data_url[2]
        filter1 = data_url[3]
        filter2 = data_url[4]
        data_set = data_url[0]
        this_query_kwargs[category+"_id"] = id
        if "show" in bra:
            this_query_kwargs["bra_id"] = bra
        if "show" in filter1:
            if data_set == "rais":
                this_query_kwargs["isic_id"] = filter1
            elif data_set == "secex":
                this_query_kwargs["hs_id"] = filter1
        if "show" in filter2:
            if data_set == "rais":
                this_query_kwargs["cbo_id"] = filter2
            elif data_set == "secex":
                this_query_kwargs["wld_id"] = filter2
        if data_set == "rais":
            data = rais_get_query(data_table, request.args, **this_query_kwargs)
            table_headers = ["year", "_id", "wage", "num_emp", "num_est"]
        else:
            data = secex_get_query(data_table, request.args, **this_query_kwargs)
            table_headers = ["year", "_id", "val_usd"]
        table_headers[1] = output + table_headers[1]
        
        table_data = [[getattr(d, h) for h in table_headers] for d in data]
        
        b = {}
        b["url"] = "/apps/embed/{0}{1}".format(build.url(),pb.variables)
        b["title"] = build.title()
        b["type"] = build.app.type
        b["position"] = pb.position
        b["output"] = output
        b["color"] = build.app.color
        b["data"] = { "table_headers":table_headers, "build":build, \
                                    "table_data":table_data}
        builds[pb.position-1] = b
        
    return render_template("profiles/profile.html", 
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