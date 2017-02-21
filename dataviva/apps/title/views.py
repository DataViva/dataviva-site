# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request
from dataviva.apps.general.views import get_locale
from dataviva.translations.dictionary import dictionary
from dataviva.api.attrs.models import Cbo, Cnae, Hs, Wld, Bra
from models import GraphTitle

mod = Blueprint('title', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/title',
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


def filter_service(key):
    if key in ['region', 'state', 'mesoregion', 'microregion', 'municipality']:
        return 'location'
    if key in  ['continent', 'country']:
        return 'partner'
    if key in ['industry_division', 'industry_section', 'industry_class']:
        return 'industry'
    if key in ['occupation_group', 'occupation_family']:
        return 'occupation'
    return key


def value_service(filter, value):
    if filter == 'location' and len(value) == 1:
        value = {'1': '1', '2': '2', '3': '4', '4': '5', '5': '3'}[value]
    elif filter == 'location' and len(value) == 5:
        value = value[0:2] + '0' + value[2:]
    elif filter == 'location' and len(value) == 4:
        value = value[0:2] + '00' + value[2:]

    models = {
        'product': (Hs, 'id'),
        'partner': (Wld, 'id_mdic' if value.isdigit() else 'id'),
        'location': (Bra, 'id' if len(value) == 1 else 'id_ibge'),
        'occupation': (Cbo, 'id'),
        'industry': (Cnae, 'id')
    }

    if filter in models:
        model = models[filter][0]
        result = model.query.filter_by(**{models[filter][1]: value}).first()
        if result:
            return result.name_en
    return None


def get_title(dataset, shapes, graph, api_filters):
    query = {}
    values = {}

    for key, value in api_filters.iteritems():
        if key == 'type':
            query['type'] = value
            values['type'] = value
        else:
            filter = filter_service(key)
            if filter:
                query[filter] = 1
                values[filter] = value_service(filter, value)
            else:
                query[filter] = 0

    if 'type' not in query:
        query['type'] = None

    query['shapes'] = filter_service(shapes)
    query['dataset'] = dataset
    query['graph'] = graph

    result = GraphTitle.query.filter_by(**query).first()
    if result:       
        title = result.title_en
        for key, value in values.iteritems():
            title = title.replace('<' + key + '>', value)
        title = title.replace('<location>', 'Brazil')
        return title, result.subtitle_en
    
    return None, None
