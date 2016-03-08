# -*- coding: utf-8 -*-
from StringIO import StringIO
from datetime import datetime
from collections import defaultdict
from sqlalchemy import func
from random import randint
from flask import Blueprint, request, render_template, g, Response, make_response, send_file, jsonify, url_for, redirect, jsonify
from flask.ext.babel import gettext

from dataviva import db, datavivadir, __year_range__, view_cache
from dataviva.general.views import get_locale
from dataviva.data.forms import DownloadForm
from dataviva.account.models import User, Starred
from dataviva.attrs.models import Bra, Cnae, Hs, Cbo, Wld, University, Course_hedu, Course_sc, Search
from dataviva.apps.models import Build, UI, App, Crosswalk_oc, Crosswalk_pi
from dataviva.general.models import Short

from dataviva.rais.views import rais_api
from dataviva.translations.translate import translate
from dataviva.utils.gzip_data import gzip_data
from dataviva.utils.cached_query import cached_query, api_cache_key
from dataviva.utils.title_format import title_format

import json, urllib2, urllib
from config import FACEBOOK_OAUTH_ID, basedir,GZIP_DATA
import os, urlparse, random, zipfile, sys, gzip
from dataviva.utils.cached_query import api_cache_key

mod = Blueprint('apps', __name__, url_prefix='/<lang_code>/apps')

@mod.before_request
def before_request():
    g.page_type = mod.name

    g.color = "#af1f24"

    g.sabrina = {
        "outfit": "lab",
        "face": "smirk",
        "hat": "glasses"
    }

@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())

@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')

def filler(dataset, filter1, filter2):

    '''Since the "builds" are held in the database with placeholders for
    attributes i.e. <cbo>, <hs>, <cnae> we need to convert the IDs given
    in the URL to these placeholders. i.e.
         - a0111    = <cnae>
         - 010101   = <hs>
         - all      = all
    '''

    filler1 = filter1
    if filler1 != "all":
        if dataset == "rais":
            filler1 = "cnae"
        elif dataset == "secex":
            filler1 = "hs"
        elif dataset == "hedu":
            filler1 = "university"

    filler2 = filter2
    if filler2 != "all":
        if dataset == "rais":
            filler2 = "cbo"
        elif dataset == "secex":
            filler2 = "wld"
        elif dataset == "hedu":
            filler2 = "course_hedu"
        elif dataset == "sc":
            filler2 = "course_sc"

    return filler1, filler2

@mod.route('/')
@view_cache.cached(key_prefix=api_cache_key("apps:guide"))
def guide():
    apps = []
    default_bra = Bra.query.get("4mg")
    compare_bra = Bra.query.get("4sp")
    default_cnae = Cnae.query.get("i56112")
    default_cbo = Cbo.query.get("2235")
    default_hs = Hs.query.get("052601")
    build_list = Build.query.all()

    # Bar Chart
    builds = [b for b in build_list if b.id in (176,177,178)]
    builds[0].set_bra(default_bra)
    builds[1].set_filter1(default_cnae)
    builds[2].set_filter2(default_cbo)
    apps.append({
        "summary": gettext("A visualization using the height of bars to show the number of jobs in a specific wage bracket."),
        "builds": builds,
        "title": gettext(u"Bar Chart"),
        "type": "bar"
    })

    # Tree Map
    builds = [b for b in build_list if b.id in (3,95,117)]
    for b in builds: b.set_bra(default_bra)
    apps.append({
        "summary": gettext("A visualization using the area of rectangles to show shares of the specified value. The data is nested heirarchically by its given classificaiton."),
        "builds": builds,
        "title": gettext(u"Tree Map"),
        "type": "tree_map"
    })
    # Stacked
    builds = [b for b in build_list if b.id in (20,27,150)]
    for b in builds: b.set_bra(default_bra); b.set_filter1(default_cnae);
    apps.append({
        "summary": gettext("Similar to to a line chart, stacked area charts use an X and Y axis to show values across time. The data is nested heirarchically by its given classificaiton."),
        "builds": builds,
        "title": gettext(u"Stacked"),
        "type": "stacked"
    })
    # Geo Map
    builds = [b for b in build_list if b.id in (36,41,123)]
    for b in builds: b.set_bra(default_bra); b.set_filter1(default_hs);
    apps.append({
        "summary": gettext("Data values overlayed on a geographic map varying their color by the value they represent."),
        "builds": builds,
        "title": gettext(u"Geo Map"),
        "type": "geo_map"
    })
    # Network
    builds = [b for b in build_list if b.id in (33,35)]
    for b in builds: b.set_bra(default_bra)
    apps.append({
        "summary": gettext("A visualization showing the connections between a specified dataset. The specified attributes are then overlayed on this network to show their position in this fictional space."),
        "builds": builds,
        "title": gettext(u"Network"),
        "type": "network"
    })
    # Line
    builds = [b for b in build_list if b.id in (91,115,154)]
    for b in builds: b.set_bra(default_bra)
    apps.append({
        "summary": gettext("A type of chart which displays data as a time series with an X and Y axis."),
        "builds": builds,
        "title": gettext(u"Line Chart"),
        "type": "line"
    })
    # Rings
    builds = [b for b in build_list if b.id in (48,49,50)]
    for b in builds: b.set_bra(default_bra)
    builds[0].set_filter1("f41204");
    builds[1].set_filter2(default_cbo);
    builds[2].set_filter1(default_hs);
    apps.append({
        "summary": gettext("A visualization showing a network centered on a single node. The depth of nodes shown is computed by their distance from the root."),
        "builds": builds,
        "title": gettext(u"Rings"),
        "type": "rings"
    })
    # Scatter
    builds = [b for b in build_list if b.id in (44,46)]
    for b in builds: b.set_bra(default_bra)
    apps.append({
        "summary": gettext("A visualization showing two variables plotted along an X and Y axis."),
        "builds": builds,
        "title": gettext(u"Scatter"),
        "type": "scatter"
    })
    # Compare
    builds = [b for b in build_list if b.id in (52,53,113)]
    for b in builds: b.set_bra([default_bra, compare_bra])
    apps.append({
        "summary": gettext("Similar to the scatter visualization except this form of a scatter shows the same variable along both axes varrying the location for comparison purposes."),
        "builds": builds,
        "title": gettext(u"Compare"),
        "type": "compare"
    })
    # Occugrid
    builds = [b for b in build_list if b.id == 51]
    for b in builds: b.set_bra(default_bra); b.set_filter1(default_cnae);
    apps.append({
        "summary": gettext("A visualization showing the main occupations employed in various industries, their importance to that industry and the number of employees who work in these activities."),
        "builds": builds,
        "title": gettext(u"Occugrid"),
        "type": "occugrid"
    })
    # Box Plot
    builds = [b for b in build_list if b.id in (160,161)]
    for b in builds: b.set_bra(default_bra)
    apps.append({
        "summary": gettext("A visualization, also known as box and whisker diagram, used to display the distribution of data based on the five number summary: minimum, first quartile, median, third quartile, and maximum."),
        "builds": builds,
        "title": gettext(u"Box Plot"),
        "type": "box"
    })

    return render_template("apps/index.html", apps=apps)

def is_xhr():
    return request.is_xhr

@mod.route("/embed/")
@mod.route("/embed/<app_name>/<dataset>/<bra_id>/<filter1>/<filter2>/<output>/")
@view_cache.cached(key_prefix=api_cache_key("apps:embed"), unless=is_xhr)
def embed(app_name="tree_map", dataset="rais", bra_id="4mg",
          filter1="all", filter2="all", output="cbo"):
    prefix = "apps:embed:xhr:"
    lang = request.args.get('lang', None) or g.locale

    if (g.user is None or not g.user.is_authenticated()) and request.is_xhr:
        cache_id = prefix + request.path + lang
        cached_q = cached_query(cache_id)
        if cached_q:
            ret = make_response(cached_q)
            ret.headers['Content-Encoding'] = 'gzip'
            ret.headers['Content-Length'] = str(len(ret.data))
            return ret

    build_filter1, build_filter2 = filler(dataset, filter1, filter2)

    '''Grab attrs for bra and filters
    '''
    if bra_id == "all":
        bra_attr = Wld.query.get_or_404("sabra")
    else:
        bra_attr = [Bra.query.get_or_404(b) for b in bra_id.split("_")]
    filter1_attr = filter1
    filter2_attr = filter2
    if filter1 != "all":
        filter1_attr = globals()[build_filter1.capitalize()].query.get_or_404(filter1)
    if filter2 != "all":
        filter2_attr = globals()[build_filter2.capitalize()].query.get_or_404(filter2)

    if build_filter1 != "all":
        build_filter1 = "<{}>".format(build_filter1)
    if build_filter2 != "all":
        build_filter2 = "<{}>".format(build_filter2)

    '''This is an instance of the Build class for the selected app,
    determined by the combination of app_type, dataset, filters and output.
    '''
    current_app = App.query.filter_by(type=app_name).first_or_404()
    current_build = Build.query.filter_by(app=current_app, dataset=dataset, filter1=build_filter1, filter2=build_filter2, output=output).first_or_404()
    current_build.set_filter1(filter1_attr)
    current_build.set_filter2(filter2_attr)
    current_build.set_bra(bra_attr)

    '''Every possible build, required by the embed page for building the build
    dropdown.
    '''
    # all_builds = Build.query.all()
    # all_builds.sort(key=lambda x: x.dataset)
    # for build in all_builds:
    #     build.set_filter1(filter1_attr)
    #     build.set_filter2(filter2_attr)
    #     build.set_bra(bra_attr)

    '''Get URL query parameters from reqest.args object to return to the view.
    '''
    global_vars = {x[0]:x[1] for x in request.args.items()}
    if "controls" not in global_vars:
        global_vars["controls"] = "true"

    '''If user is logged in see if they have starred this app.'''
    starred = 0
    app_id = "/".join([app_name, dataset, bra_id, filter1, filter2, output])
    if g.user and g.user.is_authenticated():
        is_starred = Starred.query.filter_by(user=g.user, app_id=app_id).first()
        starred = 1 if is_starred else -1

    if request.is_xhr:
        ret = jsonify({
            "current_build": current_build.serialize(),
            # "all_builds": [b.json() for b in all_builds],
            "starred": starred
        })
        ret.data = gzip_data(ret.data)
        ret.headers['Content-Encoding'] = 'gzip'
        ret.headers['Content-Length'] = str(len(ret.data))
        if starred == 0 and cached_q is None:
            cached_query(cache_id, ret.data)
    else:

        year_range = json.dumps(__year_range__)

        ret = make_response(render_template("apps/embed.html",
            # apps = App.query.all(),
            # all_builds = all_builds,
            starred = starred,
            form = DownloadForm(),
            current_build = current_build,
            global_vars = json.dumps(global_vars),
            facebook_id = FACEBOOK_OAUTH_ID,
            year_range = year_range))
        ret.data = gzip_data(ret.data)
        ret.headers['Content-Encoding'] = 'gzip'
        ret.headers['Content-Length'] = str(len(ret.data))

    ret.headers.add('Last-Modified', datetime.now())
    ret.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    ret.headers.add('Pragma', 'no-cache')

    return ret

@mod.route('/star/<app_name>/<data_type>/<bra_id>/<filter1>/<filter2>/<output>/', methods=['GET', 'POST'])
def app_star(app_name, data_type, bra_id, filter1, filter2, output):

    app_id = "/".join([app_name, data_type, bra_id, filter1, filter2, output])

    # if request.method == 'POST' and request.remote_addr == SITE_MIRROR.split(":")[1][2:]:
    #     g.user = User.query.get(request.form["user"])
    if g.user is None or not g.user.is_authenticated():
        return jsonify({"error": gettext("You need to be logged in to star visualizations.")})

    starred = Starred.query.filter_by(user=g.user, app_id=app_id).first()

    if request.method == 'POST':

        # if "user" not in request.form:
        #     form_json = {"user": g.user.id, "title": request.form['title'].encode('utf-8')}
        #     try:
        #         opener = urllib2.urlopen("{0}{1}".format(SITE_MIRROR,request.path[1:]),urllib.urlencode(form_json),5)
        #     except:
        #         return jsonify({"error": gettext("The server is not responding. Please try again later.")})

        if starred:
            db.session.delete(starred)
            db.session.commit()
            return jsonify({"success": -1})
        else:
            app_name = request.form['title'].encode('utf-8')
            timestamp = datetime.utcnow()
            new_star = Starred(user=g.user, app_id=app_id, app_name=app_name, timestamp=timestamp)
            db.session.add(new_star)
            db.session.commit()
            return jsonify({"success": 1})

    if starred:
        return jsonify({"success": 1})
    else:
        return jsonify({"success": -1})

def get_builds(bra_attr, dataset, profile1, filter1, profile2, filter2, kwargs):
    builds = Build.query.filter_by(dataset=dataset, filter1=profile1, filter2=profile2).all()
    build_list = []
    for b in builds:
        if bra_attr and ((b.output == 'bra' and len(bra_attr.id) == 9) or (bra_attr.id == "sabra" and b.id in [48, 51])): # -- when looking at all Brazil, skip Occugrid/Rings
            continue
        if bra_attr:
            b.set_bra(bra_attr)
        if filter1 != 'all':
            b.set_filter1(filter1)
        if filter2 != 'all':
            b.set_filter2(filter2)
        build_list.append(b.json(**kwargs))
    return build_list

@mod.route('/recommend/', methods=['GET', 'POST'])
@mod.route('/recommend/<app_name>/<dataset>/<bra_id>/<filter1>/<filter2>/<output>/', methods=['GET', 'POST'])
@view_cache.cached(key_prefix=api_cache_key("apps:recommend"))
def recommend(app_name=None, dataset=None, bra_id="4mg", filter1=None, filter2=None, output=None):

    recommended = {}

    build_filter1, build_filter2 = filler(dataset, filter1, filter2)

    '''Grab attrs for bra and filters
    '''
    bra_all = [Wld.query.get_or_404("sabra")]
    if bra_id == "all":
        bra_attr = bra_all
    else:
        bra_attr = [Bra.query.get_or_404(b) for b in bra_id.split("_")]
    filter1_attr = filter1
    filter2_attr = filter2
    profile = False
    if filter1 != "all":
        filter1_attr = globals()[build_filter1.capitalize()].query.get_or_404(filter1)
        if output == build_filter1:
            profile = filter1_attr
            recommended["crosswalk"] = crosswalk_recs(dataset, build_filter1, filter1)
    if filter2 != "all":
        filter2_attr = globals()[build_filter2.capitalize()].query.get_or_404(filter2)
        if output == build_filter2:
            profile = filter2_attr
            recommended["crosswalk"] = crosswalk_recs(dataset, build_filter2, filter2)

    if profile == False and output == "bra":
        profile = bra_attr[0]
    if profile and output != "school":
        if g.locale == "pt":
            title = u"Perfil <{0}_para> <{0}>".format(output)
        else:
            title = u"Profile for <{0}>".format(output)
        recommended["profile"] = {
            "title": title_format(title, profile),
            "url": profile.url()
        }

    if build_filter1 != "all":
        build_filter1 = "<{}>".format(build_filter1)
    if build_filter2 != "all":
        build_filter2 = "<{}>".format(build_filter2)

    kwargs = {k: v for k, v in request.args.items()}
    if app_name == "geo_map" and len(bra_id) < 9:
        custom = Build.query.filter_by(app_id=3, dataset=dataset, filter1=build_filter1, filter2=build_filter2, output=output).first()
        custom.set_bra(bra_attr)
        custom.set_filter1(filter1_attr)
        custom.set_filter2(filter2_attr)
        recommended["custom"] = custom.json(**kwargs)

    for bra in bra_attr:
        recommended['builds'] = get_builds(bra, dataset, build_filter1, filter1_attr, build_filter2, filter2_attr, kwargs)
    if bra_id != "all" and output != "bra":
        recommended['builds'] += get_builds(bra_all[0], dataset, build_filter1, filter1_attr, build_filter2, filter2_attr, kwargs)

    return jsonify(recommended)

def get_geo_location(ip):
    req = urllib2.Request("http://freegeoip.net/json/" + ip)
    opener = urllib2.build_opener()
    try:
        f = opener.open(req)
    except:
        return None
    json_resp = json.loads(f.read())
    city = json_resp["city"]
    # city = "Viana"
    state = json_resp["region_name"]
    # state = "Espírito Santo"
    # state = "Maranhão"

    # first try to find the exact city within the state
    bra_state = Bra.query.filter_by(name_pt=state).filter(func.char_length(Bra.id) == 3).first()
    bra_cities = Bra.query.filter_by(name_pt=city).filter(func.char_length(Bra.id) == 9)
    if bra_state:
        if bra_cities.count() == 1:
            return bra_cities.first()
        elif bra_cities.count() > 1:
            return bra_cities.filter(Bra.id.like(bra_state.id+'%')).first()
        return None
    return None

@mod.route('/builder/')
@mod.route('/builder/tree_map/', defaults={"app_name": "tree_map", "dataset": "secex", "bra_id": "4mg",
            "filter1": "all", "filter2": "all", "output": "hs", "params": ""})
@mod.route('/builder/stacked/', defaults={"app_name": "stacked", "dataset": "rais", "bra_id": "4mg",
            "filter1": "all", "filter2": "all", "output": "cbo", "params": ""})
@mod.route('/builder/geo_map/', defaults={"app_name": "geo_map", "dataset": "rais", "bra_id": "4mg",
            "filter1": "all", "filter2": "all", "output": "bra", "params": "?value_var=wage"})
@mod.route('/builder/network/', defaults={"app_name": "network", "dataset": "secex", "bra_id": "4mg",
            "filter1": "all", "filter2": "all", "output": "hs", "params": ""})
@mod.route('/builder/rings/', defaults={"app_name": "rings", "dataset": "rais", "bra_id": "4mg",
            "filter1": "all", "filter2": "2211", "output": "cbo", "params": ""})
@mod.route('/builder/scatter/', defaults={"app_name": "scatter", "dataset": "secex", "bra_id": "4mg",
            "filter1": "all", "filter2": "all", "output": "hs", "params": "?rca_scope=wld_rca"})
@mod.route('/builder/compare/', defaults={"app_name": "compare", "dataset": "rais", "bra_id": "4mg_4rj",
            "filter1": "all", "filter2": "all", "output": "cbo", "params": "?depth=cbo_4&axes=wage_avg"})
@mod.route('/builder/occugrid/', defaults={"app_name": "occugrid", "dataset": "rais", "bra_id": "4mg",
            "filter1": "c14126", "filter2": "all", "output": "cbo", "params": ""})
@mod.route('/builder/line/', defaults={"app_name": "line", "dataset": "secex", "bra_id": "4mg",
            "filter1": "all", "filter2": "all", "output": "balance", "params": ""})
@mod.route('/builder/box/', defaults={"app_name": "box", "dataset": "sc", "bra_id": "4mg",
            "filter1": "all", "filter2": "all", "output": "age", "params": ""})
@mod.route('/builder/bar/', defaults={"app_name": "bar", "dataset": "rais", "bra_id": "4mg",
            "filter1": "all", "filter2": "all", "output": "bra", "params": ""})
@mod.route('/builder/<app_name>/<dataset>/<bra_id>/<filter1>/<filter2>/<output>/')
@view_cache.cached(key_prefix=api_cache_key("apps:builder"))
def builder(app_name=None, dataset=None, bra_id=None, filter1=None,
                filter2=None, output=None, params=None):
    if bra_id == 'bra':
        bra_id = 'all'
        return redirect('/{0}/{1}/{2}/{3}/{4}/{5}/{6}/{7}?{8}'.format(g.locale, 'apps/builder', app_name, dataset, bra_id, filter1, filter2, output, request.query_string))
    if len(request.path.split("/")) == 6:
        return redirect('{0}{1}/{2}/{3}/{4}/{5}/{6}'.format(request.path, dataset, bra_id, filter1, filter2, output, request.query_string))
    g.page_type = "builder"
    builds = Build.query.all()
    builds = [b.json(fill=False) for b in builds]
    rais_builds = [b.copy() for b in builds if b["dataset"] == "rais" and b["app"]["type"] not in ("network", "occugrid", "rings")]
    builds = [b for b in builds if b["app"]["type"] not in ("bar", "box") or b["dataset"] != "rais"]
    def size_var(b):
        app = b["app"]["type"]
        if app in ["line", "stacked"]:
            return "y"
        elif app == "geo_map":
            return "color"
        elif app == "compare":
            return "axes"
        return "size"
    for b in builds:
        if b["dataset"] == "rais":
            b["url"] = "{}?{}=num_jobs".format(b["url"], size_var(b))
    for b in rais_builds:
        if b["app"]["type"] not in ("bar", "box"):
            b["id"] = "{}b".format(int(b["id"]))
            b["url"] = "{}?{}=wage".format(b["url"], size_var(b))
        b["dataset"] = "rais_wages"
    builds = rais_builds + builds
    dataset_sort = ["rais_wages", "rais", "hedu", "sc", "secex"]
    builds.sort(key=lambda x: (x["app"]["id"], dataset_sort.index(x["dataset"])))
    datatset_names = {
        "secex": gettext("International Trade"),
        "rais": gettext("Employment"),
        "rais_wages": gettext("Wages"),
        "ei": gettext("Domestic Trade"),
        "hedu": gettext("Higher Education"),
        "sc": gettext("School Census")
    }
    if "_" in bra_id:
        bra_id, bra_1_id = bra_id.split("_")
    else:
        bra_1_id = "all"
    filters = [
        ["bra", str(bra_id)],
        ["bra_1", str(bra_1_id)],
        ["cnae", "all"],
        ["cbo", "all"],
        ["hs", "all"],
        ["wld", "all"],
        ["university", "all"],
        ["course_hedu", "all"],
        ["school", "all"],
        ["course_sc", "all"]
    ]
    if dataset == "secex":
        filters[4][1] = str(filter1)
        filters[5][1] = str(filter2)
    elif dataset == "rais":
        filters[2][1] = str(filter1)
        filters[3][1] = str(filter2)
    elif dataset == "hedu":
        filters[6][1] = str(filter1)
        filters[7][1] = str(filter2)
    elif dataset == "sc":
        filters[8][1] = str(filter1)
        filters[9][1] = str(filter2)

    build_filter1, build_filter2 = filler(dataset, filter1, filter2)

    '''Grab attrs for bra and filters
    '''
    if bra_id == "all":
        bra_attr = Wld.query.get_or_404("sabra")
    else:
        bra_attr = [Bra.query.get_or_404(bra_id)]
        if bra_1_id != "all":
            bra_attr.append(Bra.query.get_or_404(bra_1_id))
    filter1_attr = filter1
    filter2_attr = filter2
    if filter1 != "all":
        filter1_attr = globals()[build_filter1.capitalize()].query.get_or_404(filter1)
    if filter2 != "all":
        filter2_attr = globals()[build_filter2.capitalize()].query.get_or_404(filter2)

    if build_filter1 != "all":
        build_filter1 = "<{}>".format(build_filter1)
    if build_filter2 != "all":
        build_filter2 = "<{}>".format(build_filter2)

    '''This is an instance of the Build class for the selected app,
    determined by the combination of app_type, dataset, filters and output.
    '''
    current_app = App.query.filter_by(type=app_name).first_or_404()
    build = Build.query.filter_by(app=current_app, dataset=dataset, filter1=build_filter1, filter2=build_filter2, output=output).first_or_404()
    build.set_filter1(filter1_attr)
    build.set_filter2(filter2_attr)
    build.set_bra(bra_attr)
    build = build.serialize()
    if build["dataset"] == "rais" and build["app"]["type"] in ("bar", "box"):
        build["dataset"] = "rais_wages"
    else:
        for p, v in request.args.items():
            if (v == "wage" or v == "wage_avg") and build["dataset"] == "rais" and build["app"]["type"] in ("bar", "box") and b["app"]["type"] not in ("network", "occugrid", "rings"):
                build["id"] = "{}b".format(int(build["id"]))
                build["url"] = "{}?{}={}".format(build["url"], size_var(build), v)
                build["dataset"] = "rais_wages"
                break

    return render_template("apps/builder.html",
        app=app_name, apps=App.query.all(), builds=builds, build=build,
        filters=filters, dataset=dataset, datatset_names=datatset_names)

@mod.route('/download/', methods=['GET', 'POST'])
def download():
    import tempfile, subprocess, random

    form = DownloadForm()
    data = form.data.data
    format = form.output_format.data
    title = form.title.data
    downloadToken = form.downloadToken.data
    max_length = 250 - (len(downloadToken) + 1)
    title_safe = title[:max_length]
    filenameDownload = title_safe + "-" + downloadToken

    if format == "png":
        mimetype='image/png'
    elif format == "pdf":
        mimetype='application/pdf'
    elif format == "svg":
        mimetype='application/octet-stream'
    elif format == "csv":
        mimetype="text/csv;charset=UTF-16"
    elif format == "url2csv":
        mimetype="text/csv;charset=UTF-16"

    if format == "png" or format == "pdf":
        temp = tempfile.NamedTemporaryFile()
        temp.write(data.encode("utf-16"))
        temp.seek(0)
        zoom = "1"
        background = "#ffffff"
        p = subprocess.Popen(["rsvg-convert", "-z", zoom, "-f", format, "--background-color={0}".format(background), temp.name], stdout=subprocess.PIPE)
        out, err = p.communicate()
        response_data = out
    else:
        response_data = data.encode("utf-16")
        #print response_data

    content_disposition = "attachment;filename=%s.%s" % (title_safe, format)
    content_disposition = content_disposition.replace(",", "_")

    download_file = make_response(Response(response_data,
                       mimetype=mimetype,
                        headers={"Content-Disposition": content_disposition}))

    with open(os.path.join(basedir, "dataviva/static/downloads/"+title_safe+"."+format),"wb") as fo:
        fo.write(response_data)

    zf = zipfile.ZipFile(os.path.join(basedir, "dataviva/static/downloads/"+filenameDownload+".zip"), mode='w')
    try:
        zf.write(os.path.join(basedir, "dataviva/static/downloads/"+title_safe+"."+format), title_safe+"."+format)
    finally:
        zf.close()

    os.remove(os.path.join(basedir, "dataviva/static/downloads/"+title_safe+"."+format))

    return "/static/downloads/"+filenameDownload+".zip"



@mod.route('/info/<app_name>/')
def info(app_name="tree_map"):
    return render_template("apps/info.html", app_name=app_name)

@mod.route('/coords/<id>/')
def coords(id="all"):
    if GZIP_DATA:
        fileext=".gz"
        filetype="gzip"
    else:
        fileext=""
        filetype="json"

    if id == "all":
        file_name = "bra_states.json"+fileext
    else:
        file_name = ("{0}_munic.json"+fileext).format(id)

    cached_q = cached_query(file_name)
    if cached_q:
        ret = make_response(cached_q)
    else:
        path = datavivadir+"/static/json/coords/{0}".format(file_name)
        gzip_file = open(path).read()
        cached_query(file_name, gzip_file)
        ret = make_response(gzip_file)

    ret.headers['Content-Encoding'] = filetype
    ret.headers['Content-Length'] = str(len(ret.data))

    return ret

@mod.route('/networks/<type>/')
def networks(type="hs"):
    if GZIP_DATA:
        fileext=".gz"
        filetype="gzip"
    else:
        fileext=""
        filetype="json"
    file_name = ("network_{0}.json"+fileext).format(type)
    cached_q = cached_query(file_name)
    if cached_q:
        ret = make_response(cached_q)
    else:
        path = datavivadir+"/static/json/networks/{0}".format(file_name)
        gzip_file = open(path).read()
        cached_query(file_name, gzip_file)
        ret = make_response(gzip_file)

    ret.headers['Content-Encoding'] = filetype
    ret.headers['Content-Length'] = str(len(ret.data))

    return ret

@mod.route('/shorten/', methods=['GET', 'POST'])
def shorten_url():

    if request.method == 'POST':

        long_url = urllib.unquote(request.form["url"].encode('utf-8')).decode("utf-8")

        short = Short.query.filter_by(long_url = long_url).first()
        if short is None:
            slug = Short.make_unique_slug(long_url)
            short = Short(slug = slug, long_url = long_url)
            db.session.add(short)
            db.session.commit()

        return jsonify({"slug": short.slug})

    return jsonify({"error": "No URL given."})


def crosswalk_recs(dataset, filter, id):
    crosswalk = []

    attr_swap = {"hs" : "cnae", "cnae": "hs", "cbo" : "course_hedu", "course_hedu": "cbo"}
    crosswalk_table = {"hs" : "pi", "cnae": "pi", "cbo" : "oc", "course_hedu": "oc"}

    if filter in attr_swap and id != "all":
        table = globals()["Crosswalk_{}".format(crosswalk_table[filter])]
        col = getattr(table, "{}_id".format(filter))
        results = table.query.filter(col == id)
        ids = [row.get_id(dataset) for row in results]
        if ids:
            ids = Search.query.filter(Search.id.in_(ids)).filter(Search.kind == attr_swap[filter]).all()
            ids = [a.id for a in ids]
            table = globals()[attr_swap[filter].capitalize()]
            attrs = table.query.filter(table.id.in_(ids)).all()
            crosswalk = [{"title": a.name(), "url": a.url(), "type": attr_swap[filter]} for a in attrs]

    return crosswalk
