# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request, abort
from dataviva.apps.general.views import get_locale
from dataviva.translations.dictionary import dictionary
from dataviva.apps.title.views import get_title
import urllib
import json

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
        4: "mesoregion",
        5: "microregion",
        7: "municipality"
    }

    return (locations[len(id_ibge)], id_ibge)


def product_service(product):
    if len(product) == 2:
        return ('product_section', product[:2])
    elif len(product) == 4:
        return ('product_chapter', product[2:4])
    else:
        return ('product', product[2:])

def wld_service(wld):
    if wld.isdigit():
        wld = '%03d' % int(wld)

    wlds = {
        2: "continent",
        3: "country"
    }

    return (wlds[len(wld)], wld)

def occupation_service(occupation):
    occupations = {
        1: "occupation_group",
        4: "occupation_family"
    }

    return (occupations[len(occupation)], occupation)

def industry_service(industry):
    if len(industry) == 1:
        return ('industry_section', industry)
    elif len(industry) == 3:
        return ('industry_division', industry[1:])
    else:
        return ('industry_class', industry[1:])


@mod.route('/<dataset>/<x>/<y>')
def index(dataset, x, y):
    product = request.args.get('product')
    id_ibge = request.args.get('id_ibge')
    type = request.args.get('type')
    wld = request.args.get('wld')
    establishment = request.args.get('establishment')
    occupation = request.args.get('occupation')
    industry = request.args.get('industry')
    counts = request.args.getlist('count')

    title_attrs = {}

    options = request.args.get('options')
    subtitle = request.args.get('subtitle', '')

    filters = []

    for count in counts:
        filters.append(('count', count))

    if type:
        filters.append(('type', type))
        title_attrs['type'] = type

    if request.args.get('filters'):
        filters.append(('filters', request.args.get('filters')))

    if wld:
        filters.append(wld_service(wld))
        title_attrs[wld_service(wld)[0]] = wld_service(wld)[1]

    if occupation:
        filters.append(occupation_service(occupation))
        title_attrs[occupation_service(wld)[0]] = occupation_service(wld)[1]

    if industry:
        filters.append(industry_service(industry))
        title_attrs[industry_service(wld)[0]] = industry_service(wld)[1]

    if product:
        filters.append(product_service(product))
        title_attrs[product_service(wld)[0]] = product_service(wld)[1]

    if id_ibge:
        filters.append(location_service(id_ibge))
        title_attrs[location_service(id_ibge)[0]] = location_service(id_ibge)[1]

    if establishment:
        filters.append(('establishment', establishment))

    filters = urllib.urlencode(filters)
    graph_title, graph_subtitle = get_title(dataset, y.split(',')[0], 'bar', title_attrs)

    return render_template('bar/index.html', dataset=dataset, x=x, y=y, filters=filters, options=options,
                           subtitle=subtitle, graph_title=graph_title or '', graph_subtitle=graph_subtitle or '',
                           dictionary=json.dumps(dictionary()))
    