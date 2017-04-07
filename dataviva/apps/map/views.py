# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request, send_file, make_response
from dataviva.apps.general.views import get_locale
from dataviva.translations.dictionary import dictionary
from dataviva import datavivadir
from config import GZIP_DATA
from dataviva.utils.gzip_data import gzip_data
from dataviva.utils.cached_query import cached_query
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

@mod.route('/<dataset>/<value>/', defaults={'state': ''})
@mod.route('/<dataset>/<value>/<state>')
def index(dataset, value, state):
  filters = []
  for k, v in request.args.items():
    filters.append((k, v))

  filters = urllib.urlencode(filters)

  return render_template('map/index.html',
                           dataset=dataset,
                           value=value,
                           state=state,
                           filters=filters,
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
        file_name = "bra_all_states.json"+fileext
    else:
        file_name = ("coords-{0}.json"+fileext).format(id)

    cached_q = cached_query(file_name)

    if cached_q:
        ret = make_response(cached_q)

    else:
        path = datavivadir+"/static/json/map/{0}".format(file_name)
        gzip_file = open(path).read()
        cached_query(file_name, gzip_file)
        ret = make_response(gzip_file)

    ret.headers['Content-Encoding'] = filetype
    ret.headers['Content-Length'] = str(len(ret.data))

    return ret
