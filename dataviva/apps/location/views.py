# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.utils.cached_query import api_cache_key
from dataviva.apps.general.views import get_locale

mod = Blueprint('location', __name__, template_folder='templates',
                url_prefix='/<lang_code>/location')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/')
# @view_cache.cached(key_prefix=api_cache_key("location"))
def index():
    return render_template('location.html')
