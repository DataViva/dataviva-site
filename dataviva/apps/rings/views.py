# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request, make_response
from dataviva.apps.general.views import get_locale
from dataviva.translations.dictionary import dictionary
from dataviva.utils.cached_query import cached_query
from dataviva.apps.title.views import get_title
from dataviva.utils.graphs_services import *
from dataviva import datavivadir
from config import GZIP_DATA
import urllib
import json


mod = Blueprint('rings', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/rings',
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


@mod.route('/<dataset>/<circles>/<focus>')
def index(dataset, circles, focus):
    filters = []
    title_attrs = {}

    if dataset == 'rais' and circles == 'occupation_family':
        title_attrs[circles] = focus
    elif dataset == 'rais' and circles == 'industry_class':
        title_attrs[circles] = focus[1:6]
    elif dataset == 'secex' and circles == 'product':
        title_attrs[circles] = focus[2:6]

    services = {'id_ibge': location_service, 'product': product_service,
                'occupation_family': occupation_service, 'industry_class': industry_service}

    if circles in services:
        focus = services[circles](focus)[1]

    for key, value in request.args.items():
        if key == 'id_ibge':
            filters.append(location_service(value))
            title_attrs[services[key](value)[0]] = services[key](value)[1]
        else:
            filters.append((key, value))

    filters = urllib.urlencode(filters)
    title, subtitle = get_title(dataset, circles, 'rings', title_attrs)

    return render_template('rings/index.html',
                           dataset=dataset,
                           circles=circles,
                           focus=focus,
                           filters=filters,
                           title=title or '',
                           subtitle=subtitle or '',
                           dictionary=json.dumps(dictionary()))


@mod.route('/networks/<type>/')
def networks(type="new_hs"):
    if GZIP_DATA:
        file_extension = ".gz"
        file_type = "gzip"
    else:
        file_extension = ""
        file_type = "json"
    file_name = ("network_{0}.json" + file_extension).format(type)
    cached_connection = cached_query(file_name)

    if cached_connection:
        connections_result = make_response(cached_connection)
    else:
        path = datavivadir + "/static/json/networks/{0}".format(file_name)
        gzip_file = open(path).read()
        cached_query(file_name, gzip_file)
        connections_result = make_response(gzip_file)

    connections_result.headers['Content-Encoding'] = file_type
    connections_result.headers['Content-Length'] = str(len(connections_result.data))

    return connections_result
