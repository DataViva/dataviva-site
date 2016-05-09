# -*- coding: utf-8 -*-
from io import BytesIO
import time
from StringIO import StringIO
from datetime import datetime
from collections import defaultdict
from sqlalchemy import func
from random import randint
from flask import Blueprint, request, render_template, g, Response, make_response, send_file, jsonify, url_for, redirect, jsonify
from flask.ext.babel import gettext

from dataviva import db, datavivadir, __year_range__, view_cache
from dataviva.api.attrs.models import Bra, Cnae, Hs, Cbo, Wld, University, Course_hedu, Course_sc, Search
from dataviva.api.rais.views import rais_api

from dataviva.apps.general.views import get_locale
from dataviva.apps.data.forms import DownloadForm
from dataviva.apps.account.models import User, Starred
from dataviva.apps.embed.models import Build, UI, App, Crosswalk_oc, Crosswalk_pi
from dataviva.apps.general.models import Short

from dataviva.translations.translate import translate
from dataviva.utils.gzip_data import gzip_data
from dataviva.utils.cached_query import cached_query, api_cache_key
from dataviva.utils.title_format import title_format

import json
import urllib2
import urllib
from config import FACEBOOK_OAUTH_ID, basedir, GZIP_DATA
import os
import urlparse
import random
import zipfile
import sys
import gzip
from dataviva.utils.cached_query import api_cache_key


mod = Blueprint('embed', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/embed')


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


def is_xhr():
    return request.is_xhr


@mod.route("/")
@mod.route("/<app_name>/<dataset>/<bra_id>/<filter1>/<filter2>/<output>/")
#@view_cache.cached(key_prefix=api_cache_key("apps:embed"), unless=is_xhr)
def embed(app_name="tree_map", dataset="rais", bra_id="4mg",
          filter1="all", filter2="all", output="cbo"):
    prefix = "apps:embed:xhr:"
    lang = request.args.get('lang', None) or g.locale

    if (g.user is None or not g.user.is_authenticated) and request.is_xhr:
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
        filter1_attr = globals()[build_filter1.capitalize()].query.get_or_404(
            filter1)
    if filter2 != "all":
        filter2_attr = globals()[build_filter2.capitalize()].query.get_or_404(
            filter2)

    if build_filter1 != "all":
        build_filter1 = "<{}>".format(build_filter1)
    if build_filter2 != "all":
        build_filter2 = "<{}>".format(build_filter2)

    '''This is an instance of the Build class for the selected app,
    determined by the combination of app_type, dataset, filters and output.
    '''
    current_app = App.query.filter_by(type=app_name).first_or_404()
    current_build = Build.query.filter_by(
        app=current_app, dataset=dataset, filter1=build_filter1, filter2=build_filter2, output=output).first_or_404()
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
    global_vars = {x[0]: x[1] for x in request.args.items()}
    if "controls" not in global_vars:
        global_vars["controls"] = "true"

    '''If user is logged in see if they have starred this app.'''
    starred = 0
    app_id = "/".join([app_name, dataset, bra_id, filter1, filter2, output])
    if g.user and g.user.is_authenticated:
        is_starred = Starred.query.filter_by(
            user=g.user, app_id=app_id).first()
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

        year_range_dict = __year_range__.copy()

        if current_build.app.type in ['network', 'rings', 'scatter']:
            year_range_dict["secex"] = ["2000-1", "2015-12"]

        year_range = json.dumps(year_range_dict)

        ret = make_response(render_template("embed/embed.html",
                                            # apps = App.query.all(),
                                            # all_builds = all_builds,
                                            starred=starred,
                                            form=DownloadForm(),
                                            current_build=current_build,
                                            global_vars=json.dumps(
                                                global_vars),
                                            facebook_id=FACEBOOK_OAUTH_ID,
                                            year_range=year_range))
        ret.data = gzip_data(ret.data)
        ret.headers['Content-Encoding'] = 'gzip'
        ret.headers['Content-Length'] = str(len(ret.data))

    ret.headers.add('Last-Modified', datetime.now())
    ret.headers.add(
        'Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    ret.headers.add('Pragma', 'no-cache')

    return ret


@mod.route('/star/<app_name>/<data_type>/<bra_id>/<filter1>/<filter2>/<output>/', methods=['GET', 'POST'])
def app_star(app_name, data_type, bra_id, filter1, filter2, output):

    app_id = "/".join([app_name, data_type, bra_id, filter1, filter2, output])

    # if request.method == 'POST' and request.remote_addr == SITE_MIRROR.split(":")[1][2:]:
    #     g.user = User.query.get(request.form["user"])
    if g.user is None or not g.user.is_authenticated:
        return jsonify({"error": gettext("You need to be logged in to star visualizations.")})

    starred = Starred.query.filter_by(user=g.user, app_id=app_id).first()

    if request.method == 'POST':

        # if "user" not in request.form:
        #     form_json = {"user": g.user.id, "title": request.form['title'].encode('utf-8')}
        #     try:
        #         opener = urllib2.urlopen("{0}{1}".format(SITE_MIRROR,request.path[1:]),urllib.urlencode(form_json),5)
        #     except:
        # return jsonify({"error": gettext("The server is not responding.
        # Please try again later.")})

        if starred:
            db.session.delete(starred)
            db.session.commit()
            return jsonify({"success": -1})
        else:
            app_name = request.form['title'].encode('utf-8')
            timestamp = datetime.utcnow()
            new_star = Starred(
                user=g.user, app_id=app_id, app_name=app_name, timestamp=timestamp)
            db.session.add(new_star)
            db.session.commit()
            return jsonify({"success": 1})

    if starred:
        return jsonify({"success": 1})
    else:
        return jsonify({"success": -1})


def get_builds(bra_attr, dataset, profile1, filter1, profile2, filter2, kwargs):
    builds = Build.query.filter_by(
        dataset=dataset, filter1=profile1, filter2=profile2).all()
    build_list = []
    for b in builds:
        # -- when looking at all Brazil, skip Occugrid/Rings
        if bra_attr and ((b.output == 'bra' and len(bra_attr.id) == 9) or (bra_attr.id == "sabra" and b.id in [48, 51])):
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
#@view_cache.cached(key_prefix=api_cache_key("apps:recommend"))
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
        filter1_attr = globals()[build_filter1.capitalize()].query.get_or_404(
            filter1)
        if output == build_filter1:
            profile = filter1_attr
            recommended["crosswalk"] = crosswalk_recs(
                dataset, build_filter1, filter1)
    if filter2 != "all":
        filter2_attr = globals()[build_filter2.capitalize()].query.get_or_404(
            filter2)
        if output == build_filter2:
            profile = filter2_attr
            recommended["crosswalk"] = crosswalk_recs(
                dataset, build_filter2, filter2)

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
        custom = Build.query.filter_by(
            app_id=3, dataset=dataset, filter1=build_filter1, filter2=build_filter2, output=output).first()
        custom.set_bra(bra_attr)
        custom.set_filter1(filter1_attr)
        custom.set_filter2(filter2_attr)
        recommended["custom"] = custom.json(**kwargs)

    for bra in bra_attr:
        recommended['builds'] = get_builds(
            bra, dataset, build_filter1, filter1_attr, build_filter2, filter2_attr, kwargs)
    if bra_id != "all" and output != "bra":
        recommended['builds'] += get_builds(
            bra_all[0], dataset, build_filter1, filter1_attr, build_filter2, filter2_attr, kwargs)

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
    bra_state = Bra.query.filter_by(name_pt=state).filter(
        func.char_length(Bra.id) == 3).first()
    bra_cities = Bra.query.filter_by(name_pt=city).filter(
        func.char_length(Bra.id) == 9)
    if bra_state:
        if bra_cities.count() == 1:
            return bra_cities.first()
        elif bra_cities.count() > 1:
            return bra_cities.filter(Bra.id.like(bra_state.id+'%')).first()
        return None
    return None


@mod.route('/download/', methods=['GET', 'POST'])
def download():
    import tempfile
    import subprocess
    import random

    form = DownloadForm()
    data = form.data.data
    format = form.output_format.data
    title = form.title.data
    downloadToken = form.downloadToken.data
    max_length = 250 - (len(downloadToken) + 1)
    title_safe = title[:max_length]
    filenameDownload = title_safe + "-" + downloadToken

    if format == "png":
        mimetype = 'image/png'
    elif format == "pdf":
        mimetype = 'application/pdf'
    elif format == "svg":
        mimetype = 'application/octet-stream'
    elif format == "csv":
        mimetype = "text/csv;charset=UTF-16"
    elif format == "url2csv":
        mimetype = "text/csv;charset=UTF-16"

    if format == "png" or format == "pdf":
        temp = tempfile.NamedTemporaryFile()
        temp.write(data.encode("utf-16"))
        temp.seek(0)
        zoom = "1"
        background = "#ffffff"
        p = subprocess.Popen(["rsvg-convert", "-z", zoom, "-f", format,
                              "--background-color={0}".format(background), temp.name], stdout=subprocess.PIPE)
        out, err = p.communicate()
        response_data = out
    else:
        response_data = data.encode("utf-16")
        # print response_data

    content_disposition = "attachment;filename=%s.%s" % (title_safe, format)
    content_disposition = content_disposition.replace(",", "_")

    download_file = make_response(Response(response_data,
                                           mimetype=mimetype,
                                           headers={"Content-Disposition": content_disposition}))

    with open(os.path.join(basedir, "dataviva/static/downloads/" + title_safe + "." + format), "wb") as fo:
        fo.write(response_data)

    zf = zipfile.ZipFile(os.path.join(
        basedir, "dataviva/static/downloads/" + filenameDownload + ".zip"), mode='w')
    try:
        zf.write(os.path.join(basedir, "dataviva/static/downloads/" +
                              title_safe + "." + format), title_safe + "." + format)
    finally:
        zf.close()

    os.remove(os.path.join(basedir, "dataviva/static/downloads/" + title_safe + "." + format))

    return "/static/downloads/" + filenameDownload + ".zip"


@mod.route('/info/<app_name>/')
def info(app_name="tree_map"):
    return render_template("embed/info.html", app_name=app_name)


@mod.route('/coords/<id>/')
def coords(id="all"):
    if GZIP_DATA:
        fileext = ".gz"
        filetype = "gzip"
    else:
        fileext = ""
        filetype = "json"

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
        fileext = ".gz"
        filetype = "gzip"
    else:
        fileext = ""
        filetype = "json"
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

        long_url = urllib.unquote(
            request.form["url"].encode('utf-8')).decode("utf-8")

        short = Short.query.filter_by(long_url=long_url).first()
        if short is None:
            slug = Short.make_unique_slug(long_url)
            short = Short(slug=slug, long_url=long_url)
            db.session.add(short)
            db.session.commit()

        return jsonify({"slug": short.slug})

    return jsonify({"error": "No URL given."})


def crosswalk_recs(dataset, filter, id):
    crosswalk = []

    attr_swap = {"hs": "cnae", "cnae": "hs",
                 "cbo": "course_hedu", "course_hedu": "cbo"}
    crosswalk_table = {
        "hs": "pi", "cnae": "pi", "cbo": "oc", "course_hedu": "oc"}

    if filter in attr_swap and id != "all":
        table = globals()["Crosswalk_{}".format(crosswalk_table[filter])]
        col = getattr(table, "{}_id".format(filter))
        results = table.query.filter(col == id)
        ids = [row.get_id(dataset) for row in results]
        if ids:
            ids = Search.query.filter(Search.id.in_(ids)).filter(
                Search.kind == attr_swap[filter]).all()
            ids = [a.id for a in ids]
            table = globals()[attr_swap[filter].capitalize()]
            attrs = table.query.filter(table.id.in_(ids)).all()
            crosswalk = [
                {"title": a.name(), "url": a.url(), "type": attr_swap[filter]} for a in attrs]

    return crosswalk
