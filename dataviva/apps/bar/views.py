# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request, abort
from dataviva.apps.general.views import get_locale
import urllib

mod = Blueprint('bar', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/bar',
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

def occupation_service(occupation):
    occupations = {
        1: "occupation_group",
        4: "occupation"
    }

    return (occupations[len(occupation)], occupation)

def industry_service(industry):
    if len(industry) == 1:
        return ('cnae_section', industry)
    elif len(industry) == 3:
        return ('cnae_division', industry[1:])
    else:
        return ('cnae', industry[1:])


@mod.route('/<dataset>/<x>/<y>')
def index(dataset, x, y):
    product = request.args.get('product')
    id_ibge = request.args.get('id_ibge')
    type = request.args.get('type')
    wld = request.args.get('wld')
    occupation = request.args.get('occupation')
    industry = request.args.get('industry')
    counts = request.args.getlist('count')

    options = request.args.get('options')

    filters = []

    for count in counts:
        filters.append(('count', count))

    if type:
        filters.append(('type', type))

    if wld:
        filters.append(wld_service(wld))

    if occupation:
        filters.append(occupation_service(occupation))

    if industry:
        filters.append(industry_service(industry))

    if product:
        filters.append(product_service(product))

    if id_ibge:
        filters.append(location_service(id_ibge))

    filters = urllib.urlencode(filters)

    return render_template('bar/index.html', dataset=dataset, x=x, y=y, filters=filters, options=options)