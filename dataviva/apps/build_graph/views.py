# -*- coding: utf-8 -*-
import re
from flask import Blueprint, render_template, g, jsonify, request
from dataviva.apps.general.views import get_locale
from dataviva.apps.embed.models import Build, App
from dataviva.translations.dictionary import dictionary
from sqlalchemy import not_
import hashlib
import json


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


def parse_filter_id(filter_id):
    if filter_id != 'all':
        return '<%>'
    else:
        return filter_id


@mod.route('/')
@mod.route('/<dataset>/<filter0>/<filter1>/<filter2>')
def index(dataset=None, filter0=None, filter1=None, filter2=None):

    view = request.args.get('view')
    graph = request.args.get('graph')
    compare = request.args.get('compare')

    build_query = Build.query.join(App).filter(
        Build.dataset == dataset,
        Build.filter1.like(parse_filter_id(filter1)),
        Build.filter2.like(parse_filter_id(filter2)),
        Build.slug2_en == view,
        App.type == graph)

    build = build_query.first_or_404()

    build.set_bra(filter0)

    if filter1 != 'all':
        build.set_filter1(filter1)

    if filter2 != 'all':
        build.set_filter2(filter2)

    title = re.sub(r'\s\(.*\)', r'', build.title())

    metadata = {
        'view': title,
        'graph': dictionary()[graph],
        'dataset': dictionary()[dataset],
    }

    return render_template(
        'build_graph/index.html', dataset=dataset, filter0=filter0, filter1=filter1, filter2=filter2,
        graph=graph, view=view, compare=compare, metadata=metadata)


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

        id = build.slug2_en

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
