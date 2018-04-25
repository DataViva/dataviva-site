# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request
from dataviva.apps.general.views import get_locale
from dataviva.translations.dictionary import dictionary
from dataviva.apps.embed.models import Build
from dataviva.apps.title.views import get_title
from dataviva.utils.graphs_services import *
import urllib
import json

mod = Blueprint('tree_map', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/tree_map',
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


@mod.route('/<dataset>/<squares>/<size>')
def index(dataset, squares, size):
    filters = []
    title_attrs = {}

    services = {'product': product_service, 'id_ibge': location_service, 'wld':
                wld_service, 'occupation': occupation_service, 'industry': industry_service, 'basic_course': sc_service}
    for key, value in request.args.items():
        if key == 'type':
            title_attrs['type'] = value

        if key in ['depths', 'sizes', 'group', 'depth', 'color', 'filter', 'filters', 'hierarchy']:
          continue
        if value and key in services:
            filters.append(services[key](value))
            title_attrs[services[key](value)[0]] = services[key](value)[1]
        else:
            if key in ['establishment', 'hedu_course', 'university', 'sc_course_field']:
              title_attrs[key] = value
            filters.append((key, value))

    filters = urllib.urlencode(filters)

    title, subtitle = get_title(dataset, squares, 'tree_map', title_attrs)

    return render_template('tree_map/index.html',
                           dataset=dataset,
                           squares=squares,
                           size=size,
                           filters=filters,
                           title=title or '',
                           subtitle=subtitle or '',
                           dictionary=json.dumps(dictionary()))
