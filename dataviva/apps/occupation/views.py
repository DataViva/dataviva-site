# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale

from dataviva.api.attrs.models import Cbo, Bra, Cnae
from dataviva.api.rais.models import Yo, Ybo, Yio, Ybio

from dataviva.api.rais.services import Occupation as RaisOccupationService

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


@mod.route('/<occupation_id>')
def index(occupation_id):

    #occupation_id = '2122'
    bra_id = '4mg'
    header = {}
    body = {}

    #se tiver sido selecionada uma localidade especific
    '''
    if bra_id:



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




        for name_pt, wage_avg in ybio_activity_wage_avg_generator:
            body['activity_higher_income'] = name_pt
            body['value_activity_higher_income'] = wage_avg     

        for name_pt, wage_avg in ybo_county_wage_avg_generator:
            body['county_bigger_average_monsthly_income'] = name_pt
            body['bigger_average_monsthly_income'] = wage_avg   

        for name_pt, num_jobs in ybio_activity_num_jobs_generator:
            body['activity_for_job'] = name_pt
            body['num_activity_for_job'] = num_jobs 

    ######################## else ##########################
    else: 

        #quando nao temos a localidade, buscamos em todo o brasil - rais_yo


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
    '''
    if bra_id: 
        rais_occupation_service = RaisOccupationService(occupation_id = occupation_id, bra_id = bra_id)
        header['year'] = rais_occupation_service.year
        header.update(rais_occupation_service.get_ybo_header())
        body.update(rais_occupation_service.get_ybo_county_num_jobs_with_bra_id())

    else:
        rais_occupation_service = RaisOccupationService(occupation_id = occupation_id)
        header['year'] = rais_occupation_service.year
        header.update(rais_occupation_service.get_yo_header())


    context = {
        #'family' : True,
        'portrait' : 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d7748245.803118934!2d-49.94643868147362!3d-18.514293729997753!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xa690a165324289%3A0x112170c9379de7b3!2sMinas+Gerais!5e0!3m2!1spt-BR!2sbr!4v1450524997110',
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

    if len(occupation_id) == 4: 
        context['family'] = True
    else:
         context['family'] = False  
    #acessar o contex do diogo com context.id.oqeuquero

    
    return render_template('occupation/index.html', body_class='perfil-estado', context=context, header = header, body = body)
