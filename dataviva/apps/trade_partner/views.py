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
	'average_monthly_income' : 8, #'renda_media_mensal' 
	'average_monthly_income_unity' : 'Milhares', #'unidade_renda_media_mensal'
	'salary_mass': 17.9, #'massa_salarial'
	'salary_mass_unity' : 'mil',
	'total_employment' : 1.6, #total de empregos
	'total_employment_unity' : 'milhares', 
	'total_establishments' : 6.8, #'total_estabelecimentos'
	'total_establishments_unity' : 'milhares', #'unidade_total_estabelecimentos' 
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
	'value_activity_higher_income' : 990 
	#tab-comercio-internacional
	
} 

@mod.route('/')
def index():
	return render_template('trade_partner/index.html', body_class='perfil-estado', context=context)


	