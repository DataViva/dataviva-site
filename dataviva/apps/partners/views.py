# -*- coding: utf8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.apps.calls.models import Call


mod = Blueprint('partners', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/partners')


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
    return render_template('partners/index.html')


@mod.route('/be-a-partner')
def be_a_partner():
    calls = Call.query.filter_by(active=True).all()
    return render_template('partners/be-a-partner.html', calls=calls)
