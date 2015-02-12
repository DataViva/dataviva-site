# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, g, url_for
from flask.ext.babel import gettext
from sqlalchemy import func, distinct
from werkzeug import urls

from dataviva import db, view_cache
from dataviva.attrs import models as attrs
from dataviva.rais import models as rais
from dataviva.secex import models as secex

from dataviva.general.models import Plan
from dataviva.attrs.models import Bra, Cnae, Cbo, Hs, Wld, University, Course_hedu, Course_sc
from dataviva.rais.models import Ybi, Ybo, Yio

from dataviva.utils.decorators import cache_api
from dataviva.utils.gzip_data import gzipped

from dataviva.profiles import models as profileModels

import time

mod = Blueprint('profiles', __name__, url_prefix='/profiles')

@mod.before_request
def before_request():
    g.page_type = mod.name
    g.path = request.path

    g.color = "#e0902d"

@mod.route('/')
@mod.route('/<category>/select/')
#@view_cache.cached(timeout=604800, key_prefix=make_cache_key)
def index(category = None, id = None):
    selector = category

    article = None

    if category == "cbo":
        article = gettext(u"an occupation")
    elif category == "cnae":
        article = gettext(u"an industry")
    elif category == "hs":
        article = gettext(u"a product")
    elif category == "bra":
        article = gettext(u"a location")
    elif category == "wld":
        article = gettext(u"a country")
    elif category == "university":
        article = gettext(u"a university")
    elif category == "course_hedu":
        article = gettext(u"a course")
    elif category == "course_sc":
        article = gettext(u"a course")

    if category:
        page = "general/selector.html"
    else:
        page = "profiles/index.html"

    return render_template(page,
        selector = selector,
        article = article)

@mod.route('/<category>/<id>/')
@cache_api("profiles", timeout=604800)
@gzipped
def profiles(category = None, id = None):

    if category == "bra" and id == "all":
        item = Wld.query.get("sabra")
    else:
        item = globals()[category.capitalize()].query.get_or_404(id)

    profile = getattr(profileModels, category.capitalize())(category, item)
    builds = profile.builds()

    start = request.args.get("app", 1)

    return render_template("profiles/profile.html",
                category=category, item=item,
                starting_app = start, builds=builds)
