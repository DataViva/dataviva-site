from sqlalchemy import func
from flask import Blueprint, request, render_template, g

from visual.attrs.models import Bra, Wld
from visual.rais.models import Isic, Cbo
from visual.secex.models import Hs
from visual.utils import Pagination

mod = Blueprint('about', __name__, url_prefix='/about')

@mod.route('/')
def about():
    return render_template("about/visual.html", page = "dataminas")
    
@mod.route('/data/')
def data():
    return render_template("about/data/index.html", page = "data")

@mod.route('/data/<attr>/', defaults={"category": "all", "page":1})
@mod.route('/data/<attr>/<category>/', defaults={"page":1})
@mod.route('/data/<attr>/<category>/<int:page>/')
def data_attr(attr, category, page):
    per_page = request.args.get("per_page", "25")
    
    if attr == "bra":
        attr_table = Bra
        category_lookup = {"state":2, "mesoregion":4, "microregion":4, "municipality":8}
        title = "Brazilian Geography"
    elif attr == "wld":
        attr_table = Wld
        category_lookup = {"continent":2, "country":5}
        title = "Countries"
    elif attr == "isic":
        attr_table = Isic
        category_lookup = {"top category":1, "isic":5}
        title = "Industries by ISIC Classification"
    elif attr == "cbo":
        attr_table = Cbo
        category_lookup = {"top category":1, "cbo":4}
        title = "Occupations by CBO Classification"
    elif attr == "hs":
        attr_table = Hs
        category_lookup = {"top category":2, "hs":6}
        title = "Products by HS Classification"
    
    attrs = attr_table.query
    
    if category == "all":
        possible_nestings = category_lookup.values()
        attrs = attrs.filter(func.char_length(attr_table.id).in_(possible_nestings))
    else:
        attrs = attrs.filter(func.char_length(attr_table.id) == category_lookup[category])
    
    total = attrs.count()
    if per_page.isdigit():
        pagination = Pagination(page, int(per_page), total)
        attrs = attrs.paginate(page, int(per_page), False).items
    else:
        pagination = Pagination(page, per_page, total)
        attrs = attrs.all()
    
    return render_template("about/data/attr.html",
        title = title,
        page = "data",
        page_attr = attr,
        category = category,
        category_lookup = category_lookup,
        attrs = attrs,
        pagination = pagination)

@mod.route('/visual/')
def visual():
    return render_template("about/visual.html", page = "dataminas")
    
@mod.route('/sabrina/')    
def sabrina():
    return render_template("about/sabrina.html", page = "sabrina")
    
@mod.route('/minas/')
def minas():
    return render_template("about/minas.html", page = "minas")
    
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