# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request, make_response
from dataviva.apps.general.views import get_locale
from dataviva.translations.dictionary import dictionary
from dataviva import datavivadir
from config import GZIP_DATA
from dataviva.utils.cached_query import cached_query
from dataviva.utils.graphs_services import location_service
from dataviva.apps.title.views import get_title
from dataviva.utils.graphs_services import *
import urllib
import json


mod = Blueprint('map', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/map',
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


@mod.route('/<dataset>/<value>/', defaults={'id_ibge': ''})
@mod.route('/<dataset>/<value>/<id_ibge>')
def index(dataset, value, id_ibge):
    filters = []
    title_attrs = {}
    services = {
        'product': product_service,
        'id_ibge': location_service,
        'wld': wld_service,
        'occupation': occupation_service,
        'industry': industry_service,
        'basic_course': sc_service,
    }

    for k, v in request.args.items():
        if k not in ['values', 'filters', 'count', 'year']:
            if v and k in services:
                filters.append(services[k](v))
                title_attrs[services[k](v)[0]] = services[k](v)[1]
            else:
                filters.append((k, v))
                title_attrs[k] = v

    if id_ibge:
        location = location_service(id_ibge)[0]
        filters.append((location, id_ibge))
        state = '' if location == 'region' else id_ibge[:2]
        title_attrs['state'] = state
    else:
        state = id_ibge
        location = 'municipality'

    filters = urllib.urlencode(filters)
    title, subtitle = get_title(dataset, value, 'map', title_attrs)
    return render_template('map/index.html',
                           dataset=dataset,
                           value=value,
                           state=state,
                           filters=filters,
                           title=title or '',
                           subtitle=subtitle or '',
                           dictionary=json.dumps(dictionary()))


@mod.route('/coords/', defaults={'id': 'all'})
@mod.route('/coords/<id>')
def coords(id):
    if GZIP_DATA:
        fileext = ".gz"
        filetype = "gzip"
    else:
        fileext = ""
        filetype = "json"

    if id == "all":
        file_name = "bra_all_states.json" + fileext
    else:
        file_name = ("coords-{0}.json" + fileext).format(id)

    cached_q = cached_query(file_name)

    if cached_q:
        ret = make_response(cached_q)
    else:
        path = datavivadir + "/static/json/map/{0}".format(file_name)
        gzip_file = open(path).read()
        cached_query(file_name, gzip_file)
        ret = make_response(gzip_file)

    ret.headers['Content-Encoding'] = filetype
    ret.headers['Content-Length'] = str(len(ret.data))

    return ret
