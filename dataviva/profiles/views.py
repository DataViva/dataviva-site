# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, g, url_for
from flask.ext.babel import gettext
from sqlalchemy import func, distinct
from werkzeug import urls

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
    g.page_type = mod.name
    g.path = request.path
    
    g.color = "#e0902d"

@mod.route('/')
@mod.route('/<category>/select/')
def index(category = None, id = None):
    
    selector = category
    
    article = None
    
    if category == "cbo":
        article = gettext(u"an occupation")
    elif category == "isic":
        article = gettext(u"an industry")
    elif category == "hs":
        article = gettext(u"a product")
    elif category == "bra":
        article = gettext(u"a location")
    elif category == "wld":
        article = gettext(u"a country")

    if category:
        page = "general/selector.html"
    else:
        page = "profiles/index.html"
        
    return render_template(page,
        selector = selector,
        article = article)

@mod.route('/<category>/<id>/')
def profiles(category = None, id = None):
    
    category_type = "<{0}.{1}>".format(category,len(id))
    
    Attr = globals()[category.title()]()
    item = Attr.query.get_or_404(id)
    
    plan = Plan.query.filter_by(category=category, category_type=category_type, 
                                    option=None).first()
        
    plan.set_attr(id, category)
    
    if category != "bra":
        plan.set_attr("all", "bra")
    
    builds = [0]*len(plan.builds.all())
    for pb in plan.builds.all():
        
        build = pb.build.first()
        b = {}
        
        b["url"] = "/apps/embed/{0}{1}".format(build.url(),pb.variables)
        params = dict(urls.url_decode(pb.variables[1:]))
        b["title"] = build.title(**params)
        b["type"] = build.app.type
        b["position"] = pb.position
        b["output"] = build.output
        b["color"] = build.app.color
        builds[pb.position-1] = b
    
    return render_template("profiles/profile.html", 
                category=category,
                item=item, 
                builds=builds)