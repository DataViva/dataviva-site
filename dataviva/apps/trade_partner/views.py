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
	#tab-geral
	'county_for_jobs': unicode('Sāo Paulo', 'utf8'), #'municipio_por_empregos' 
	'num_jobs_county' : 1.62 , #num_empregos_principal_municipio
	'jobs_county_unity' : 'milhares', #'unidade_empregos_principal_municipio'
	'activity_for_job' : 'atividade x', #atividade_por_empregos
	'num_activity_for_job': 1.0, #valor_atividade_por_empregos
	'activity_for_job_unit': unicode('bilhāo','utf8'), #unidade_atividade_por_empregos
	'county_bigger_average_monsthly_income': unicode('Sāo Paulo', 'utf8'),
	'bigger_average_monsthly_income': 12.3, #MUNICIPO Valor_maior_renda_media_mensal
	'bigger_average_monsthly_income_unity': unicode('bilhões','utf-8'),
	'activity_higher_income': 'Desenvolvimento Sob Encomenda ',  #atividade_maior_renda
	'value_activity_higher_income' : 990 ,
	#tab-comercio-internacional
	'text_comercio_internacional' : 'Texto sobre o comercio internacional. '
	
} 

@mod.route('/')
def index():
	return render_template('trade_partner/index.html', body_class='perfil-estado', context=context)


	