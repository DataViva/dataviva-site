# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request
from dataviva.apps.general.views import get_locale
from dataviva.translations.dictionary import dictionary
from dataviva.apps.title.views import get_title
from dataviva.utils.graphs_services import *
import urllib
import json


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


@mod.route('/<dataset>/<line>/<y_value>')
def index(dataset, line, y_value):
    filters = []
    title_attrs = {}

    services = {'product': product_service, 'id_ibge': location_service, 'wld':
                wld_service, 'occupation': occupation_service, 'industry': industry_service}

    for key, value in request.args.items():
        if key == 'type':
            title_attrs['type'] = value

        if key in ['depths', 'values', 'group']:
            continue
        if value and key in services:
            filters.append(services[key](value))
            title_attrs[services[key](value)[0]] = services[key](value)[1]
        else:
            if key == 'hedu_course' or key == 'university':
                title_attrs[key] = value
            filters.append((key, value))

    filters = urllib.urlencode(filters)

    title, subtitle = get_title(dataset, line, 'line', title_attrs)

    return render_template('line/index.html',
                           dataset=dataset,
                           line=line,
                           y_value=y_value,
                           filters=filters,
                           title=title or '',
                           subtitle=subtitle or '',
                           dictionary=json.dumps(dictionary()))
