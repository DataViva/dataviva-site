# -*- coding: utf-8 -*- 
import urllib2
import json
from datetime import datetime
from sqlalchemy import func
from flask import Blueprint, request, render_template, g, Response, make_response, send_file, jsonify, redirect, url_for

from dataviva import db
from dataviva.data.forms import DownloadForm
from dataviva.account.models import User, Starred
from dataviva.attrs.models import Bra, Wld
from dataviva.rais.models import Isic, Cbo
from dataviva.secex.models import Hs

from dataviva.utils import crossdomain

import json

mod = Blueprint('data', __name__, url_prefix='/data')

@mod.before_request
def before_request():
    g.page_type = mod.name
    
    g.color = "#1abbee"
    
    g.sabrina = {}
    g.sabrina["outfit"] = "lab"
    g.sabrina["face"] = "smirk"
    g.sabrina["hat"] = "glasses"

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
def index():
    return render_template("data/index.html")

@mod.route('/query/')
@mod.route('/query/<data_type>/<year>/<bra_id>/<filter_1>/<filter_2>/')
@crossdomain()
def query(data_type="rais", year="all", bra_id=None, filter_1=None, filter_2=None):
    isic, cbo, hs, wld = [None] * 4
    g.page_type = "query"
    if not bra_id:
        '''try getting the user's ip address, since the live server is using
            proxy nginx, we need to use the "X-Forwarded-For" remote address 
            otherwise this will always be 127.0.0.1 ie localhost'''
        if not request.headers.getlist("X-Forwarded-For"):
            ip = request.remote_addr
        else:
            ip = request.headers.getlist("X-Forwarded-For")[0]
    
        # next try geolocating the user's ip
        bra = get_geo_location(ip) or None
    
        '''if the city or region is not found in the db use Belo Horizonte as 
            default'''
        if not bra:
            bra = [Bra.query.get("mg030000")]
        else:
            bra = [bra]
    else:
        bra = [Bra.query.get_or_404(b) for b in bra_id.split("+")]
    
    if filter_1 and filter_1 != "all":
        if data_type == "rais":
            if filter_1 == "show":
                isic = []
            else:
                isic = [Isic.query.get_or_404(f1) for f1 in filter_1.split("+")]
        else:
            if filter_1 == "show":
                hs = []
            else:
                hs = [Hs.query.get_or_404(f1) for f1 in filter_1.split("+")]
    
    if filter_2 and filter_2 != "all":
        if data_type == "rais":
            if filter_2 == "show":
                cbo = []
            else:
                cbo = [Cbo.query.get_or_404(f2) for f2 in filter_2.split("+")]
        else:
            if filter_2 == "show":
                wld = []
            else:
                wld = [Wld.query.get_or_404(f2) for f2 in filter_2.split("+")]
    
    return render_template("data/query.html", 
        data_type = data_type,
        bra=bra, isic=isic, cbo=cbo, hs=hs, wld=wld)

@mod.route('/classifications/')
@mod.route('/classifications/<attr>/')
@mod.route('/classifications/<attr>/<depth>/')
@crossdomain()
def classifications(attr = None, depth = None, page = 1):
    
    if not attr:
        return render_template("data/select.html")
    
    g.page_type = "classifications"
    per_page = 50
    offset = request.args.get("offset", 0)
    
    attr_table = globals()[attr.capitalize()]
    
    if attr == "bra":
        depths = ["2","4","6","7","8"]
        if g.locale == "pt":
            title = u"Localidades Brasileiras"
        else:
            title = u"Brazilian Locations"
    elif attr == "wld":
        depths = ["2","5"]
        if g.locale == "pt":
            title = u"Países"
        else:
            title = u"Countries"
    elif attr == "isic":
        depths = ["1","3","5"]
        if g.locale == "pt":
            title = u"Atividades Econômicas por Classificação ISIC"
        else:
            title = u"Industries by ISIC Classification"
    elif attr == "cbo":
        depths = ["1","4"]
        if g.locale == "pt":
            title = u"Ocupações por Classificação CBO"
        else:
            title = u"Occupations by CBO Classification"
    elif attr == "hs":
        depths = ["2","4","6"]
        if g.locale == "pt":
            title = u"Produtos por Classificação HS"
        else:
            title = u"Products by HS Classification"
            
    if depth == None:
        depth = depths[0]
    
    attrs = attr_table.query.filter(func.char_length(attr_table.id) == depth).limit(per_page).offset(offset)
    
    ret = make_response(render_template("data/classifications.html",
        title = title,
        page_attr = attr,
        depth = depth,
        depths = depths,
        attrs = attrs))
            
    ret.headers.add('Last-Modified', datetime.now())
    ret.headers.add('Expires', '-1')
    ret.headers.add('Cache-Control', 'must-revalidate, private')
            
    return ret

@mod.route('/classificationslist/<attr>/')
@mod.route('/classificationslist/<attr>/<depth>/')
@crossdomain()
def classificationslist(attr = None, depth = None, page = 1):
    
    g.page_type = "classifications"
    per_page = 50
    offset = request.args.get("offset", 0)
    
    attr_table = globals()[attr.capitalize()]
            
    if depth == None:
    
        if attr == "bra":
            depths = ["2","4","6","7","8"]
        elif attr == "wld":
            depths = ["2","5"]
        elif attr == "isic":
            depths = ["1","3","5"]
        elif attr == "cbo":
            depths = ["1","4"]
        elif attr == "hs":
            depths = ["2","4","6"]
            
        depth = depths[0]
    
    attrs = attr_table.query.filter(func.char_length(attr_table.id) == depth).limit(per_page).offset(offset)
    
    attrs_json = [dict(a.serialize().items() + [("attr_type",attr)]) for a in attrs]
    ret = jsonify({"data": attrs_json})
            
    ret.headers.add('Last-Modified', datetime.now())
    ret.headers.add('Expires', '-1')
    ret.headers.add('Cache-Control', 'must-revalidate, private')
            
    return ret

@mod.route('/download/', methods=['GET', 'POST'])
@crossdomain()
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