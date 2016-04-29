# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, jsonify, request
from dataviva.apps.general.views import get_locale
from dataviva.apps.embed.models import Build

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


@mod.route('/')
def index():
    return render_template('build_graph/index.html')


@mod.route('/views/<dataset>/<bra>/<filter1>/<filter2>')
def views(dataset, bra, filter1, filter2):
    '''/views/secex/hs/wld'''

    builds = Build.query.filter_by(
        dataset=dataset,
        filter1='<%s>' % filter1,
        filter2='<%s>' % filter2).all()

    build_list = []
    for build in builds:
        if bra:
            build.set_bra(bra)

        if filter1 != 'all':
            request.args.get('filter1')

        if filter2 != 'all':
            request.args.get('filter2')

        build_list.append(build.json())

    return jsonify(builds=build_list)
