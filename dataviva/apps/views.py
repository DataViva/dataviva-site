# -*- coding: utf-8 -*-
import urllib2, json
from datetime import datetime
from collections import defaultdict
from sqlalchemy import func
from random import randint
from flask import Blueprint, request, render_template, g, Response, make_response, send_file, jsonify, url_for, redirect
from flask.ext.babel import gettext

from dataviva import db, datavivadir
from dataviva.data.forms import DownloadForm
from dataviva.account.models import User, Starred
from dataviva.attrs.models import Bra, Isic, Hs, Cbo, Wld
from dataviva.apps.models import Build, UI, App
from dataviva.general.models import Short

from dataviva.rais.views import rais_ybi
from dataviva.utils import gzip_data, cached_query

import json, urllib2, urllib
from config import FACEBOOK_OAUTH_ID

mod = Blueprint('apps', __name__, url_prefix='/apps')

@mod.before_request
def before_request():
    g.page_type = mod.name

    g.color = "#af1f24"

    g.sabrina = {
        "outfit": "lab",
        "face": "smirk",
        "hat": "glasses"
    }

@mod.route('/embed/', defaults={"app_name": "tree_map", "dataset": "rais",
            "bra_id": "mg", "filter1": "all", "filter2": "all", "output": "cbo"})
@mod.route('/embed/<app_name>/<dataset>/<bra_id>/<filter1>/<filter2>/'
            '<output>/')
def embed(app_name=None, dataset=None, bra_id=None, filter1=None, filter2=None,
            output=None):

    lang = request.args.get('lang', None) or g.locale

    if (g.user is None or not g.user.is_authenticated()) and request.is_xhr:
        cache_id = request.path + lang
        cached_q = cached_query(cache_id)
        if cached_q:
            ret = make_response(cached_q)
            ret.headers['Content-Encoding'] = 'gzip'
            ret.headers['Content-Length'] = str(len(ret.data))
            return ret
    '''Since the "builds" are held in the database with placeholders for
    attributes i.e. <cbo>, <hs>, <isic> we need to convert the IDs given
    in the URL to these placeholders. i.e.
         - a0111    = <isic>
         - 010101   = <hs>
         - all      = all
    '''
    build_filter1 = filter1
    if dataset == "rais" and build_filter1 != "all":
        build_filter1 = "<isic>"
    if dataset == "secex" and build_filter1 != "all":
        build_filter1 = "<hs>"

    build_filter2 = filter2
    if dataset == "rais" and build_filter2 != "all":
        build_filter2 = "<cbo>"
    if dataset == "secex" and build_filter2 != "all":
        build_filter2 = "<wld>"

    '''This is an instance of the Build class for the selected app,
    determined by the combination of app_type, dataset, filters and output.
    '''
    current_app = App.query.filter_by(type=app_name).first_or_404()
    current_build = Build.query.filter_by(app=current_app, dataset=dataset, filter1=build_filter1, filter2=build_filter2, output=output).first_or_404()
    current_build.set_filter1(filter1)
    current_build.set_filter2(filter2)
    current_build.set_bra(bra_id)

    '''Get the recommended app list to pass with data'''
    filler_bra = bra_id
    filler1 = filter1
    filler2 = filter2
    if output == "isic" or output == "hs":
        filler1 = "filler"
    elif output == "cbo" or output == "wld":
        filler2 = "filler"
    elif output == "bra":
        filler_bra = "filler"

    recs = recommend(app_name=app_name, dataset=dataset, bra_id=filler_bra, \
                        filter1=filler1, filter2=filler2, output=output)

    '''Every possible build, required by the embed page for building the build
    dropdown.
    '''
    all_builds = Build.query.all()
    for build in all_builds:
        build.set_filter1(filter1)
        build.set_filter2(filter2)
        build.set_bra(bra_id)

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

    '''Get the actual data for the current build'''
    # view_data = rais_ybi(bra_id='sp', isic_id='a0112').data
    # app.url_map.bind('/').match('/attrs/wld/nausa/')

    if request.is_xhr:
        ret = jsonify({
            "current_build": current_build.serialize(),
            "all_builds": [b.serialize() for b in all_builds],
            "recommendations": json.loads(recs.data),
            "starred": starred
        })
        ret.data = gzip_data(ret.data)
        ret.headers['Content-Encoding'] = 'gzip'
        ret.headers['Content-Length'] = str(len(ret.data))
        if starred == 0 and cached_q is None:
            cached_query(cache_id, ret.data)
    else:
        ret = make_response(render_template("apps/embed.html",
            all_builds = all_builds,
            starred = starred,
            form = DownloadForm(),
            current_build = current_build,
            global_vars = json.dumps(global_vars),
            facebook_id = FACEBOOK_OAUTH_ID))

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
        return jsonify({"error": gettext("You need to be logged in to star apps.")})

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

@mod.route('/recommend/', methods=['GET', 'POST'])
@mod.route('/recommend/<app_name>/<dataset>/<bra_id>/<filter1>/<filter2>/<output>/', methods=['GET', 'POST'])
def recommend(app_name=None, dataset=None, bra_id="mg", filter1=None, filter2=None, output=None):

    recommended = {}

    '''Since the "builds" are held in the database with placeholders for
    attributes i.e. <cbo>, <hs>, <isic> we need to convert the IDs given
    in the URL to these placeholders. i.e.
         - a0111    = <isic>
         - 010101   = <hs>
         - all      = all
    '''
    build_filter1 = filter1
    if dataset == "rais" and build_filter1 != "all":
        build_filter1 = "<isic>"
    if dataset == "secex" and build_filter1 != "all":
        build_filter1 = "<hs>"

    build_filter2 = filter2
    if dataset == "rais" and build_filter2 != "all":
        build_filter2 = "<cbo>"
    if dataset == "secex" and build_filter2 != "all":
        build_filter2 = "<wld>"

    '''First get the MOST relevent builds (ones that use all filters)'''
    if build_filter1 != "all" and build_filter2 != "all":
        builds = Build.query.filter_by(dataset=dataset, filter1=build_filter1,
                    filter2=build_filter2).all()
        recommended['both_filters'] = []
        for b in builds:
            if bra_id != "filler":
                b.set_bra(bra_id)
            if filter1 != "filler":
                b.set_filter1(filter1)
            if filter2 != "filler":
                b.set_filter2(filter2)
            recommended['both_filters'].append(b.serialize())
    else:

        '''Add any builds that rely strictly on the second filter'''
        if build_filter2 != "all":
            builds = Build.query.filter_by(dataset=dataset, filter1="all",
                        filter2=build_filter2).all()
            recommended['filter2'] = []
            for b in builds:
                if bra_id != "filler":
                    b.set_bra(bra_id)
                if filter2 != "filler":
                    b.set_filter2(filter2)
                recommended['filter2'].append(b.serialize())

        '''Add any builds that rely strictly on the first filter'''
        if build_filter1 != "all":
            builds = Build.query.filter_by(dataset=dataset, filter1=build_filter1,
                        filter2="all").all()
            recommended['filter1'] = []
            for b in builds:
                if bra_id != "filler":
                    b.set_bra(bra_id)
                if filter1 != "filler":
                    b.set_filter1(filter1)
                recommended['filter1'].append(b.serialize())

        '''Lastly get the rest of the relevent builds'''
        if build_filter1 == "all" and build_filter2 == "all":
            builds = Build.query.filter_by(dataset=dataset, filter1="all", filter2="all").all()
            recommended['no_filters'] = []
            for b in builds:
                if bra_id != "filler":
                    b.set_bra(bra_id)
                recommended['no_filters'].append(b.serialize())

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
    bra_state = Bra.query.filter_by(name_pt=state).filter(func.char_length(Bra.id) == 2).first()
    bra_cities = Bra.query.filter_by(name_pt=city).filter(func.char_length(Bra.id) == 8)
    if bra_state:
        if bra_cities.count() == 1:
            return bra_cities.first()
        elif bra_cities.count() > 1:
            return bra_cities.filter(Bra.id.like(bra_state.id+'%')).first()
        return None
    return None

@mod.route('/builder/')
@mod.route('/builder/tree_map/', defaults={"app_name": "tree_map", "dataset": "secex", "bra_id": "mg",
            "filter1": "all", "filter2": "all", "output": "hs", "params": ""})
@mod.route('/builder/stacked/', defaults={"app_name": "stacked", "dataset": "rais", "bra_id": "mg",
            "filter1": "all", "filter2": "all", "output": "cbo", "params": ""})
@mod.route('/builder/geo_map/', defaults={"app_name": "geo_map", "dataset": "rais", "bra_id": "mgplr02",
            "filter1": "all", "filter2": "all", "output": "bra", "params": "?value_var=wage"})
@mod.route('/builder/network/', defaults={"app_name": "network", "dataset": "secex", "bra_id": "mg",
            "filter1": "all", "filter2": "all", "output": "hs", "params": ""})
@mod.route('/builder/rings/', defaults={"app_name": "rings", "dataset": "rais", "bra_id": "mg",
            "filter1": "all", "filter2": "2211", "output": "cbo", "params": ""})
@mod.route('/builder/scatter/', defaults={"app_name": "scatter", "dataset": "secex", "bra_id": "mg",
            "filter1": "all", "filter2": "all", "output": "hs", "params": "?rca_scope=wld_rca"})
@mod.route('/builder/compare/', defaults={"app_name": "compare", "dataset": "rais", "bra_id": "mg_rj",
            "filter1": "all", "filter2": "all", "output": "cbo", "params": "?depth=cbo_4&axes=wage_avg"})
@mod.route('/builder/occugrid/', defaults={"app_name": "occugrid", "dataset": "rais", "bra_id": "mg030000",
            "filter1": "m7310", "filter2": "all", "output": "cbo", "params": ""})
@mod.route('/builder/<app_name>/<dataset>/<bra_id>/<filter1>/<filter2>/<output>/')
def builder(app_name=None, dataset=None, bra_id=None, filter1=None,
                filter2=None, output=None, params=None):
    path = request.path.split("/")
    if len(path) == 5:
        return redirect('{0}{1}/{2}/{3}/{4}/{5}/{6}'.format("/".join(path),dataset,bra_id,filter1,filter2,output,params))
    g.page_type = "builder"
    return render_template("apps/builder.html")

@mod.route('/download/', methods=['GET', 'POST'])
def download():
    import tempfile, subprocess
    
    form = DownloadForm()

    data = form.data.data
    format = form.output_format.data
    title = form.title.data
    downloadToken = form.downloadToken.data

    temp = tempfile.NamedTemporaryFile()
    temp.write(data.encode("utf-16"))
    temp.seek(0)

    if format == "png":
        mimetype='image/png'
    elif format == "pdf":
        mimetype='application/pdf'
    elif format == "svg":
        mimetype='application/octet-stream'
    elif format == "csv":
        mimetype="text/csv;charset=UTF-16"

    if format == "png" or format == "pdf":
        zoom = "1"
        background = "#ffffff"
        p = subprocess.Popen(["rsvg-convert", "-z", zoom, "-f", format, "--background-color={0}".format(background), temp.name], stdout=subprocess.PIPE)
        out, err = p.communicate()
        response_data = out
    else:
        response_data = data.encode("utf-16")
    
    content_disposition = "attachment;filename=%s.%s" % (title, format)
    content_disposition = content_disposition.replace(",", "_")
    
    download_file = make_response(Response(response_data,
                        mimetype=mimetype,
                        headers={"Content-Disposition": content_disposition}))
    
    download_file.set_cookie('downloadToken', downloadToken)
    
    return download_file

@mod.route('/info/<app_name>/')
def info(app_name="tree_map"):
    return render_template("apps/info.html", app_name=app_name)

@mod.route('/coords/<id>/')
def coords(id="all"):
    if id == "all":
        file_name = "bra_states.json.gz"
    else:
        file_name = "{0}_munic.json.gz".format(id)

    cached_q = cached_query(file_name)
    if cached_q:
        ret = make_response(cached_q)
    else:
        path = datavivadir+"/static/json/coords/{0}".format(file_name)
        gzip_file = open(path).read()
        cached_query(file_name, gzip_file)
        ret = make_response(gzip_file)

    ret.headers['Content-Encoding'] = 'gzip'
    ret.headers['Content-Length'] = str(len(ret.data))

    return ret

@mod.route('/networks/<type>/')
def networks(type="hs"):
    file_name = "network_{0}.json.gz".format(type)
    cached_q = cached_query(file_name)
    if cached_q:
        ret = make_response(cached_q)
    else:
        path = datavivadir+"/static/json/networks/{0}".format(file_name)
        gzip_file = open(path).read()
        cached_query(file_name, gzip_file)
        ret = make_response(gzip_file)

    ret.headers['Content-Encoding'] = 'gzip'
    ret.headers['Content-Length'] = str(len(ret.data))

    return ret

@mod.route('/')
def guide():
    return render_template("apps/index.html")

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
