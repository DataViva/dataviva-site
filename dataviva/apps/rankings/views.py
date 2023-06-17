# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva import view_cache
from dataviva.utils.cached_query import api_cache_key

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
@view_cache.cached(key_prefix=api_cache_key("apps:ranking_index"))
def index():
    return render_template('rankings/location-international-trade.html', tab='location-international-trade')


@mod.route('/location/international-trade', methods=['GET'])
@view_cache.cached(key_prefix=api_cache_key("apps:ranking_location_international_trade"))
def location_international_trade():
    return render_template('rankings/location-international-trade.html', tab='location-international-trade')


@mod.route('/location/wages-and-employment', methods=['GET'])
@view_cache.cached(key_prefix=api_cache_key("apps:ranking_location_wages"))
def location_wages():
    return render_template('rankings/location-wages.html', tab='location-wages')


@mod.route('/occupation', methods=['GET'])
@view_cache.cached(key_prefix=api_cache_key("apps:ranking_occupation"))
def occupation():
    return render_template('rankings/occupation.html', tab='occupation')


@mod.route('/economic-activities', methods=['GET'])
@view_cache.cached(key_prefix=api_cache_key("apps:ranking_economic_activities"))
def economic_activities():
    return render_template('rankings/economic-activities.html', tab='economic_activities')


@mod.route('/product', methods=['GET'])
@view_cache.cached(key_prefix=api_cache_key("apps:ranking_product"))
def product():
    return render_template('rankings/product.html', tab='product')


@mod.route('/trade-partner', methods=['GET'])
@view_cache.cached(key_prefix=api_cache_key("apps:ranking_trade_partner"))
def trade_partner():
    return render_template('rankings/trade-partner.html', tab='trade_partner')


@mod.route('/university', methods=['GET'])
@view_cache.cached(key_prefix=api_cache_key("apps:ranking_university"))
def university():
    return render_template('rankings/university.html', tab='university')


@mod.route('/major', methods=['GET'])
@view_cache.cached(key_prefix=api_cache_key("apps:ranking_major"))
def major():
    return render_template('rankings/major.html', tab='major')


@mod.route('/basic-course', methods=['GET'])
@view_cache.cached(key_prefix=api_cache_key("apps:ranking_basic_course"))
def basic_course():
    return render_template('rankings/basic-course.html', tab='basic_course')
