# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, g, url_for
from sqlalchemy import func

from visual import db
from visual.attrs import models as attrs
from visual.rais import models as rais
from visual.secex import models as secex

from visual.general.models import Plan

mod = Blueprint('profiles', __name__, url_prefix='/profiles')

@mod.before_request
def before_request():
    g.page_type = mod.name
    g.path = request.path

@mod.route('/')
@mod.route('/<category>/')
@mod.route('/<category>/<id>/')
def profiles(category = None, id = None):
    
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

    category_type = None
    if id and id != "select":
        category_type = "<"+category+">"
        
    plan = Plan.query.filter_by(category=category, category_type=category_type, option=None, option_type=None, option_id=None).first()
    # raise Exception(plan)
    if plan:
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
        
    elif category:
        page = "general/selector.html"
    else:
        page = "profiles/index.html"
        
    return render_template(page,
        selector = selector,
        article = article,
        plan = plan)