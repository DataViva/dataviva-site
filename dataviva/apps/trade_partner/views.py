# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale

mod = Blueprint('trade_partner', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/trade_partner',
                static_folder='static')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())

context = {
	#index
	'name' : unicode('China', 'utf8') ,
	'text_profile': unicode('Texto sobre a parceria economica entre Brasil e China.'),
	'background_image': unicode("'static/img/bg-profile-location.jpg'", 'utf8'),
	'year' : 2010,
	#header 
	'trade_balance' : 80, #balanca comercial 
	'trade_balance_unity' : 'Bilhoes', 
	'total_exported': 17.9, #'total exportado
	'total_exported_unity' : 'milhoes',
	'weight_exported_value' : 1.6, #pelo/valor exportado
	'weight_exported_value_unity' : 'milhares', 
	'total_imported': 17.9, #'total exportado
	'total_imported_unity' : 'milhoes',
	'weight_imported_value' : 1.6, #pelo/valor exportado
	'weight_imported_value_unity' : 'milharess', 
	#tab-geral e valores tab-comercio-internacional
	'county_for_exported_value': unicode('Sāo Paulo', 'utf8'), #'municipio_por_valor exportado' 
	'num_county_for_exported_value' : 1.62 , 
	'county_for_imported_value': unicode('Municipio X', 'utf8'), #'municipio_por_valor importado' 
	'num_county_for_imported_value' : 1.62 , 
	'product_for_exported_value': unicode('Minerio', 'utf8'), #'produto_por_valor exportado' 
	'num_product_for_exported_value' : 1.62 , 
	'product_for_imported_value': unicode('Produto X', 'utf8'), #'produto_por_valor importado' 
	'num_product_for_imported_value' : 1.62 , 
	'product_bigger_trade_balance' : unicode('Produto Y', 'utf8'),
	'value_product_bigger_trade_balance' : 10.88,
	'product_smaller_trade_balance' : unicode('Produto Z', 'utf8'),
	'value_product_smaller_trade_balance' : 1.88,
	#tab-comercio-internacional
	'text_comercio_internacional' : 'Texto sobre o comercio internacional. '
	
} 

@mod.route('/')
def index():
	return render_template('trade_partner/index.html', body_class='perfil-estado', context=context)


	