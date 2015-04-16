# -*- coding: utf-8 -*-
from flask import Blueprint, redirect, request, render_template, g, url_for
from flask.ext.babel import gettext
from sqlalchemy import func, not_
from werkzeug import urls
import random, time

from dataviva import db, view_cache
from dataviva.attrs import models as attrs
from dataviva.rais import models as rais
from dataviva.secex import models as secex

from dataviva.attrs.models import Bra, Cnae, Cbo, Hs, Wld, University, Course_hedu, Course_sc
from dataviva.attrs.models import Ybb, Yii, Yoo, Ypp, Yww, Yuu
from dataviva.secex.models import Ymb, Ymp, Ymw
from dataviva.rais.models import Ybi, Ybo, Yio, Yi, Yo
from dataviva.hedu.models import Yu, Yc_hedu
from dataviva.sc.models import Yc_sc

from dataviva.utils.cached_query import cached_query, make_cache_key, api_cache_key
from dataviva.utils.gzip_data import gzipped
from dataviva.profiles import models as profileModels

from dataviva import __year_range__
from dataviva.stats.util import parse_year
from dataviva.stats.profile_helper import compute_stats

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
        "summary": gettext("Showing the locations and schools in which these basic courses are taught."),
        "top": top,
        "title": gettext(u"Basic Courses"),
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
        article = gettext(u"a major")
    elif category == "course_sc":
        article = gettext(u"a course")

    if category:
        page = "general/selector.html"
    else:
        page = "profiles/index.html"

    return render_template(page,
        selector = selector,
        article = article)

@mod.route("/<category>/")
def randomProfile(category = None):

    if category == "bra":
        ids = db.session.query(Ymb.bra_id).filter(Ymb.bra_id_len == "9") \
                .filter(Ymb.year == __year_range__["secex"][1].split("-")[0]) \
                .filter(not_(Ymb.bra_id.contains("0xx"))) \
                .filter(Ymb.month == 0).distinct()
    elif category == "hs":
        ids = db.session.query(Ymp.hs_id).filter(Ymp.hs_id_len == "6") \
                .filter(Ymp.year == __year_range__["secex"][1].split("-")[0]) \
                .filter(Ymp.month == 0).distinct()
    elif category == "wld":
        ids = db.session.query(Ymw.wld_id).filter(Ymw.wld_id_len == "5") \
                .filter(Ymw.year == __year_range__["secex"][1].split("-")[0]) \
                .filter(Ymw.month == 0).distinct()
    elif category == "cnae":
        ids = db.session.query(Yi.cnae_id).filter(Yi.cnae_id_len == "6") \
                .filter(Yi.year == __year_range__["rais"][1]).distinct()
    elif category == "cbo":
        ids = db.session.query(Yo.cbo_id).filter(Yo.cbo_id_len == "4") \
                .filter(Yo.year == __year_range__["rais"][1]).distinct()
    elif category == "university":
        ids = db.session.query(Yu.university_id) \
                .filter(Yu.year == __year_range__["hedu"][1]).distinct()
    elif category == "course_hedu":
        ids = db.session.query(Yc_hedu.course_hedu_id).filter(Yc_hedu.course_hedu_id_len == "6") \
                .filter(Yc_hedu.course_hedu_id != "000000") \
                .filter(Yc_hedu.year == __year_range__["hedu"][1]).distinct()
    elif category == "course_sc":
        ids = db.session.query(Yc_sc.course_sc_id).filter(Yc_sc.course_sc_id_len == "5") \
                .filter(Yc_sc.course_sc_id != "000000") \
                .filter(not_(Yc_sc.course_sc_id.contains("xx"))) \
                .filter(Yc_sc.year == __year_range__["sc"][1]).distinct()
    rand = random.randrange(0, ids.count())
    id = ids[rand][0]
    return redirect(url_for("profiles.profiles", category=category, id=id))

@mod.route("/<category>/<id>/")
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
    stats = compute_stats(item)

    related = []
    def get_related(table, attr, title):
        if attr == "bra":
            data_attr = category
        else:
            data_attr = attr
        if data_attr == "hs" or data_attr == "wld":
            dataset = "secex"
        elif data_attr == "cnae" or data_attr == "cbo":
            dataset = "rais"
        elif data_attr == "university" or data_attr == "course_hedu":
            dataset = "hedu"
        elif data_attr == "course_sc":
            dataset = "sc"
        else:
            return
        q = table.query.filter(getattr(table, "{}_id".format(category)) == id) \
                 .filter(getattr(table, "year") == parse_year(__year_range__[dataset][1])) \
                 .order_by(getattr(table, "prox_{}".format(attr)).desc()).limit(5).all()
        if len(q) > 0:
            m = globals()[category.capitalize()]
            q = [m.query.get(getattr(a, "{}_id_target".format(category))) for a in q]
            related.append({"title": title, "pages": q})

    if category == "bra":
        get_related(Ybb, "hs", gettext("Locations with Similar Product Exports"))
        get_related(Ybb, "wld", gettext("Locations with Similar Trade Partners"))
        get_related(Ybb, "cnae", gettext("Locations with Similar Industries"))
        get_related(Ybb, "cbo", gettext("Locations with Similar Occupations"))
    if category == "cnae":
        get_related(Yii, "bra", gettext("Similar Industries by Co-location"))
    if category == "cbo":
        get_related(Yoo, "bra", gettext("Similar Occupations by Co-location"))
    if category == "hs":
        get_related(Ypp, "bra", gettext("Similar Products by Co-location"))
    if category == "wld":
        get_related(Yww, "bra", gettext("Destinations with Similar Brazilian Origins"))
    if category == "university":
        get_related(Yuu, "course_hedu", gettext("Universities with Similar Course Offerings"))

    return render_template("profiles/profile.html",
                category=category, item=item, stats=stats,
                starting_app = start, builds=builds, related=related)
