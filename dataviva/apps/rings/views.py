# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request, make_response
from dataviva.apps.general.views import get_locale
from dataviva.translations.dictionary import dictionary
from dataviva.utils.cached_query import cached_query
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


def location_service(id_ibge):
    locations = {
        1: "region",
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


@mod.route('/<dataset>/<circles>/<focus>')
def index(dataset, circles, focus):
    filters = []

    for key, value in request.args.items():
            if key == 'product':
                filters.append(product_service(value))
            elif key == 'id_ibge':
                filters.append(location_service(value))
            elif key == 'wld':
                filters.append(wld_service(value))
            elif key == 'occupation':
                filters.append(occupation_service(value))
            elif key == 'industry':
                filters.append(industry_service(value))
            else:
                filters.append((key, value))

    filters = urllib.urlencode(filters)

    if circles == 'product':
        focus = product_service(focus)[1]

    if circles == 'industry_class':
        focus = industry_service(focus)[1]

    return render_template('rings/index.html',
                           dataset=dataset,
                           circles=circles,
                           focus=focus,
                           filters=filters,
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
