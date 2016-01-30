# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale

from dataviva.api.attrs.models import Cbo, Bra, Cnae
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
    bra_id = None #'1ac'
    header = {}
    body = {}

    #se tiver sido selecionada uma localidade especific
    if bra_id:

        #encontrando o ano mais recente 
        ybo_max_year= db.session.query(func.max(Ybo.year)).filter(
            Ybo.cbo_id == occupation_id, 
            Ybo.bra_id == bra_id)\
            .one()
            
        year = 0
        for year in ybo_max_year:
            year = year

        ybo_header_generator = Ybo.query.join(Cbo).filter(
            Ybo.cbo_id == occupation_id,
            Ybo.bra_id == bra_id,
            Ybo.year == year)\
            .values(Cbo.name_pt,
                    Ybo.wage_avg,
                    Ybo.wage,
                    Ybo.num_jobs,
                    Ybo.num_est)

        ybo_county_num_jobs_generator = Ybo.query.join(Bra).filter(
                Ybo.cbo_id == occupation_id,
                Ybo.bra_id.like(bra_id+'%'),
                Ybo.year == year,
                Ybo.bra_id_len == 9)\
            .order_by(desc(Ybo.num_jobs)).limit(1)\
            .values(Bra.name_pt,
                    Ybo.num_jobs)

        ybo_county_wage_avg_generator = Ybo.query.join(Bra).filter(
                Ybo.cbo_id == occupation_id,
                Ybo.bra_id.like(bra_id+'%'),
                Ybo.year == year,
                Ybo.bra_id_len == 9)\
            .order_by(desc(Ybo.wage_avg)).limit(1)\
            .values(Bra.name_pt,
                    Ybo.wage_avg)
        

        ybio_activity_num_jobs_generator = Ybio.query.join(Cnae).filter(
                Ybio.cbo_id == occupation_id,
                Ybio.bra_id.like(bra_id+'%'),
                Ybio.year == year,
                Ybio.cnae_id_len == 6)\
            .order_by(desc(Ybio.num_jobs)).limit(1)\
            .values(Cnae.name_pt,
                    Ybio.num_jobs)
        

        ybio_activity_wage_avg_generator = Ybio.query.join(Cnae).filter(
                Ybio.cbo_id == occupation_id,
                Ybio.bra_id.like(bra_id+'%'),
                Ybio.year == year,
                Ybio.cnae_id_len == 6)\
            .order_by(desc(Ybio.wage_avg)).limit(1)\
            .values(Cnae.name_pt,
                    Ybio.wage_avg)

        
        header['year'] = year

        for name_pt, wage_avg, wage, num_jobs, num_est in ybo_header_generator:
            header['name'] = name_pt
            header['average_monthly_income'] = wage_avg
            header['salary_mass'] = wage
            header['total_employment'] = num_jobs
            header['total_establishments'] = num_est

        for name_pt, num_jobs in ybo_county_num_jobs_generator:
            body['county_for_jobs'] = name_pt
            body['num_jobs_county'] = num_jobs

        for name_pt, wage_avg in ybio_activity_wage_avg_generator:
            body['activity_higher_income'] = name_pt
            body['value_activity_higher_income'] = wage_avg     

        for name_pt, wage_avg in ybo_county_wage_avg_generator:
            body['county_bigger_average_monsthly_income'] = name_pt
            body['bigger_average_monsthly_income'] = wage_avg   

        for name_pt, num_jobs in ybio_activity_num_jobs_generator:
            body['activity_for_job'] = name_pt
            body['num_activity_for_job'] = num_jobs 


    else: 
        
        #encontrando o ano mais recente 
        yo_max_year= db.session.query(func.max(Yo.year)).filter(
            Ybo.cbo_id == occupation_id)\
            .one()
            
        year = 0
        for year in yo_max_year:
            year = year

        #quando nao temos a localidade, buscamos em todo o brasil - rais_yo
        yo_header_generator = Yo.query.join(Cbo).filter(
            Yo.cbo_id == occupation_id,
            Yo.year == year)\
            .values(Cbo.name_pt,
                    Yo.wage_avg,
                    Yo.wage,
                    Yo.num_jobs,
                    Yo.num_est)

        ybo_county_num_jobs_generator = Ybo.query.join(Bra).filter(
                Ybo.cbo_id == occupation_id,
                Ybo.year == year,
                Ybo.bra_id_len == 9)\
            .order_by(desc(Ybo.num_jobs)).limit(1)\
            .values(Bra.name_pt,
                    Ybo.num_jobs)

        ybo_county_wage_avg_generator = Ybo.query.join(Bra).filter(
                Ybo.cbo_id == occupation_id,
                Ybo.year == year,
                Ybo.bra_id_len == 9)\
            .order_by(desc(Ybo.wage_avg)).limit(1)\
            .values(Bra.name_pt,
                    Ybo.wage_avg)
        

        yio_activity_num_jobs_generator = Yio.query.join(Cnae).filter(
                Yio.cbo_id == occupation_id,
                Yio.year == year,
                Yio.cnae_id_len == 6)\
            .order_by(desc(Yio.num_jobs)).limit(1)\
            .values(Cnae.name_pt,
                    Yio.num_jobs)
        

        yio_activity_wage_avg_generator = Yio.query.join(Cnae).filter(
                Yio.cbo_id == occupation_id,
                Yio.year == year,
                Yio.cnae_id_len == 6)\
            .order_by(desc(Yio.wage_avg)).limit(1)\
            .values(Cnae.name_pt,
                    Yio.wage_avg)

        
        header['year'] = year

        for name_pt, wage_avg, wage, num_jobs, num_est in yo_header_generator:
            header['name'] = name_pt
            header['average_monthly_income'] = wage_avg
            header['salary_mass'] = wage
            header['total_employment'] = num_jobs
            header['total_establishments'] = num_est

        for name_pt, num_jobs in ybo_county_num_jobs_generator:
            body['county_for_jobs'] = name_pt
            body['num_jobs_county'] = num_jobs

        for name_pt, wage_avg in yio_activity_wage_avg_generator:
            body['activity_higher_income'] = name_pt
            body['value_activity_higher_income'] = wage_avg     

        for name_pt, wage_avg in ybo_county_wage_avg_generator:
            body['county_bigger_average_monsthly_income'] = name_pt
            body['bigger_average_monsthly_income'] = wage_avg   

        for name_pt, num_jobs in yio_activity_num_jobs_generator:
            body['activity_for_job'] = name_pt
            body['num_activity_for_job'] = num_jobs 

    #dados que ainda sofrerāo alteracoes  
    context = {
        'family' : True,
        #unidades
        'average_monthly_income_unity' : 'Milhares', #'unidade_renda_media_mensal'
        'salary_mass_unity' : 'mil',
        'total_employment_unity' : 'milhares', 
        'total_establishments_unity' : 'milhares', #'unidade_total_estabelecimentos' 
        #unidades
        'jobs_county_unity' : 'milhares de', #'unidade_empregos_principal_municipio'
        'activity_for_job_unity': unicode('bilhões','utf8'), #unidade_atividade_por_empregos
        'bigger_average_monsthly_income_unity': unicode('bilhões','utf8'),
        'activity_for_job_unity' : unicode('bilhoes','utf8'),
        #tab-salario-emprego
        'text_salario_e_emprego': unicode('Minas Gerais é uma das 27 unidades feder...','utf8'),
        #tab-oportunidades-economicas
        'text_oportunidades_economicas' : unicode('Minas Gerais é uma das 27 unidades federativas do Brasil, localizada na Região Sudeste ','utf8')

    } 
    #acessar o contex do diogo com context.id.oqeuquero

    
    return render_template('occupation/index.html', body_class='perfil-estado', context=context, header = header, body = body)
