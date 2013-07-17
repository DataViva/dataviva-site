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
    
    g.sabrina = {}
    g.sabrina["outfit"] = "lab"
    g.sabrina["face"] = "smirk"
    g.sabrina["hat"] = None
    
    g.path = request.path

@mod.route('/')
@mod.route('/<category>/')
@mod.route('/<category>/<id>/')
def profiles(category = None, id = None):
    
    selector = category
    category_type = None
        
    bra_id = "all"
    filter1 = None
    filter2 = None
    
    article = None
        
    if category == "career":
        article = "an occupation"
        if id and id != "select":
            category_type = "<cbo>"
    elif category == "establishment":
        article = "an industry"
        if id and id != "select":
            category_type = "<isic>"
    elif category == "export":
        article = "a product"
        if id and id != "select":
            category_type = "<hs>"
    elif category == "location":
        article = "a location"
        if id and id != "select":
            category_type = "<bra>"
    elif category == "partner":
        article = "a trade partner"
        if id and id != "select":
            category_type = "<wld>"
        
    plan = Plan.query.filter_by(category=category, category_type=category_type, option=None, option_type=None, option_id=None).first()
    # raise Exception(plan)
    if plan:
        page = "general/guide.html"
        
        if category == "career":
            plan.set_attr(id,"cbo")
        elif category == "establishment":
            plan.set_attr(id,"isic")
        elif category == "export":
            plan.set_attr(id,"hs")
        elif category == "partner":
            plan.set_attr(id,"wld")
            
        if category == "location":
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
        
    if category == "career":
        g.sabrina["outfit"] = "preppy"
    elif category == "export" or category == "establishment":
        g.sabrina["outfit"] = "worker"
        g.sabrina["hat"] = "hardhat"
    elif category == "location" or category == "partner":
        g.sabrina["outfit"] = "travel"
        
    return render_template(page,
        selector = selector,
        article = article,
        plan = plan)