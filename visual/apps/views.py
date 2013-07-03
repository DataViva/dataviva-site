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
from visual.apps.models import Build, UI

import json

mod = Blueprint('apps', __name__, url_prefix='/apps')

@mod.before_request
def before_request():
    g.page_type = mod.name

def get_title(url):
    
    app, data_type, bra, f1, f2, output = url.split("/")
    
    bra = Bra.query.get_or_404(bra)
    filters = []
    if f1 != "all":
        f1 = Isic.query.get_or_404(f1) if data_type == "rais" else Hs.query.get_or_404(f1)
        filters.append(f1)
    if f2 != "all":
        f2 = Cbo.query.get_or_404(f2) if data_type == "rais" else Wld.query.get_or_404(f2)
        filters.append(f2)
    
    if output == "hs": output_name = "Product"; output_name_pl = "Products"
    if output == "isic": output_name = "Industry"; output_name_pl = "Industries"
    if output == "cbo": output_name = "Occupation"; output_name_pl = "Occupations"
    if output == "wld": output_name = "Country"; output_name_pl = "Countries"
    if output == "bra": output_name = "Location"; output_name_pl = "Locations"
    
    if data_type == "rais": items = "Local Industries"
    if data_type == "secex": items = "Product Exports"
    
    if g.locale == "en":
        if app == "network":
            return output_name + " Space for " + bra.name_en
        elif app == "rings":
            return "Connections for " + filters[0].name_en + " in " + bra.name_en
        elif app == "bubbles":
            return "Available and required employment for " + filters[0].name_en + " in " + bra.name_en;
        else:
            # var title = visual.format.text(out+"_plural")
            title = output_name_pl
            if output == "isic" or output == "cbo" or output == "bra":
                title += " in "
            if output == "hs" or output == "wld":
                title += " of "
            title += bra.name_en
            if output == "bra" and len(filters) == 1:
                title += " with " + items
            
            for i, f in enumerate(filters):
                if i != 0:
                    if f == "isic":
                        article = "employed in" if output == "cbo" else "that have"
                        title += " " + article + " the " + isic.name_en + " industry"
                elif f == "cbo":
                    article = "that" if i == 1 else "and"
                    title += " " + article + " employ " + filter[0].name_en
                elif f == "hs":
                  trade = "import" if out == "wld" else "export"
                  title += " that " + trade + " " + hs.name_en
                elif f == "wld":
                  title += " to " + wld.name_en
                elif f == "bra2":
                  title += " and " + bra2.name_en
            
            
            return title
    elif g.locale == "pt":
        pass

def get_urls(app=None, data_type=None, bra="mg", f1=None, f2=None, output=None):
    
    app = None if app == "all" else app
    data_type = None if data_type == "all" else data_type
    # Determine which data set we're looking at
    rais = True if data_type == "rais" or data_type == None else None
    secex = True if data_type == "secex" or data_type == None else None
    # The dictionary we'll return indexed by app_type and data_type
    apps = defaultdict(lambda: defaultdict(list))
    defaults = {"cbo":"1210", "hs":"178703", "isic":"c1410", "wld":"aschn", "bra":"mg"}
    
    potential_apps = {
        "network": {
            "rais": ["all/all/isic", "all/all/cbo"],
            "secex": ["all/all/hs"]
        },
        "rings": {
            "rais": ["{isic}/all/isic", "all/{cbo}/cbo"],
            "secex": ["{hs}/all/hs"]
        },
        "bubbles": {
            "rais": ["{isic}/all/isic"],
        },
        "pie_scatter": {
            "rais": ["all/all/isic", "all/{cbo}/isic"],
            "secex": ["all/all/hs", "all/{wld}/hs"]
        },
        "stacked": {
            "rais": ["all/all/isic", "all/{cbo}/isic", 
                        "all/all/cbo", "{isic}/all/cbo",
                        "all/all/bra", "{isic}/all/bra", "all/{cbo}/bra",
                        "{isic}/{cbo}/bra"],
            "secex": ["all/all/hs", "all/{wld}/hs",
                        "all/all/wld", "{hs}/all/wld",
                        "all/all/bra", "{hs}/all/bra", "all/{wld}/bra",
                        "{hs}/{wld}/bra"]
        },
        "tree_map": {
            "rais": ["all/all/isic", "all/{cbo}/isic", 
                        "all/all/cbo", "{isic}/all/cbo",
                        "all/all/bra", "{isic}/all/bra", "all/{cbo}/bra",
                        "{isic}/{cbo}/bra"],
            "secex": ["all/all/hs", "all/{wld}/hs",
                        "all/all/wld", "{hs}/all/wld",
                        "all/all/bra", "{hs}/all/bra", "all/{wld}/bra",
                        "{hs}/{wld}/bra"]
        },
        "geo_map": {
            "rais": ["all/all/bra", "{isic}/all/bra", "all/{cbo}/bra",
                        "{isic}/{cbo}/bra"],
            "secex": ["all/all/bra", "{hs}/all/bra", "all/{wld}/bra",
                        "{hs}/{wld}/bra"]
        },
    }
    
    for app_type in potential_apps.keys():
        
        # check if user specified app_type
        if not app or app == app_type:
            
            # go through each data_type
            for dt in potential_apps[app_type].keys():
                
                # if the user DID specify a data_type and it's not this one, skip
                if not data_type or dt == data_type:
                    
                    # go through each potential app
                    for pa in potential_apps[app_type][dt]:
                        this_output = pa.split("/")[-1]
                        isic = f1 if data_type == "rais" and f1 else defaults["isic"]
                        cbo = f2 if data_type == "rais" and f2 else defaults["cbo"]
                        hs = f1 if data_type == "secex" and f1 else defaults["hs"]
                        wld = f2 if data_type == "secex" and f2 else defaults["wld"]
                        pa = pa.format(isic=isic, cbo=cbo, hs=hs, wld=wld)
                        
                        if not output or this_output == output:
                            url = "/".join([app_type, dt, bra]) + "/" + pa
                            # raise Exception(get_title(url))
                            apps[app_type][dt].append({"title": get_title(url), "url": url})
    
    return apps

# @mod.route('/embed/', defaults={"app_name": "tree_map", "data_type": "rais", "bra_id": "mg", "filter1": "all", "filter2": "all", "output": "cbo"})
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

# @mod.route('/embed2/', defaults={"app_name": "tree_map", "data_type": "rais", "bra_id": "mg", "filter1": "all", "filter2": "all", "output": "cbo"})
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
    current_build = Build.query.filter_by(type=app_name, dataset=dataset, filter1=build_filter1, filter2=build_filter2, output=output).first()
    
    '''Every possible build, required by the embed page for building the build
    dropdown.
    '''
    all_builds = Build.query.all()
    
    '''Get URL query parameters from reqest.args object to return to the view.
    '''
    global_vars = {x[0]:x[1] for x in request.args.items()}
    global_vars["controls"] = "true"

    '''If user is logged in see if they have starred this app.'''
    starred = 0
    if g.user and g.user.is_authenticated():
        is_starred = Starred.query.filter_by(user=g.user, app_id=app_id).first()
        starred = 1 if is_starred else -1

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
