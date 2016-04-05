# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale

mod = Blueprint('rankings', __name__, template_folder='templates',
                url_prefix='/<lang_code>/rankings')


@mod.before_request
def before_request():
    g.page_type = mod.name


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/', methods=['GET'])
def index():
    pass


@mod.route('/location/wages-and-employment', methods=['GET'])
def location_wages():
    return render_template('rankings/location-wages.html')


@mod.route('/location/international-trade', methods=['GET'])
def location_international_trade():
    return render_template('rankings/location-international-trade.html')


@mod.route('/economic-activities', methods=['GET'])
def economic_activities():
    return render_template('rankings/economic-activities.html')


@mod.route('/occupation', methods=['GET'])
def occupation():
    return render_template('rankings/occupation.html')


@mod.route('/trade-partner', methods=['GET'])
def trade_partner():
    return render_template('rankings/trade-partner.html')


@mod.route('/university', methods=['GET'])
def university():
    return render_template('rankings/university.html')


@mod.route('/product', methods=['GET'])
def product():
    return render_template('rankings/product.html')
