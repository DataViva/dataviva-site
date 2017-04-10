# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request
from dataviva.apps.general.views import get_locale
from dataviva.translations.dictionary import dictionary
from dataviva.utils.graphs_services import filter_service
from dataviva.api.attrs.models import Cbo, Cnae, Hs, Wld, Bra
from models import GraphTitle
import requests

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
    if key in ['equipment_type', 'equipment_code']:
        return 'equipment'
    if key in ['bed_type', 'bed_type_per_specialty']:
        return 'bed_type'
    return key


def location_service(id_ibge):
    if len(id_ibge) == 1:
        return {'1': '1', '2': '2', '3': '4', '4': '5', '5': '3'}[id_ibge]
    if len(id_ibge) == 5:
        return id_ibge[0:2] + '0' + id_ibge[2:]
    if len(id_ibge) == 4:
        return id_ibge[0:2] + '00' + id_ibge[2:]
    return id_ibge


def value_service(filter, value):
    if filter == 'location':
        value = location_service(value)

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
            return getattr(result, 'name_' + g.locale)
    return None

def inflect(title, object, preposition, name):
    inflections = {'in': ['no', 'na', 'em'], 'from': ['do', 'da', 'de'], 'of': [
        'do', 'da', 'de'], 'to': ['para o', 'para a', 'para']}

    if object.article_pt and object.gender_pt == 'm':
        inflection = inflections[preposition][0]
    elif object.article_pt and object.gender_pt == 'f':
        inflection = inflections[preposition][1]
    else:
        inflection = inflections[preposition][2]

    return title.replace('<' + name + '_' + preposition + '>', inflection)


def get_title(dataset, shapes, graph, api_filters):
    query = {}
    values = {}

    for key, value in api_filters.iteritems():
        if key == 'type':
            query['type'] = value
            values['type'] = value
        else:
            if dataset.startswith('cnes_'):
                url = 'http://api.staging.dataviva.info/metadata/' + key + '/' + str(value)
            filter = filter_service(key)
            if filter:
                query[filter] = 1
                if dataset.startswith('cnes_'):
                    response = requests.get(url).json()
                    values[filter] = response['name_' + g.locale]
                else:
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
        title = getattr(result, 'title_' + g.locale)
        for key, value in values.iteritems():
            title = title.replace('<' + key + '>', value)

        title = title.replace('<location>', 'Brazil' if g.locale == 'en' else 'Brasil')

        possible_location_filters = [location for location in ['municipality', 'microregion', 'mesoregion', 'health_region', 'state', 'region'] if location in api_filters]
        if len(possible_location_filters) > 0:
            api_filters['location'] = api_filters[possible_location_filters[0]]

        if 'location' in api_filters:
            id = ('id' if len(api_filters['location']) == 1 else 'id_ibge', location_service(api_filters['location']))
            location = Bra.query.filter_by(**{id[0]: id[1]}).first()
            for preposition in ['in', 'from', 'of']:
                if '<location_' + preposition + '>' in title:
                    title = inflect(title, location, preposition, 'location')

        title = title.replace('<location_in>', 'no').replace('<location_from', 'do').replace('<location_of>', 'do')

        if 'partner' in api_filters:
            if api_filters['partner'].isdigit():
                partner = Wld.query.filter_by(id_mdic=api_filters['partner']).first()
            else:
                partner = Wld.query.get(api_filters['partner'])

            if '<partner_to>' in title:
                title = inflect(title, partner, 'to', 'partner')

        return title, getattr(result, 'subtitle_' + g.locale)

    return None, None
