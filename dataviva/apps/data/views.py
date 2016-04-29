# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale


mod = Blueprint('data', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/data')


@mod.before_request
def before_request():
    g.page_type = mod.name
    g.color = "#1abbee"


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/')
def index():
    return render_template('data/index.html')
