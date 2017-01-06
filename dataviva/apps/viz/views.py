# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request, abort
from dataviva.apps.general.views import get_locale
import urllib

mod = Blueprint('viz', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/viz',
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


def location_service(location):
    locations = {
        1: "region",    #todo
        2: "state",
        6: "mesoregion",
        6: "microregion",
        7: "municipality"
    }

    return (locations[len(location)], location)

def product_service(product):
    if len(product) == 2:
        return ('section', product[:2])
    elif len(product) == 4:
        return ('chapter', product[2:4])
    else:
        return ('product', product[2:])


@mod.route('/product/trade-partner/export/port/<string:product>/<string:location>')
@mod.route('/product/trade-partner/export/port/<string:product>/', defaults={'location': None})
def viz_export_port(product, location):
    script = 'product_trade-partner_export_port_line.js'

    filters = [
        ('type', 'export'),
        product_service(product)
    ]

    if location:
        filters.append(location_service(location))

    url = "http://localhost:5001/secex/year/port?{filters}".format(
        filters=urllib.urlencode(filters)
    )
    
    params = {
        'title': request.args.get('title')
    }

    return render_template('viz/viz.html', url=url, script=script, params=params)
