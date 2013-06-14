# -*- coding: utf-8 -*- 
import urllib2
import json
from datetime import datetime
from sqlalchemy import func
from flask import Blueprint, request, render_template, g, Response, make_response, send_file, jsonify

from visual import db
from visual.data.forms import DownloadForm
from visual.account.models import User, Starred
from visual.attrs.models import Bra

import json

mod = Blueprint('apps', __name__, url_prefix='/apps')
    
@mod.route('/embed/')
@mod.route('/embed/<app_name>/<data_type>/<bra_id>/<filter1>/<filter2>/<output>/')
def embed(app_name=None,data_type=None,bra_id=None,filter1=None,filter2=None,output=None):

    if app_name == None:
      app_name = "tree_map"
      data_type = "rais"
      bra_id = "mg"
      filter1 = "all"
      filter2 = "all"
      output = "cbo"
    
    # init variables
    global_vars = {x[0]:x[1] for x in request.args.items()}
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
                app_name = request.form['title']
            new_star = Starred(user=g.user, app_id=app_id, app_name=app_name)
            db.session.add(new_star)
            db.session.commit()
    if starred:
        return jsonify({"success": -1})
    else:
        return jsonify({"success": 1})

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

@mod.route('/')
@mod.route('/<category>/')
def guide(category = None):
    
    # try getting the user's ip address, since the live server is using a proxy
    # nginx, we need to use the "X-Forwarded-For" remote address otherwise
    # this will always be 127.0.0.1 ie localhost
    if not request.headers.getlist("X-Forwarded-For"):
        ip = request.remote_addr
    else:
        ip = request.headers.getlist("X-Forwarded-For")[0]
    
    # next try geolocating the user's ip
    geo_location = get_geo_location(ip) or None
    
    # if the city or region is not found in the db use Belo Horizonte as default
    if not geo_location:
        geo_location = Bra.query.get("mg030000")
    
    ajax = request.args.get("ajax")
    if ajax == "true":
        if category:
            return render_template("apps/{0}.html".format(category), geo_location = geo_location)
        else:
            return render_template("apps/home.html")
            
    return render_template("apps/index.html",
        category = category,
        geo_location = geo_location)

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