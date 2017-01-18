# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request, abort
from dataviva.apps.general.views import get_locale
from dataviva.translations.dictionary import dictionary 
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


def location_service(id_ibge):
    locations = {
        1: "region",    #todo
        2: "state",
        6: "mesoregion",
        6: "microregion",
        7: "municipality"
    }

    return (locations[len(id_ibge)], id_ibge)


@mod.route('/<dataset>/<squares>/<group>')
def index(dataset='secex', squares='product', group='state'):
    expected_filters = ['type', 'state', 'year']

    filters = [(filter, request.args.get(filter)) for filter in expected_filters if request.args.get(filter)]
    filters = urllib.urlencode(filters)

    return render_template('tree_map/index.html', dataset=dataset, squares=squares, group=group, filters=filters, dictionary=json.dumps(dictionary()))
