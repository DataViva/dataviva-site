# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request, abort
from dataviva.apps.general.views import get_locale
import urllib

mod = Blueprint('radar', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/radar',
                static_folder='static')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


def location_service(id_ibge):
    locations = {
        1: "region",    #todo
        2: "state",
        4: "mesoregion",
        5: "microregion",
        7: "municipality"
    }

    return (locations[len(id_ibge)], id_ibge)

@mod.route('/<dataset>/<polygon>/<label>/<value>')
def index(dataset, polygon, label, value):

    id_ibge = request.args.get('id_ibge')

    filters = []

    if id_ibge:
        filters.append(location_service(id_ibge))

    filters = urllib.urlencode(filters)

    return render_template('radar/index.html', dataset=dataset, polygon=polygon, label=label, value=value, filters=filters)
