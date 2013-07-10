# -*- coding: utf-8 -*- 
import urllib2
import json
from datetime import datetime
from collections import defaultdict
from sqlalchemy import func
from flask import Blueprint, request, render_template, g, Response, make_response, send_file, jsonify, url_for

from visual import db
from visual.data.forms import DownloadForm
from visual.account.models import User, Starred
from visual.attrs.models import Bra, Isic, Hs, Cbo, Wld
from visual.apps.models import Build, UI, App

from visual.rais.views import rais_ybi

import json

mod = Blueprint('apps', __name__, url_prefix='/apps')

@mod.before_request
def before_request():
    g.page_type = mod.name
    
    g.sabrina = {}
    g.sabrina["outfit"] = "lab"
    g.sabrina["face"] = "smirk"
    g.sabrina["hat"] = "glasses"

@mod.route('/embed/', defaults={"app_name": "tree_map", "data_type": "rais", "bra_id": "mg", "filter1": "all", "filter2": "all", "output": "cbo"})
@mod.route('/embed/<app_name>/<data_type>/<bra_id>/<filter1>/<filter2>/<output>/')
def embed(app_name=None,data_type=None,bra_id=None,filter1=None,filter2=None,output=None):
    
    # init variables
    global_vars = {x[0]:x[1] for x in request.args.items()}
    if "controls" not in global_vars:
        global_vars["controls"] = "true"
    starred = 0
    app_id = "/".join([app_name, data_type, bra_id, filter1, filter2, output])
    
    # if user is logged in see if they have starred this app
    if g.user and g.user.is_authenticated():
        is_starred = Starred.query.filter_by(user=g.user, app_id=app_id).first()
        starred = 1 if is_starred else -1
    
    return render_template("apps/embed.html",
        starred = starred,
        form = DownloadForm(),
        app_name = app_name,
        data_type = data_type,
        bra_id = bra_id,
        filter1 = filter1,
        filter2 = filter2,
        output = output,
        global_vars = json.dumps(global_vars))

@mod.route('/embed2/', defaults={"app_name": "tree_map", "data_type": "rais", "bra_id": "mg", "filter1": "all", "filter2": "all", "output": "cbo"})
@mod.route('/embed2/<app_name>/<dataset>/<bra_id>/<filter1>/<filter2>/'
            '<output>/')
def embed2(app_name=None, dataset=None, bra_id=None, filter1=None, filter2=None,
            output=None):
    
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
        return jsonify({
            "current_build": current_build.serialize()
        })
        
    return render_template("apps/embed2.html",
        all_builds = all_builds,
        starred = starred,
        form = DownloadForm(),
        current_build = current_build,
        global_vars = json.dumps(global_vars))

@mod.route('/star/<app_name>/<data_type>/<bra_id>/<filter1>/<filter2>/<output>/', methods=['GET', 'POST'])
def app_star(app_name, data_type, bra_id, filter1, filter2, output):
    app_id = "/".join([app_name, data_type, bra_id, filter1, filter2, output])
    if g.user is None or not g.user.is_authenticated():
        return jsonify({"error": "You need to be logged in for this action."})
    starred = Starred.query.filter_by(user=g.user, app_id=app_id).first()
    if request.method == 'POST':
        if starred:
            db.session.delete(starred)
            db.session.commit()
        else:
            app_name = None
            if 'title' in request.form:
                app_name = request.form['title'].encode('utf-8')
                # print app_name
                # app_name = "Uberlândia"
            timestamp = datetime.utcnow()
            new_star = Starred(user=g.user, app_id=app_id, app_name=app_name, timestamp=timestamp)
            db.session.add(new_star)
            db.session.commit()
            return jsonify({"success": app_name})
    if starred:
        return jsonify({"success": -1})
    else:
        return jsonify({"success": 1})

@mod.route('/recommend/', methods=['GET', 'POST'])
@mod.route('/recommend/<app_name>/<data_type>/<bra_id>/<filter1>/<filter2>/<output>/', methods=['GET', 'POST'])
def recommend(app_name=None, data_type=None, bra_id="mg", filter1=None, filter2=None, output=None):
    return jsonify(get_urls(app=app_name, data_type=data_type, bra=bra_id, f1=filter1, f2=filter2, output=output))

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
def builder():
    return render_template("apps/builder.html")

@mod.route('/download/', methods=['GET', 'POST'])
def download():
    import tempfile, subprocess
    
    form = DownloadForm()

    data = form.data.data
    format = form.output_format.data
    title = form.title.data

    temp = tempfile.NamedTemporaryFile()
    temp.write(data.encode("utf-8"))
    temp.seek(0)

    if format == "png":
        mimetype='image/png'
    elif format == "pdf":
        mimetype='application/pdf'
    elif format == "svg":
        mimetype='application/octet-stream'
    elif format == "csv":
        mimetype="text/csv;charset=UTF-8"

    if format == "png" or format == "pdf":
        zoom = "1"
        background = "#ffffff"
        p = subprocess.Popen(["rsvg-convert", "-z", zoom, "-f", format, "--background-color={0}".format(background), temp.name], stdout=subprocess.PIPE)
        out, err = p.communicate()  
        response_data = out
    else:
        response_data = data.encode("utf-8")
    
    content_disposition = "attachment;filename=%s.%s" % (title, format)
    content_disposition = content_disposition.replace(",", "_")

    return Response(response_data, 
                        mimetype=mimetype, 
                        headers={"Content-Disposition": content_disposition})

@mod.route('/')
def guide():
    return render_template("apps/index.html")
