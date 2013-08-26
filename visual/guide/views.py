# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, g, url_for
from sqlalchemy import func
from datetime import datetime

from visual import db
from visual.attrs import models as attrs
from visual.rais import models as rais
from visual.secex import models as secex

from visual.general.models import Plan

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
def guide(category = None, category_id = None, option = None, subject = None, option_id = None, extra_id = None):
    
    item = None
    article = None
    selector = category
    plan = None
    
    category_type = category_id
    
    if category_id == "all" and category == "cbo":
        category_type = "all"
    elif category:
        category_type = "<"+category+">"
        
    if (category == "cbo" or option == "potential") and option_id and option_id != "select":
        option_type = "<bra>"
    else:
        option_type = option_id
        

    extra_type = extra_id
        
    if category == "bra":
        if option == "isic" and option_id:
            option_type = "<isic>"
        if option_id == "hs" and extra_id and extra_id != "select":
            extra_type = "<hs>"
        elif option_id == "isic" and extra_id and extra_id != "select":
            extra_type = "<isic>"
        
    # raise Exception(category,category_type,option,option_type,extra_type)
    if option:
        plan = Plan.query.filter_by(category=category, category_type=category_type, option=option, option_type=option_type, option_id=extra_type).first()
    # raise Exception(plan)
    if plan:
        
        g.page_type = "plan"
        page = "guide/guide.html"
        

        plan.set_attr(category_id,category)

        if category == "bra":
            if option_id == "hs" and extra_id:
                plan.set_attr(extra_id,"hs")
            elif option_id == "isic" and extra_id:
                plan.set_attr(extra_id,"isic")
            bra_id = category_id    
        elif option_type == "<bra>":
            plan.set_attr(option_id,"bra")
        else:
            plan.set_attr("all","bra")
            
        builds = [0]*len(plan.builds.all())
        for pb in plan.builds.all():
            build = {}
            build["url"] = "/apps/embed/{0}{1}".format(pb.build.all()[0].url(),pb.variables)
            build["title"] = pb.build.all()[0].title()
            build["type"] = pb.build.all()[0].app.type
            build["position"] = pb.position
            builds[pb.position-1] = build
            
        plan = {"title": plan.title(), "builds": builds}
            
    elif extra_id == "select":
        page = "general/selector.html"
        selector = option_id
    elif option_id == "select":
        page = "general/selector.html"
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
        if category_id == "select":
            page = "general/selector.html"
        else:
            if category_id != "all":
                if category == "isic":
                    item = attrs.Isic.query.get_or_404(category_id).name()
                elif category == "hs":
                    item = attrs.Hs.query.get_or_404(category_id).name()
                elif category == "cbo":
                    item = attrs.Cbo.query.get_or_404(category_id).name()
                elif category == "bra":
                    item = attrs.Bra.query.get_or_404(category_id).name()
            elif category == "bra":
                item = attrs.Wld.query.get_or_404("sabra").name()
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
        plan = plan)
