# -*- coding: utf-8 -*-
from flask import Blueprint, g
from dataviva.apps.general.views import get_locale
from dataviva.utils.graphs_services import filter_service
from models import GraphTitle
import requests
from config import API_BASE_URL

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


def location_service(id_ibge):
    if len(id_ibge) == 1:
        return {'1': '1', '2': '2', '3': '4', '4': '5', '5': '3'}[id_ibge]
    if len(id_ibge) == 5:
        return id_ibge[0:2] + '0' + id_ibge[2:]
    if len(id_ibge) == 4:
        return id_ibge[0:2] + '00' + id_ibge[2:]
    return id_ibge


def inflect(title, object, preposition, name):
    inflections = {'in': ['no', 'na', 'em'], 'from': ['do', 'da', 'de'], 'of': [
        'do', 'da', 'de'], 'to': ['para o', 'para a', 'para']}
    if object['gender'] == 'm':
        inflection = inflections[preposition][0]
    elif object['gender'] == 'f':
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
            if key == 'sc_course' and len(value) == 4:
                value = '0'+value
            url = API_BASE_URL + 'metadata/' + key + '/' + str(value)
            filter = filter_service(key)
            query[filter] = 1
            response = requests.get(url).json()
            values[filter] = response['name_' + g.locale]

    for filter in ['product', 'partner', 'occupation', 'industry', 'establishment', 'hedu_course', 'university', 'sc_course', 'sc_course_field']:
        if filter not in query:
            query[filter] = 0

    if 'type' not in query:
        query['type'] = None

    query['shapes'] = filter_service(shapes)
    query['dataset'] = dataset
    query['graph'] = graph
    query['location'] = 1 if query['establishment'] == 0 else 0

    if query['university'] == 1:
        query['location'] = 0

    result = GraphTitle.query.filter_by(**query).first()

    if result:
        title = getattr(result, 'title_' + g.locale)

        for key, value in values.iteritems():
            title = title.replace('<' + key + '>', value)

        title = title.replace(
            '<location>', 'Brazil' if g.locale == 'en' else 'Brasil')

        # Deals with brazilian locations prepositions
        locations = [l for l in api_filters if l in [
            'region', 'state', 'mesoregion', 'microregion', 'municipality']]
        if len(locations) > 0:
            url = API_BASE_URL + 'metadata/inflection/' + \
                str(api_filters[locations[0]])
            response = requests.get(url).json()
            for preposition in ['in', 'from', 'of']:
                if '<location_' + preposition + '>' in title:
                    title = inflect(title, response, preposition, 'location')
        else:
            title = title.replace('<location_in>', 'no').replace(
                '<location_from>', 'do').replace('<location_of>', 'do')

        # Deals with countries and continents prepositions
        partners = [p for p in api_filters if p in ['country', 'continent']]
        if len(partners) > 0:
            url = API_BASE_URL + 'metadata/inflection/' + \
                str(api_filters[partners[0]])
            response = requests.get(url).json()
            if '<partner_to>' in title:
                title = inflect(title, response, 'to', 'partner')

        return title, getattr(result, 'subtitle_' + g.locale)

    return None, None
