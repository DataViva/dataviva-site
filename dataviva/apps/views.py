# -*- coding: utf-8 -*-
from StringIO import StringIO
from datetime import datetime
from collections import defaultdict
from sqlalchemy import func
from random import randint
from flask import Blueprint, request, render_template, g, Response, make_response, send_file, jsonify, url_for, redirect, jsonify
from flask.ext.babel import gettext

from dataviva import db, datavivadir, __year_range__, view_cache
from dataviva.data.forms import DownloadForm
from dataviva.account.models import User, Starred
from dataviva.attrs.models import Bra, Cnae, Hs, Cbo, Wld
from dataviva.apps.models import Build, UI, App, Crosswalk_oc, Crosswalk_pi
from dataviva.general.models import Short


from dataviva.rais.views import rais_api
from dataviva.utils.gzip_data import gzip_data
from dataviva.utils.translates import translate_columns
from dataviva.utils.cached_query import cached_query, make_cache_key

import json, urllib2, urllib
from config import FACEBOOK_OAUTH_ID, basedir,GZIP_DATA
import os
import urlparse
import random
import zipfile
import sys
import gzip
from dataviva.utils.decorators import cache_api

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
            filler1 = "<cnae>"
        elif dataset == "secex":
            filler1 = "<hs>"
        elif dataset == "hedu":
            filler1 = "<university>"

    filler2 = filter2
    if filler2 != "all":
        if dataset == "rais":
            filler2 = "<cbo>"
        elif dataset == "secex":
            filler2 = "<wld>"
        elif dataset == "hedu":
            filler2 = "<course_hedu>"
        elif dataset == "sc":
            filler2 = "<course_sc>"

    return filler1, filler2

@mod.route("/embed/")
@mod.route("/embed/<app_name>/<dataset>/<bra_id>/<filter1>/<filter2>/<output>/")
# @cache_api("apps:embed", timeout=604800)
def embed(app_name="tree_map", dataset="rais", bra_id="4mg",
          filter1="all", filter2="all", output="cbo"):

    lang = request.args.get('lang', None) or g.locale

    if (g.user is None or not g.user.is_authenticated()) and request.is_xhr:
        cache_id = request.path + lang
        cached_q = cached_query(cache_id)
        if cached_q:
            ret = make_response(cached_q)
            ret.headers['Content-Encoding'] = 'gzip'
            ret.headers['Content-Length'] = str(len(ret.data))
            return ret

    build_filter1, build_filter2 = filler(dataset, filter1, filter2)

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
    if output == "cnae" or output == "hs" or output == "university":
        filler1 = "filler"
    elif output == "cbo" or output == "wld" or output == "course_hedu" or "course_sc":
        filler2 = "filler"
    elif output == "bra":
        filler_bra = "filler"

    recs = recommend(app_name=app_name, dataset=dataset, bra_id=filler_bra, \
                        filter1=filler1, filter2=filler2, output=output)

    '''Every possible build, required by the embed page for building the build
    dropdown.
    '''
    all_builds = Build.query.all()
    all_builds.sort(key=lambda x: x.app_id)
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
    # view_data = rais_api(bra_id='sp', cnae_id='a0112').data
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

        year_range = json.dumps(__year_range__)

        ret = make_response(render_template("apps/embed.html",
            all_builds = all_builds,
            starred = starred,
            form = DownloadForm(),
            current_build = current_build,
            global_vars = json.dumps(global_vars),
            facebook_id = FACEBOOK_OAUTH_ID,
            year_range = year_range))

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
def recommend(app_name=None, dataset=None, bra_id="4mg", filter1=None, filter2=None, output=None):

    recommended = {}

    build_filter1, build_filter2 = filler(dataset, filter1, filter2)

    recommended["crosswalk"] = crosswalk_recs(dataset, build_filter1, filter1, build_filter2, filter2, bra_id)

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
                # Municipalities are not allowed to have other municipality within it - Github #141
                if b.output == "bra" and len(bra_id) > 2:
                    continue
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
@mod.route('/builder/geo_map/', defaults={"app_name": "geo_map", "dataset": "rais", "bra_id": "4mgplr02",
            "filter1": "all", "filter2": "all", "output": "bra", "params": "?value_var=wage"})
@mod.route('/builder/network/', defaults={"app_name": "network", "dataset": "secex", "bra_id": "4mg",
            "filter1": "all", "filter2": "all", "output": "hs", "params": ""})
@mod.route('/builder/rings/', defaults={"app_name": "rings", "dataset": "rais", "bra_id": "4mg",
            "filter1": "all", "filter2": "2211", "output": "cbo", "params": ""})
@mod.route('/builder/scatter/', defaults={"app_name": "scatter", "dataset": "secex", "bra_id": "4mg",
            "filter1": "all", "filter2": "all", "output": "hs", "params": "?rca_scope=wld_rca"})
@mod.route('/builder/compare/', defaults={"app_name": "compare", "dataset": "rais", "bra_id": "4mg_4rj",
            "filter1": "all", "filter2": "all", "output": "cbo", "params": "?depth=cbo_4&axes=wage_avg"})
@mod.route('/builder/occugrid/', defaults={"app_name": "occugrid", "dataset": "rais", "bra_id": "4mg030000",
            "filter1": "c14126", "filter2": "all", "output": "cbo", "params": ""})
@mod.route('/builder/line/', defaults={"app_name": "line", "dataset": "secex", "bra_id": "4mg",
            "filter1": "all", "filter2": "all", "output": "all", "params": ""})
@mod.route('/builder/box/', defaults={"app_name": "box", "dataset": "rais", "bra_id": "4mg030000",
            "filter1": "c14126", "filter2": "all", "output": "cbo", "params": ""})
@mod.route('/builder/<app_name>/<dataset>/<bra_id>/<filter1>/<filter2>/<output>/')
#@view_cache.cached(timeout=604800, key_prefix=make_cache_key)
def builder(app_name=None, dataset=None, bra_id=None, filter1=None,
                filter2=None, output=None, params=None):
    path = request.path.split("/")
    if bra_id == 'bra':
        bra_id = 'all'
        params = request.query_string
        return redirect('/{0}/{1}/{2}/{3}/{4}/{5}/{6}?{7}'.format('apps/builder',app_name,dataset,bra_id,filter1,filter2,output,params))
    if len(path) == 5:
        return redirect('{0}{1}/{2}/{3}/{4}/{5}/{6}'.format("/".join(path),dataset,bra_id,filter1,filter2,output,params))
    g.page_type = "builder"
    return render_template("apps/builder.html")

@mod.route('/download/', methods=['GET', 'POST'])
def download():
    import tempfile, subprocess, random

    form = DownloadForm()
    data = form.data.data
    format = form.output_format.data
    title = form.title.data
    downloadToken = form.downloadToken.data
    filenameDownload = title+"-"+downloadToken



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

    def getRows(data):
        # ?? this totally depends on what's in your data
        return []

    if format == "png" or format == "pdf":
        temp = tempfile.NamedTemporaryFile()
        temp.write(data.encode("utf-16"))
        temp.seek(0)
        zoom = "1"
        background = "#ffffff"
        p = subprocess.Popen(["rsvg-convert", "-z", zoom, "-f", format, "--background-color={0}".format(background), temp.name], stdout=subprocess.PIPE)
        out, err = p.communicate()
        response_data = out
    elif format == "url2csv":
        urrll = data
        format = "csv"

        lang = request.args.get('lang', None) or g.locale
        txdata = None
        txheaders = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            'Accept-Language': lang,
            'encoding': 'UTF-8',
            'Content-type': 'text/html',
            'Keep-Alive': '300',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
        }
        reqq = urllib2.Request(data, txdata, txheaders)
        reqq.add_header('Accept-encoding', 'gzip')
        req = urllib2.urlopen(reqq)

        if req.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(req.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        else:
            data = req.read()

        data = json.loads(str(data))

        cvs = ""
        i = 0
        lineArray = []
        linesArray = []
        headerArray = []
        checkHeader = []


        for item in data['data']:
            for cabecalho in item:
                if cabecalho not in checkHeader:
                   checkHeader.append(cabecalho)
                   translation = translate_columns(cabecalho, lang)
                   headerArray.append(unicode(translation,'utf-8'))

        for item in data['data']:
            print item
            lineArray = []
            for header in checkHeader:
                if header in item:
                    if (type(item[header]) is unicode):
                        lineArray.append(item[header])
                    else:
                        lineArray.append(str(item[header]))
                else:
                    lineArray.append("")

            linesArray.append('\t'.join(lineArray))
            i = 1
        cvs = '\t'.join(headerArray) + '\n' + '\n'.join(linesArray)
        response_data = cvs.encode("utf-16", 'ignore')

    else:
        response_data = data.encode("utf-16")
        #print response_data


    content_disposition = "attachment;filename=%s.%s" % (title, format)
    content_disposition = content_disposition.replace(",", "_")

    download_file = make_response(Response(response_data,
                       mimetype=mimetype,
                        headers={"Content-Disposition": content_disposition}))

    with open(os.path.join(basedir, "dataviva/static/downloads/"+title+"."+format),"wb") as fo:
        fo.write(response_data)

    zf = zipfile.ZipFile(os.path.join(basedir, "dataviva/static/downloads/"+filenameDownload+".zip"), mode='w')
    try:
        zf.write(os.path.join(basedir, "dataviva/static/downloads/"+title+"."+format), title+"."+format)
    finally:
        zf.close()

    os.remove(os.path.join(basedir, "dataviva/static/downloads/"+title+"."+format))

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

@mod.route('/')
#@view_cache.cached(timeout=604800, key_prefix=make_cache_key)
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


def crosswalk_recs(dataset, build_filter1, raw_filter1, build_filter2, raw_filter2, bra_id):
    crosswalk = {"filter1" : [], "filter2": []}

    data1 = {"<cnae>": Crosswalk_pi.cnae_id, "<hs>": Crosswalk_pi.hs_id}
    data2 = {"<cbo>": Crosswalk_oc.cbo_id, "<course_hedu>": Crosswalk_oc.course_hedu_id}

    if build_filter1 in data1 and raw_filter1 != "all":

        col = data1[build_filter1]
        results = Crosswalk_pi.query.filter(col == raw_filter1).all()
        ids = [row.get_id(dataset) for row in results]
        if ids:
            # Build filter1 must either be <cnae> or <hs>
            swap_map = { "secex" : { "<hs>" : ("rais", "<cnae>") },
                         "rais" : { "<cnae>" : ("secex", "<hs>") }}
            dataset2, target_filter = swap_map[dataset][build_filter1]
            raw_target_filter = "_".join(ids)

            builds = Build.query.filter_by(dataset=dataset2, filter1=target_filter, filter2="all").all()

            for b in builds:
                if bra_id != "filler":
                    b.set_bra(bra_id)
                b.set_filter1(raw_target_filter)

            crosswalk["filter1"] = [b.serialize() for b in builds]
    elif build_filter2 in data2 and raw_filter2 != "all":
        col = data2[build_filter2]
        results = Crosswalk_oc.query.filter(col == raw_filter2).all()
        ids = [row.get_id(dataset) for row in results]
        if ids:
            # Build filter2 must either be <cbo>, <course_hedu>
            swap_map = { "hedu" : { "<course_hedu>" : ("rais", "<cbo>")},
                         "rais" : { "<cbo>" : ("hedu", "<course_hedu>") }}
            dataset2, target_filter = swap_map[dataset][build_filter2]
            raw_target_filter = "_".join(ids)
            builds = Build.query.filter_by(dataset=dataset2, filter1="all", filter2=target_filter).all()

            for b in builds:
                if bra_id != "filler":
                    b.set_bra(bra_id)
                b.set_filter2(raw_target_filter)

            crosswalk["filter2"] = [b.serialize() for b in builds]

    return crosswalk
