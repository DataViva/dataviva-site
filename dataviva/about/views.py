from sqlalchemy import func
from flask import Blueprint, request, render_template, g

from dataviva.attrs.models import Bra, Wld
from dataviva.rais.models import Isic, Cbo
from dataviva.secex.models import Hs

mod = Blueprint('about', __name__, url_prefix='/about')

@mod.before_request
def before_request():
    g.page_type = mod.name
    
    g.color = "#d67ab0"

@mod.route('/')
@mod.route('/dataviva/')
def about():
    return render_template("about/dataviva.html", page = "dataviva")
    
@mod.route('/data/<data>/')
def data(data):
    return render_template("about/data.html", data=data, page = "data")

@mod.route('/glossary/<term>/')
def glossary(term):
    return render_template("about/glossary.html", term=term, page = "glossary")
  
@mod.route('/apps/<app>/')
def apps(app):
    return render_template("about/apps.html", app=app, page = "apps")