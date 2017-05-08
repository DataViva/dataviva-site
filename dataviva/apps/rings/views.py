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

    title_attrs = {circles: focus}

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
def networks(type="hs"):
    if GZIP_DATA:
        fileext = ".gz"
        filetype = "gzip"
    else:
        fileext = ""
        filetype = "json"
    file_name = ("network_{0}.json" + fileext).format(type)
    cached_q = cached_query(file_name)
    if cached_q:
        ret = make_response(cached_q)
    else:
        path = datavivadir + "/static/json/networks/{0}".format(file_name)
        gzip_file = open(path).read()
        cached_query(file_name, gzip_file)
        ret = make_response(gzip_file)

    ret.headers['Content-Encoding'] = filetype
    ret.headers['Content-Length'] = str(len(ret.data))

    return ret
