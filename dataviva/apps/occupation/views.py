# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request
from dataviva.apps.general.views import get_locale
from dataviva.api.rais.services import Occupation
from dataviva.api.rais.services import OccupationByLocation
from dataviva.api.rais.services import OccupationMunicipalities
from dataviva.api.rais.services import OccupationActivities

from dataviva.api.rais.models import Yi, Yo, Ybo, Ybi, Yio, Ybio
from dataviva import db
from sqlalchemy import func, desc

mod = Blueprint('occupation', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/occupation')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/<occupation_id>')
def index(occupation_id):

    #Use Example /occupation/2122 OR /occupation/2122?bra_id=4mg
    bra_id = request.args.get('bra_id')
    header = {}
    body = {}
    context = {}

    header['cbo_id'] = occupation_id

    if len(occupation_id) == 4:
        context['is_family'] = True
    else:
         context['is_family'] = False

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
    header['age_avg'] = occupation_service.age_avg()

    if context['is_not_municipality']:

        body['municipality_with_more_jobs'] = occupation_municipalities_service.municipality_with_more_jobs()
        body['municipality_with_more_jobs_value'] = occupation_municipalities_service.highest_number_of_jobs()

        body['municipality_with_biggest_wage_avg'] = occupation_municipalities_service.municipality_with_biggest_wage_average()
        body['municipality_with_biggest_wage_avg_value'] = occupation_municipalities_service.biggest_wage_average()

    body['activity_with_more_jobs'] = occupation_activities_service.activity_with_more_jobs()
    body['activity_with_more_jobs_value'] = occupation_activities_service.highest_number_of_jobs()

    body['activity_with_biggest_wage_avg'] = occupation_activities_service.activity_with_biggest_wage_average()
    body['activity_with_biggest_wage_avg_value'] = occupation_activities_service.biggest_wage_average()

    #query relativa a posicao do ranking
    max_year_query= db.session.query(func.max(Yo.year)).filter(
            Yo.cbo_id == occupation_id)
    rais_query = Yo.query.filter(
        Yo.year == max_year_query)\
        .order_by(Yo.num_jobs.desc())
    rais = rais_query.all()
    for index, occ in enumerate(rais):
        if rais[index].cbo_id == occupation_id:
            header['ranking'] = index + 1
            break

    return render_template('occupation/index.html', body_class='perfil-estado', context=context, header = header, body = body)
