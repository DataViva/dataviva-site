# encoding: utf-8

from flask import Blueprint, render_template, g, request, abort
from dataviva.apps.general.views import get_locale
import requests
from config import API_BASE_URL

mod = Blueprint('health', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/health',
                static_folder='static')


@mod.before_request
def before_request():
    g.page_type = 'category'


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/<cnes_id>', defaults={'tab': 'general'})
@mod.route('/<cnes_id>/<tab>')
def index(cnes_id, tab):
    response = requests.get(
        API_BASE_URL + 'cnes/id/name_pt/?id=' + cnes_id + '&limit=1').json()

    establishment = {
        'id': response['data'][0][0],
        'name': response['data'][0][1].title()
    }
    # establishment = {
    #     'name' : '<name>'
    # }

    graph = {}
    url = request.args.get('url', '')
    menu = request.args.get('menu', '')
    if menu and url:
        graph['menu'] = menu
        graph['url'] = '/' + menu.split('-')[-1] + '/' + url

    return render_template('health/index.html',
                           tab=tab,
                           establishment=establishment,
                           graph=graph)


@mod.route('/<cnes_id>/graphs/<tab>', methods=['POST'])
def graphs(cnes_id, tab):
    response = requests.get(
        API_BASE_URL + 'cnes/id/name_pt/?id=' + cnes_id + '&limit=1').json()
    establishment = {'id': response['data'][0]
                     [0], 'name': response['data'][0][1]}

    graph = {}
    url = request.args.get('url', '')
    menu = request.args.get('menu', '')
    if menu and url:
        graph['menu'] = menu
        graph['url'] = menu.split('-')[-1] + '/' + url

    return render_template('health/graphs-' + tab + '.html', establishment=establishment, graph=graph)
