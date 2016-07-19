# -*- coding: utf-8 -*-
import re
from flask import Blueprint, render_template, g, jsonify, request
from dataviva.apps.general.views import get_locale
from dataviva.apps.embed.models import Build
from sqlalchemy import not_
import hashlib


mod = Blueprint('build_graph', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/build_graph')


@mod.before_request
def before_request():
    g.page_type = mod.name


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


#http://localhost:5000/pt/build_graph/rais/4sp/g/2?view%3DxwFzAdaRQ6%26graph%3Dline
@mod.route('/', defaults={'dataset': None, 'filter0': None, 'filter1': None, 'filter2': None})
@mod.route('/<dataset>', defaults={'filter0': None, 'filter1': None, 'filter2': None})
@mod.route('/<dataset>/<filter0>', defaults={'filter1': None, 'filter2': None})
@mod.route('/<dataset>/<filter0>/<filter1>', defaults={'filter2': None})
@mod.route('/<dataset>/<filter0>/<filter1>/<filter2>')
def index(dataset, filter0, filter1, filter2):
    return render_template('build_graph/index.html')


def parse_filter(filter):
    if filter != 'all':
        return '<%s>' % filter
    else:
        return filter


@mod.route('/views/<dataset>/<bra>/<filter1>/<filter2>')
def views(dataset, bra, filter1, filter2):
    '''/views/secex/hs/wld'''

    build_query = Build.query.filter(
        Build.dataset == dataset,
        Build.filter1 == parse_filter(filter1),
        Build.filter2 == parse_filter(filter2))

    if bra != 'all':
        build_query.filter(not_(Build.bra.like('all')))

    views = {}
    for build in build_query.all():
        if bra:
            build.set_bra(bra)

        if filter1 != 'all':
            build.set_filter1(request.args.get('filter1'))

        if filter2 != 'all':
            build.set_filter2(request.args.get('filter2'))

        title = re.sub(r'\s\(.*\)', r'', build.title())

        id = hashlib.md5(build.slug2_en).digest().encode("base64")[0:10]

        if id not in views:
            views[id] = {
                'id': id,
                'name': title,
                'graphs': {},
            }

        views[id]['graphs'][build.app.type] = {
            'url': build.url(),
            'name': build.app.name()
        }

    return jsonify(views=views)
