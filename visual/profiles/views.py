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
    # if category == "bra":
    #     isic = get_query(Ybi, request.args, bra_id=id, isic_id="show.5", raw=True)
    #     cbo = get_query(Ybo, request.args, bra_id=id, cbo_id="show.4", raw=True)
    
    data_tables = []
    rais_latest_year = db.session.query(Yio.year.distinct()) \
                        .order_by(Yio.year.desc()).all()[0][0]
    secex_latest_year = db.session.query(Ypw.year.distinct()) \
                        .order_by(Ypw.year.desc()).all()[0][0]
    app = App.query.filter_by(type="tree_map").first_or_404()
    if category == "isic" or category == "cbo":
        '''RAIS'''

        if category == "isic":
            item = Isic.query.get_or_404(id)
            
            '''locations that have this industry'''
            table = rais_get_query(Ybi, request.args, isic_id=id, \
                        bra_id="show.8", raw=True, year=rais_latest_year)
            table_headers = ["year", "bra_id", "wage", "num_emp", "num_est"]
            table_data = [[getattr(t, h) for h in table_headers] for t in table]
            build = Build.query.filter_by(app=app, dataset="rais", 
                        filter1="<isic>", filter2="all", output="bra") \
                        .first_or_404()
            build.set_filter1(id)
            build.set_filter2("all")
            build.set_bra("all")
            data_tables.append({ "table_headers":table_headers, "build":build, \
                                    "table_data":table_data})
            
            '''occupations that employ this industry'''
            table = rais_get_query(Yio, request.args, isic_id=id, \
                        cbo_id="show.4", raw=True, year=rais_latest_year)
            table_headers = ["year", "cbo_id", "wage", "num_emp", "num_est"]
            table_data = [[getattr(t, h) for h in table_headers] for t in table]
            build = Build.query.filter_by(app=app, dataset="rais", 
                        filter1="<isic>", filter2="all", output="cbo") \
                        .first_or_404()
            build.set_filter1(id)
            build.set_filter2("show")
            build.set_bra("all")
            data_tables.append({ "table_headers":table_headers, "build":build, \
                                    "table_data":table_data})

        if category == "cbo":
            item = Cbo.query.get_or_404(id)
            
            '''locations that employ this occupation'''
            table = rais_get_query(Ybo, request.args, cbo_id=id, \
                        bra_id="show.8", raw=True, year=rais_latest_year)
            table_headers = ["year", "bra_id", "wage", "num_emp", "num_est"]
            table_data = [[getattr(t, h) for h in table_headers] for t in table]
            build = Build.query.filter_by(app=app, dataset="rais", 
                        filter1="all", filter2="<cbo>", output="bra") \
                        .first_or_404()
            build.set_filter1("all")
            build.set_filter2(id)
            build.set_bra("all")
            data_tables.append({ "table_headers":table_headers, "build":build, \
                                    "table_data":table_data})

            '''industries that employ this occupation'''            
            table = rais_get_query(Yio, request.args, cbo_id=id, \
                        isic_id="show.5", raw=True, year=rais_latest_year)
            table_headers = ["year", "isic_id", "wage", "num_emp", "num_est"]
            table_data = [[getattr(t, h) for h in table_headers] for t in table]
            build = Build.query.filter_by(app=app, dataset="rais", 
                        filter1="all", filter2="<cbo>", output="isic") \
                        .first_or_404()
            build.set_filter1("show")
            build.set_filter2(id)
            build.set_bra("all")
            data_tables.append({ "table_headers":table_headers, "build":build, \
                                    "table_data":table_data})
            
            
    elif category == "hs" or category == "wld":
        '''SECEX'''

        if category == "hs":
            item = Hs.query.get_or_404(id)
            
            '''locations that export this product'''
            table = secex_get_query(Ybp, request.args, hs_id=id, \
                        bra_id="show.8", raw=True, year=secex_latest_year)
            table_headers = ["year", "bra_id", "val_usd"]
            table_data = [[getattr(t, h) for h in table_headers] for t in table]
            build = Build.query.filter_by(app=app, dataset="secex", 
                        filter1="<hs>", filter2="all", output="bra") \
                        .first_or_404()
            build.set_filter1(id)
            build.set_filter2("all")
            build.set_bra("all")
            data_tables.append({ "table_headers":table_headers, "build":build, \
                                    "table_data":table_data})
            
            '''trade partners that import this product'''
            table = secex_get_query(Ypw, request.args, hs_id=id, \
                        wld_id="show.5", raw=True, year=secex_latest_year)
            table_headers = ["year", "wld_id", "val_usd"]
            table_data = [[getattr(t, h) for h in table_headers] for t in table]
            build = Build.query.filter_by(app=app, dataset="secex", 
                        filter1="<hs>", filter2="all", output="wld") \
                        .first_or_404()
            build.set_filter1(id)
            build.set_filter2("show")
            build.set_bra("all")
            data_tables.append({ "table_headers":table_headers, "build":build, \
                                    "table_data":table_data})
            
        if category == "wld":
            item = Wld.query.get_or_404(id)
            
            '''locations that export this product'''
            table = secex_get_query(Ybw, request.args, wld_id=id, \
                        bra_id="show.8", raw=True, year=secex_latest_year)
            table_headers = ["year", "bra_id", "val_usd"]
            table_data = [[getattr(t, h) for h in table_headers] for t in table]
            build = Build.query.filter_by(app=app, dataset="secex", 
                        filter1="all", filter2="<wld>", output="bra") \
                        .first_or_404()
            build.set_filter1("all")
            build.set_filter2(id)
            build.set_bra("all")
            data_tables.append({ "table_headers":table_headers, "build":build, \
                                    "table_data":table_data})
            
            '''trade partners that import this product'''
            table = secex_get_query(Ypw, request.args, wld_id=id, \
                        hs_id="show.6", raw=True, year=secex_latest_year)
            table_headers = ["year", "hs_id", "val_usd"]
            table_data = [[getattr(t, h) for h in table_headers] for t in table]
            build = Build.query.filter_by(app=app, dataset="secex", 
                        filter1="all", filter2="<wld>", output="hs") \
                        .first_or_404()
            build.set_filter1("show")
            build.set_filter2(id)
            build.set_bra("all")
            data_tables.append({ "table_headers":table_headers, "build":build, \
                                    "table_data":table_data})
            
    else:
        item = Bra.query.get_or_404(id)
        
        '''industries found in this location'''
        table = rais_get_query(Ybi, request.args, bra_id=id, \
                    isic_id="show.5", raw=True, year=rais_latest_year)
        table_headers = ["year", "isic_id", "wage", "num_emp", "num_est"]
        table_data = [[getattr(t, h) for h in table_headers] for t in table]
        build = Build.query.filter_by(app=app, dataset="rais", 
                    filter1="all", filter2="all", output="isic") \
                    .first_or_404()
        build.set_filter1("show")
        build.set_filter2("all")
        build.set_bra(id)
        data_tables.append({ "table_headers":table_headers, "build":build, \
                                "table_data":table_data})
        
        '''occupations found in this location'''
        table = rais_get_query(Ybo, request.args, bra_id=id, \
                    cbo_id="show.4", raw=True, year=rais_latest_year)
        table_headers = ["year", "cbo_id", "wage", "num_emp", "num_est"]
        table_data = [[getattr(t, h) for h in table_headers] for t in table]
        build = Build.query.filter_by(app=app, dataset="rais", 
                    filter1="all", filter2="all", output="cbo") \
                    .first_or_404()
        build.set_filter1("all")
        build.set_filter2("show")
        build.set_bra(id)
        data_tables.append({ "table_headers":table_headers, "build":build, \
                                "table_data":table_data})
        
        '''products exported by this location'''
        table = secex_get_query(Ybp, request.args, bra_id=id, \
                    hs_id="show.6", raw=True, year=secex_latest_year)
        table_headers = ["year", "hs_id", "val_usd"]
        table_data = [[getattr(t, h) for h in table_headers] for t in table]
        build = Build.query.filter_by(app=app, dataset="secex", 
                    filter1="all", filter2="all", output="hs") \
                    .first_or_404()
        build.set_filter1("show")
        build.set_filter2("all")
        build.set_bra(id)
        data_tables.append({ "table_headers":table_headers, "build":build, \
                                "table_data":table_data})

        '''world trade partners of this location'''
        table = secex_get_query(Ybw, request.args, bra_id=id, \
                    wld_id="show.5", raw=True, year=secex_latest_year)
        table_headers = ["year", "wld_id", "val_usd"]
        table_data = [[getattr(t, h) for h in table_headers] for t in table]
        build = Build.query.filter_by(app=app, dataset="secex", 
                    filter1="all", filter2="all", output="wld") \
                    .first_or_404()
        build.set_filter1("all")
        build.set_filter2("show")
        build.set_bra(id)
        data_tables.append({ "table_headers":table_headers, "build":build, \
                                "table_data":table_data})

        
        
    
    return render_template("profiles/profile.html", 
                item=item, 
                data_tables=data_tables)

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