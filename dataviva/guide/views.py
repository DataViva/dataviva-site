# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, g, url_for
from sqlalchemy import func
from datetime import datetime
from werkzeug import urls

from dataviva import db
from dataviva.attrs.models import Bra, Isic, Cbo, Hs, Wld
from dataviva.rais import models as rais
from dataviva.secex import models as secex

from dataviva.general.models import Plan

mod = Blueprint('guide', __name__, url_prefix='/guide')

@mod.before_request
def before_request():
    g.page_type = mod.name
    g.path = request.path

@mod.route('/')
@mod.route('/<category>/')
@mod.route('/<category>/<category_id>/')
@mod.route('/<category>/<category_id>/<option>/')
@mod.route('/<category>/<category_id>/<option>/<option_id>/')
@mod.route('/<category>/<category_id>/<option>/<option_id>/<extra_id>/')
def guide(category = None, category_id = None, option = None, option_id = None, extra_id = None):
    
    item = None
    article = None
    selector = category
    plan = None
    group = None
    
    depths = {
        "bra": [2,3,4,7,8],
        "isic": [1,5],
        "cbo": [1,4],
        "hs": [2,6],
        "wld": [2,5]
    }
        
    if option:
        
        if category_id == "all":
            category_type = category_id
        else:
            category_type = "<{0}.{1}>".format(category,len(category_id))
            
        if option_id == "isic" or option_id == "hs":
            option_type = option_id
        elif option_id and option_id != "all":
            option_type = "<bra.{0}>".format(len(option_id))
        else:
            option_type = option_id
            
        if extra_id and extra_id != "select" and extra_id != "all":
            extra_type = "<{0}.{1}>".format(option_id,len(extra_id))
        elif extra_id != "select":
            extra_type = extra_id
        else:
            extra_type = None
                    
        plan = Plan.query.filter_by(category=category, category_type=category_type, option=option, option_type=option_type, option_id=extra_type).first()
    
    # raise Exception(plan)
    
    if plan:
        
        g.page_type = "plan"
        page = "guide/guide.html"
        
        plan.set_attr(category_id,category)

        if category == "bra" and extra_id:
            plan.set_attr(extra_id,option_id)
            
        if category != "bra":
            if option_type and "<bra" in option_type:
                plan.set_attr(option_id,"bra")
            else:
                plan.set_attr("all","bra")
            
        builds = [0]*len(plan.builds.all())
        for pb in plan.builds.all():
            
            build = {}
            build["url"] = "/apps/embed/{0}{1}".format(pb.build.all()[0].url(),pb.variables)
            params = dict(urls.url_decode(pb.variables[1:]))
            build["title"] = pb.build.all()[0].title(**params)
            build["type"] = pb.build.all()[0].app.type
            build["position"] = pb.position
            builds[pb.position-1] = build
            
        plan = {"title": plan.title(), "builds": builds}
            
    elif extra_id == "select" or option_id == "select" or category_id == "select":
        page = "general/selector.html"
        if extra_id:
            selector = option_id
        elif option_id:
            selector = "bra"
            
    elif option:
        if category == "cbo":
            selector = "bra"
            page = "guide/choice.html"
        elif category == "bra":
            page = "guide/industry.html"
        elif category == "hs" or category == "isic" and option == "potential":
            selector = "bra"
            page = "guide/choice.html"
            
    elif category_id:

        if category == "bra":
            if len(category_id) == depths[category][0]:
                group = "parent"
            elif len(category_id) == depths[category][1]:
                group = "all"
            else:
                group = "child"
        else:
            if len(category_id) == depths[category][0]:
                group = "parent"
            elif len(category_id) == depths[category][1]:
                group = "child"
                
        if category_id != "all":
            table = category.title()
            item = globals()[table].query.get_or_404(category_id).name()
        elif category == "bra":
            item = Wld.query.get_or_404("sabra").name()
        page = "guide/{0}.html".format(category)
        
    elif category == "industry":
        page = "guide/industry.html"
        
    elif category:
        page = "guide/choice.html"
        
    else:
        page = "guide/index.html"
        
    if g.locale == "pt":
        if selector == "cbo":
            article = "uma profissão"
        elif selector == "isic":
            article = "uma indústria"
        elif selector == "hs":
            article = "um produto"
        elif selector == "bra":
            article = "um local"
    else:
        if selector == "cbo":
            article = "an occupation"
        elif selector == "isic":
            article = "an industry"
        elif selector == "hs":
            article = "a product"
        elif selector == "bra":
            article = "a location"
            
    return render_template(page,
        category = category,
        category_id = category_id,
        option = option,
        item = item,
        article = article,
        selector = selector,
        plan = plan,
        group = group)
