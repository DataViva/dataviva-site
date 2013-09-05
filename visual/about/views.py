from sqlalchemy import func
from flask import Blueprint, request, render_template, g

from visual.attrs.models import Bra, Wld
from visual.rais.models import Isic, Cbo
from visual.secex.models import Hs

mod = Blueprint('about', __name__, url_prefix='/about')

@mod.before_request
def before_request():
    g.page_type = mod.name
    
    g.color = "#d67ab0"

@mod.route('/')
def about():
    return render_template("about/visual.html", page = "dataminas")
    
@mod.route('/data/')
def data():
    return render_template("about/data/index.html", page = "data")

@mod.route('/visual/')
def visual():
    return render_template("about/visual.html", page = "dataminas")
    
@mod.route('/sabrina/')    
def sabrina():
    return render_template("about/sabrina.html", page = "sabrina")
    
@mod.route('/minas/')
def minas():
    return render_template("about/minas.html", page = "minas")

@mod.route('/glossary/')
def glossary():
    return render_template("about/glossary.html", page = "glossary")
    
@mod.route('/growthventures/')
def growthventures():
    return render_template("about/growthventures.html", page = "growthventures")
  
@mod.route('/apps/')
@mod.route('/apps/<app>/')
def apps(app=None):
    ajax = request.args.get("ajax")
    if ajax == "true" and app != None:
        return render_template("about/apps/{0}.html".format(app), page = "apps")
    else:
        return render_template("about/appsdocs.html", app=app, page = "apps")
    
@mod.route('/api/')      
def api():
    return render_template("about/api.html", page = "api")
    
@mod.route('/credits/')  
def credits():
    return render_template("about/credits.html", page = "credits")