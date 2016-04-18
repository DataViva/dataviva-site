# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, jsonify
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


@mod.route('/views/<dataset>/<filter1>/<filter2>')
def views(dataset, filter1, filter2):
    builds = Build.query.filter_by(
        dataset=dataset,
        filter1=filter1,
        filter2=filter2).all()

    return jsonify(builds)
