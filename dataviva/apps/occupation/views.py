# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.rais.services import Occupation as RaisOccupationService
from dataviva.api.rais.services import OccupationByLocation as RaisOccupationByLocationService

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

    bra_id = None#'4mg'
    header = {}
    body = {}

    if bra_id: 
        rais_occupation_service = RaisOccupationByLocationService(occupation_id = occupation_id, bra_id = bra_id)

    else:
        rais_occupation_service = RaisOccupationService(occupation_id = occupation_id)
        
    header['name'] = rais_occupation_service.name()
    header['average_monthly_income'] = rais_occupation_service.average_monthly_income()
    header['salary_mass'] = rais_occupation_service.salary_mass()
    header['total_employment'] = rais_occupation_service.total_employment()
    header['total_establishments'] = rais_occupation_service.total_establishments()
    header['year'] = rais_occupation_service.year
    
    body.update(rais_occupation_service.municipality_with_more_jobs())
    body.update(rais_occupation_service.municipality_with_biggest_wage_average())
    body.update(rais_occupation_service.activity_with_more_jobs())
    body.update(rais_occupation_service.activity_with_biggest_wage_average())

    context = {
        'portrait' : 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d7748245.803118934!2d-49.94643868147362!3d-18.514293729997753!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xa690a165324289%3A0x112170c9379de7b3!2sMinas+Gerais!5e0!3m2!1spt-BR!2sbr!4v1450524997110',
        'average_monthly_income_unity' : 'Milhares',
        'salary_mass_unity' : 'mil',
        'total_employment_unity' : 'milhares', 
        'total_establishments_unity' : 'milhares', 
        'jobs_municipality_unity' : 'milhares de', 
        'activity_for_job_unity': unicode('bilhões','utf8'), 
        'bigger_average_monsthly_income_unity': unicode('bilhões','utf8'),
        'activity_for_job_unity' : unicode('bilhoes','utf8'),
        'text_salario_e_emprego': unicode('Minas Gerais é uma das 27 unidades feder...','utf8'),
        'text_oportunidades_economicas' : unicode('Minas Gerais é uma das 27 unidades federativas do Brasil, localizada na Região Sudeste ','utf8'),
    } 

    if len(occupation_id) == 4: 
        context['family'] = True
    else:
         context['family'] = False  
    
    return render_template('occupation/index.html', body_class='perfil-estado', context=context, header = header, body = body)
