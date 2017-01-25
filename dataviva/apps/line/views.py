# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request, json
from dataviva.apps.general.views import get_locale
from dataviva.translations.dictionary import dictionary
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
        1: "region",
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


@mod.route('/<dataset>/<line>/<y_value>')
def index(dataset, line, y_value):
    filters = []

    for key, value in request.args.items():
        if key not in ['depths', 'values', 'group'] and value:
            filters.append((key, value[2:] if key == 'product' else value))

    group = request.args.get('group') or ''

    params = {}
    for param in ['depths', 'values']:
        value = request.args.get(param)
        params[param] = value if value and len(value.split()) > 1 else ''

    if 'wld' in filters:
        filters.append(wld_service(filters['wld']))

    if 'product' in filters:
        filters.append(product_service(filters['product']))

    if 'id_ibge' in filters:
        filters.append(location_service(filters['id_ibge']))

    filters = urllib.urlencode(filters)

    return render_template('line/index.html',
                           dataset=dataset,
                           line=line,
                           y_value=y_value,
                           group=group,
                           depths=params['depths'],
                           values=params['values'],
                           filters=filters,
                           dictionary=json.dumps(dictionary()))
