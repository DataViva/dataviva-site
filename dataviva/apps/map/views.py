# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request, send_file
from dataviva.apps.general.views import get_locale
from dataviva.translations.dictionary import dictionary
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


@mod.route('/<dataset>/<value>')
def index(dataset, value):
  filters = []
  for k, v in request.args.items():
    filters.append((k, v))

  filters = urllib.urlencode(filters)

  return render_template('map/index.html',
                           dataset=dataset,
                           value=value,
                           filters=filters,
                           dictionary=json.dumps(dictionary()))

@mod.route('/coords')
def coords():
  return send_file('static/json/coords.json')
