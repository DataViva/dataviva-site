# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale

from dataviva.api.attrs.models import Cbo, Bra
from dataviva.api.rais.models import Yo, Ybo, Yio, Ybio

from dataviva import db
from sqlalchemy.sql.expression import func, desc, asc

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


@mod.route('/')
def index():

	occupation_id = '2122'
	location_id = '4mg'
	has_location = True

	#se tiver sido selecionada uma localidade especific
	if has_location:

		#encontrando o ano mais recente 
		ybo_max_year= db.session.query(func.max(Ybo.year)).filter(
			Ybo.cbo_id == occupation_id, 
			Ybo.bra_id == location_id)\
			.one()
			
		occupation_basic = {}
		for year in ybo_max_year:
			occupation_basic['year'] = year
	

		ybo_header_query = Ybo.query.join(Cbo).filter(
			Ybo.cbo_id == occupation_id,
			Ybo.bra_id == location_id,
			Ybo.year == occupation_basic['year'])\
			.values(Cbo.name_pt,
					Ybo.wage_avg,
					Ybo.wage,
					Ybo.num_jobs,
					Ybo.num_est)

		header = {}
		for name_pt, wage_avg, wage, num_jobs, num_est in ybo_header_query:
			header['name'] = name_pt
			header['average_monthly_income'] = float(wage_avg)
			header['salary_mass'] = float(wage)
			header['total_employment'] = int(num_jobs)
			header['total_establishments'] = int(num_est)

		ybo_county_num_jobs_query = Ybo.query.join(Bra).filter(
				Ybo.cbo_id == occupation_id,
				Ybo.bra_id.like(location_id+'%'),
				Ybo.year == occupation_basic['year'],
				Ybo.bra_id_len == 9)\
			.order_by(asc(Ybo.num_jobs))\
			.values(Bra.name_pt,
					Ybo.num_jobs)

		body = {}
		for name_pt, num_jobs in ybo_county_num_jobs_query:
			body['county_for_jobs'] = name_pt
			body['num_jobs_county'] = num_jobs
	
		
	
	context = {
		'name' : header['name'],
		'text_profile': unicode('Engenharia de Computacao e o ramo da engenharia que lida com a realizacao de projeto e construcaoo de computadores e de sistemas que integram hardware e software, viabilizando a producao de novas maquinas e de equipamentos computacionais para serem utilizados em diversos setores.'),
		'year' : occupation_basic['year'],
		'average_monthly_income' : header['average_monthly_income'],
		'salary_mass': header['salary_mass'],
		'total_employment' : header['total_employment'],
		'total_establishments' : header['total_establishments'],
		'county_for_jobs' : body['county_for_jobs'],
		'num_jobs_county' : body['num_jobs_county'],
	}

	#acessar o contex do diogo com context.id.oqeuquero

	
	return render_template('occupation/index.html', body_class='perfil-estado', context=context)


'''
context = {
	#index
	'name' : unicode('Engenheiros em Computaçāo', 'utf8') ,
	'text_profile': unicode('Engenharia de Computacao e o ramo da engenharia que lida com a realizacao de projeto e construcaoo de computadores e de sistemas que integram hardware e software, viabilizando a producao de novas maquinas e de equipamentos computacionais para serem utilizados em diversos setores.'),
	'background_image': unicode("'static/img/bg-profile-location.jpg'", 'utf8'),
	'family' : True,
	'year' : yo_max_year_query ,
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
	'bigger_average_monsthly_income': 12.3, #Valor_maior_renda_media_mensal
	'bigger_average_monsthly_income_unity': unicode('bilhões','utf8'),
	'activity_higher_income': 'Desenvolvimento Sob Encomenda ',  #atividade_maior_renda
	'value_activity_higher_income' : 990 ,
	#tab-salario-emprego - utiliza as mesmas variaveis da tab geral salario e emprego
	'text_salario_e_emprego': unicode('Minas Gerais é uma das 27 unidades feder...','utf8'),
	#tab-oportunidades-economicas
	'text_oportunidades_economicas' : unicode('Minas Gerais é uma das 27 unidades federativas do Brasil, localizada na Região Sudeste ','utf8')

	} 
'''

'''yo_query = Ybo.query.join(Cbo).filter(
		Ybo.cbo_id == occupation_id,
		Ybo.year == ybo_max_year_query)

	yo_results = yo_query.values(
		Cbo.name_pt,
		Ybo.num_emp,
		Ybo.num_jobs)

	data = {}
	for name_pt, num_emp, num_jobs in yo_results:
		data['name'] = name_pt
		data['total_employment'] = num_emp
		#data['total']
		#data += (name_pt, num_emp, num_jobs)'''
	