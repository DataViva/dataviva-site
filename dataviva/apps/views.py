# -*- coding: utf-8 -*- 
import urllib2
import json
from datetime import datetime
from collections import defaultdict
from sqlalchemy import func
from flask import Blueprint, request, render_template, g, Response, make_response, send_file, jsonify, url_for

from dataviva import db
from dataviva.data.forms import DownloadForm
from dataviva.account.models import User, Starred
from dataviva.attrs.models import Bra, Isic, Hs, Cbo, Wld
from dataviva.apps.models import Build, UI, App

from dataviva.rais.views import rais_ybi

import json

mod = Blueprint('apps', __name__, url_prefix='/apps')

@mod.before_request
def before_request():
    g.page_type = mod.name
    
    g.color = "#3daf49"
    
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
    recs = recommend(app_name=app_name, dataset=dataset, bra_id=bra_id, \
                        filter1=filter1, filter2=filter2, output=output)
    
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
            "current_build": current_build.serialize(),
            "all_builds": [b.serialize() for b in all_builds],
            "recomendations": json.loads(recs.data)
        })
    
    return render_template("apps/embed.html",
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
            return jsonify({"success": 1})
    if starred:
        return jsonify({"success": -1})
    else:
        return jsonify({"success": 1})

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
            b.set_bra(bra_id)
            b.set_filter1(filter1)
            b.set_filter2(filter2)
            recommended['both_filters'].append(b.serialize())

    '''Add any builds that rely strictly on the second filter'''
    if build_filter2 != "all":
        builds = Build.query.filter_by(dataset=dataset, filter1="all", 
                    filter2=build_filter2).all()
        recommended['filter2'] = []
        for b in builds:
            b.set_bra(bra_id)
            b.set_filter2(filter2)
            recommended['filter2'].append(b.serialize())
    
    '''Add any builds that rely strictly on the first filter'''
    if build_filter1 != "all":
        builds = Build.query.filter_by(dataset=dataset, filter1=build_filter1, 
                    filter2="all").all()
        recommended['filter1'] = []
        for b in builds:
            b.set_bra(bra_id)
            b.set_filter1(filter1)
            recommended['filter1'].append(b.serialize())

    '''Lastly get the rest of the relevent builds'''
    builds = Build.query.filter_by(dataset=dataset, filter1="all", filter2="all").all()
    recommended['no_filters'] = []
    for b in builds:
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
@mod.route('/builder/<app_name>/<dataset>/<bra_id>/<filter1>/<filter2>/'
            '<output>/')
def builder(app_name=None, dataset=None, bra_id=None, filter1=None, 
                filter2=None, output=None):
    g.page_type = "builder"
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
