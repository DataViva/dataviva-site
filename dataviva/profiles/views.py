# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, g, url_for
from flask.ext.babel import gettext
from sqlalchemy import func, distinct
from werkzeug import urls
import time

from dataviva import db, view_cache
from dataviva.attrs import models as attrs
from dataviva.rais import models as rais
from dataviva.secex import models as secex

from dataviva.general.models import Plan
from dataviva.attrs.models import Bra, Cnae, Cbo, Hs, Wld, University, Course_hedu, Course_sc
from dataviva.secex.models import Ymb, Ymp, Ymw
from dataviva.rais.models import Ybi, Ybo, Yio, Yi, Yo
from dataviva.hedu.models import Yu, Yc_hedu
from dataviva.sc.models import Yc_sc

from dataviva.utils.cached_query import cached_query, make_cache_key, api_cache_key
from dataviva.utils.gzip_data import gzipped
from dataviva.profiles import models as profileModels

from dataviva import __year_range__
from dataviva.stats.util import parse_year


mod = Blueprint('profiles', __name__, url_prefix='/profiles')

@mod.before_request
def before_request():
    g.page_type = mod.name
    g.path = request.path

    g.color = "#e0902d"

@mod.route('/')
@view_cache.cached(timeout=604800, key_prefix=make_cache_key)
def index():

    profile_types = []

    # Bra
    most_recent_year = parse_year(__year_range__["secex"][-1])
    top = Ymb.query.filter_by(year=most_recent_year, month=0, bra_id_len=9).order_by(Ymb.export_val.desc()).limit(5).all()
    top = [t.bra for t in top]
    profile_types.append({
        "summary": gettext("Showing exports, employment and education data, statistics and visualizations about the chosen Brazilian location."),
        "top": top,
        "title": gettext(u"Brazilian Locations"),
        "type": "bra"
    })

    # Occupations
    most_recent_year = parse_year(__year_range__["rais"][-1])
    top = Yo.query.filter_by(year=most_recent_year, cbo_id_len=4).order_by(Yo.num_emp.desc()).limit(5).all()
    top = [t.cbo for t in top]
    profile_types.append({
        "summary": gettext("Showing industries and locations that employ the selected occupation."),
        "top": top,
        "title": gettext(u"Occupations"),
        "type": "cbo"
    })

    # Industries
    top = Yi.query.filter_by(year=most_recent_year, cnae_id_len=6).order_by(Yi.num_emp.desc()).limit(5).all()
    top = [t.cnae for t in top]
    profile_types.append({
        "summary": gettext("Showing the occupations and locations with employees in the selected industry."),
        "top": top,
        "title": gettext(u"Industries"),
        "type": "cnae"
    })

    # Prods
    most_recent_year = parse_year(__year_range__["secex"][-1])
    top = Ymp.query.filter_by(year=most_recent_year, month=0, hs_id_len=6).order_by(Ymp.export_val.desc()).limit(5).all()
    top = [t.hs for t in top]
    profile_types.append({
        "summary": gettext("Showing locations in Brazil that export and import the selected product and their destinations and origins."),
        "top": top,
        "title": gettext(u"Products"),
        "type": "hs"
    })

    # Countries
    top = Ymw.query.filter_by(year=most_recent_year, month=0, wld_id_len=5).order_by(Ymw.export_val.desc()).limit(5).all()
    top = [t.wld for t in top]
    profile_types.append({
        "summary": gettext("Showing locations in brazil that trade with the selected country and the products they export and import from them."),
        "top": top,
        "title": gettext(u"Trade Partners"),
        "type": "wld"
    })

    # Universities
    most_recent_year = parse_year(__year_range__["hedu"][-1])
    top = Yu.query.filter_by(year=most_recent_year).order_by(Yu.enrolled.desc()).limit(5).all()
    top = [t.university for t in top]
    profile_types.append({
        "summary": gettext("Showing the majors found in the selected univserity."),
        "top": top,
        "title": gettext(u"Universities"),
        "type": "university"
    })

    # Majors
    top = Yc_hedu.query.filter_by(year=most_recent_year).order_by(Yc_hedu.enrolled.desc()).limit(5).all()
    top = [t.course_hedu for t in top]
    profile_types.append({
        "summary": gettext("Showing the university and locations in Brazil where the selected major is found."),
        "top": top,
        "title": gettext(u"Majors"),
        "type": "course_hedu"
    })

    # Vocations
    most_recent_year = parse_year(__year_range__["sc"][-1])
    top = Yc_sc.query.filter_by(year=most_recent_year, course_sc_id_len=5).order_by(Yc_sc.enrolled.desc()).filter(~Yc_sc.course_sc_id.startswith('xx')).limit(5).all()
    top = [t.course_sc for t in top]
    profile_types.append({
        "summary": gettext("Showing the locations and schools in which these vocations are taught."),
        "top": top,
        "title": gettext(u"Vocational Courses"),
        "type": "course_sc"
    })

    return render_template("profiles/index.html", profile_types=profile_types)

@mod.route('/<category>/select/')
@view_cache.cached(timeout=604800, key_prefix=make_cache_key)
def index_selector(category = None, id = None):
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
@view_cache.cached(timeout=604800, key_prefix=api_cache_key("profiles"))
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
