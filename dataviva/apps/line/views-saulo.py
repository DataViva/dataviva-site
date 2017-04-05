# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request, abort
from dataviva.apps.general.views import get_locale
import urllib

mod = Blueprint('line', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/line',
                static_folder='static')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.before_request
def before_request():
    g.page_type = mod.name


def location_service(id_ibge):
    locations = {
        1: "region",    #todo
        2: "state",
        6: "mesoregion",
        6: "microregion",
        7: "municipality"
    }

    return (locations[len(id_ibge)], id_ibge)


def product_service(product):
    if len(product) == 2:
        return ('section', product[:2])
    elif len(product) == 4:
        return ('chapter', product[2:4])
    else:
        return ('product', product[2:])

def wld_service(wld):
    wlds = {
        2: "continent",
        3: "country"
    }

    return (wlds[len(wld)], wld)


@mod.route('/<dataset>/<line>')
def index(dataset, line):
    values = request.args.getlist('value')
    values = ','.join(values)

    type = request.args.get('type')
    product = request.args.get('product')
    id_ibge = request.args.get('id_ibge')
    wld = request.args.get('wld')
    options = request.args.get('options')
    subtitle = request.args.get('subtitle', '')

    filters = []

    if type:
        filters.append(('type', type))
        
    if wld:
        filters.append(wld_service(wld))

    if product:
        filters.append(product_service(product))

    if id_ibge:
        filters.append(location_service(id_ibge))

    filters = urllib.urlencode(filters)

    return render_template('line/index.html', dataset=dataset, line=line, filters=filters, values=values, options=options, subtitle=subtitle, type=type)
    