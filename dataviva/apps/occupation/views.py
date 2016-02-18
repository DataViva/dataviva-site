# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request
from dataviva.apps.general.views import get_locale
from dataviva.api.rais.services import Occupation
from dataviva.api.rais.services import OccupationByLocation
from dataviva.api.rais.services import OccupationMunicipalities
from dataviva.api.rais.services import OccupationActivities

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

    bra_id = request.args.get('bra_id')
    header = {}
    body = {}

    context = {
        'portrait' : 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d7748245.803118934!2d-49.94643868147362!3d-18.514293729997753!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xa690a165324289%3A0x112170c9379de7b3!2sMinas+Gerais!5e0!3m2!1spt-BR!2sbr!4v1450524997110',
        'average_monthly_income_unity' : 'Milhares',
        'salary_mass_unity' : 'mil',
        'total_employment_unity' : 'milhares',
        'total_establishments_unity' : 'milhares',
        'jobs_municipality_unity' : 'milhares de',
        'activity_for_job_unity': unicode('milhares','utf8'),
        'biggest_average_monsthly_income_unity': unicode('bilhões','utf8'),
        'activity_for_job_unity' : unicode('milhares','utf8'),
        'text_salario_e_emprego': unicode('Minas Gerais é uma das 27 unidades feder...','utf8'),
        'text_oportunidades_economicas' : unicode('Minas Gerais é uma das 27 unidades federativas do Brasil, localizada na Região Sudeste ','utf8'),
    }

    header['cbo_id'] = occupation_id
    
    if len(occupation_id) == 4:
        context['is_family'] = True
    else:
         context['is_family'] = False

    #defaut
    context['is_not_municipality'] = True

    if bra_id:
        occupation_service = OccupationByLocation(occupation_id = occupation_id, bra_id = bra_id)
        if len(bra_id) == 9:
            context['is_not_municipality'] = False
    else:
        occupation_service = Occupation(occupation_id = occupation_id)

    occupation_municipalities_service = OccupationMunicipalities(occupation_id = occupation_id, bra_id=bra_id)
    occupation_activities_service = OccupationActivities(occupation_id = occupation_id, bra_id = bra_id)

    header['name'] = occupation_service.occupation_name()
    header['average_monthly_income'] = occupation_service.average_monthly_income()
    header['salary_mass'] = occupation_service.salary_mass()
    header['total_employment'] = occupation_service.total_employment()
    header['total_establishments'] = occupation_service.total_establishments()
    header['year'] = occupation_service.year()
    
    if context['is_not_municipality']:

        body['municipality_with_more_jobs'] = occupation_municipalities_service.municipality_with_more_jobs()
        body['municipality_with_more_jobs_value'] = occupation_municipalities_service.highest_number_of_jobs()

        body['municipality_with_biggest_wage_avg'] = occupation_municipalities_service.municipality_with_biggest_wage_average()
        body['municipality_with_biggest_wage_avg_value'] = occupation_municipalities_service.biggest_wage_average()

    body['activity_with_more_jobs'] = occupation_activities_service.activity_with_more_jobs()
    body['activity_with_more_jobs_value'] = occupation_activities_service.highest_number_of_jobs()

    body['activity_with_biggest_wage_avg'] = occupation_activities_service.activity_with_biggest_wage_average()
    body['activity_with_biggest_wage_avg_value'] = occupation_activities_service.biggest_wage_average()
    

    return render_template('occupation/index.html', body_class='perfil-estado', context=context, header = header, body = body)
