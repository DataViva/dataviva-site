# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale

mod = Blueprint('occupation', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/occupation',
                static_folder='static')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())

dicionario = {
	#index
	'occupation' : 'Engenheiros em Computacao', 
	'text_profile':'Engenharia de Computacao e o ramo da engenharia que lida com a realizacao de projeto e construcaoo de computadores e de sistemas que integram hardware e software, viabilizando a producao de novas maquinas e de equipamentos computacionais para serem utilizados em diversos setores.',
	'family' : True,
	#header 
	'average_monthly_income' : 8, #'renda_media_mensal' 
	'average_monthly_income_unity' : 'Milhares', #'unidade_renda_media_mensal'
	'salary_mass': 17.9, #'massa_salarial'
	'salary_mass_unity' : 'mil',
	'total_employment' : 1.6, #total de empregos
	'total_employment_unity' : 'milhares', 
	'total_establishments' : 6.8, #'total_estabelecimentos'
	'total_establishments_unity' : 'milhares', #'unidade_total_estabelecimentos' 
	#tabela responsiva 
	'county_for_jobs': 'Sao Paulo', #'municipio_por_empregos' 
	'num_jobs_county' : 1.62 , #num_empregos_principal_municipio
	'jobs_county_unity' : 'milhares', #'unidade_empregos_principal_municipio'
	'activity_for_job' : 'atividade x', #atividade_por_empregos
	'num_activity_for_job': 1.0, #valor_atividade_por_empregos
	'activity_for_job_unit': 'bilhao', #unidade_atividade_por_empregos
	'bigger_average_monsthly_income': 12.3, #Bigger Average monthly income valor_maior_renda_media_mensal
	'bigger_average_monsthly_income_unity': 'bilhoes',
	'activity_higher_income': 'Desenvolvimento Sob Encomenda ',  #atividade_maior_renda
	'value_activity_higher_income' : 990 #
} 

@mod.route('/')
def index():
	return render_template('occupation/index.html', body_class='perfil-estado', dic = dicionario)


	