# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request,abort
from dataviva.apps.general.views import get_locale
from dataviva.api.rais.services import Occupation
from dataviva.api.rais.services import OccupationByLocation
from dataviva.api.rais.services import OccupationMunicipalities
from dataviva.api.rais.services import OccupationActivities

from dataviva.api.rais.models import Yo, Ybo
from dataviva.api.attrs.models import Cbo, Bra
from dataviva import db
from sqlalchemy import func

mod = Blueprint('occupation', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/occupation')


tabs = {
    'general': [],
    'opportunities': [
        'economic-opportunities-rings'
    ],

    'wages': [
        'jobs-opportunities-tree_map',
        'jobs-opportunities-stacked',
        'jobs-municipalities-tree_map',
        'jobs-municipalities-geo_map',
        'jobs-municipalities-stacked',
        'wages-opportunities-tree_map',
        'wages-opportunities-stacked',
        'wages-municipalities-tree_map',
        'wages-municipalities-geo_map',
        'wages-municipalities-stacked',
    ],
}


@mod.before_request
def before_request():
    g.page_type = 'category'


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/<occupation_id>/graphs/<tab>', methods=['POST'])
def graphs(occupation_id, tab):
    occupation = Cbo.query.filter_by(id=occupation_id).first_or_404()
    location = Bra.query.filter_by(id=request.args.get('bra_id')).first()
    return render_template('occupation/graphs-'+tab+'.html', occupation=occupation, location=location)

@mod.route('/<occupation_id>', defaults={'tab': 'general'})
@mod.route('/<occupation_id>/<tab>')
def index(occupation_id, tab):
    occupation = Cbo.query.filter_by(id=occupation_id).first_or_404()

    bra_id = request.args.get('bra_id')
    menu = request.args.get('menu')
    url = request.args.get('url')

    location = Bra.query.filter_by(id=bra_id).first()
    language = g.locale
    header = {}
    body = {}
    body = {}

    header['family_id'] = occupation_id[0]

    if len(occupation_id) == 4:
        body['is_family'] = True
    else:
        body['is_family'] = False

    body['is_not_municipality'] = True

    if bra_id:
        occupation_service = OccupationByLocation(
            occupation_id=occupation_id, bra_id=bra_id)
        if len(bra_id) == 9:
            body['is_not_municipality'] = False
    else:
        occupation_service = Occupation(occupation_id=occupation_id)

    occupation_municipalities_service = OccupationMunicipalities(
        occupation_id=occupation_id, bra_id=bra_id)
    occupation_activities_service = OccupationActivities(
        occupation_id=occupation_id, bra_id=bra_id)

    header['average_monthly_income'] = occupation_service.average_monthly_income()
    header['salary_mass'] = occupation_service.salary_mass()
    header['total_employment'] = occupation_service.total_employment()
    header['total_establishments'] = occupation_service.total_establishments()
    header['year'] = occupation_service.year()
    header['age_avg'] = occupation_service.age_avg()

    if body['is_not_municipality']:

        body['municipality_with_more_jobs'] = occupation_municipalities_service.municipality_with_more_jobs()
        body['municipality_with_more_jobs_value'] = occupation_municipalities_service.highest_number_of_jobs()
        body['municipality_with_more_jobs_state'] = occupation_municipalities_service.municipality_with_more_jobs_state()
        body['municipality_with_biggest_wage_avg'] = occupation_municipalities_service.municipality_with_biggest_wage_average()
        body['municipality_with_biggest_wage_avg_value'] = occupation_municipalities_service.biggest_wage_average()
        body['municipality_with_biggest_wage_avg_state'] = occupation_municipalities_service.municipality_with_biggest_wage_average_state()

    body['activity_with_more_jobs'] = occupation_activities_service.activity_with_more_jobs()
    body['activity_with_more_jobs_value'] = occupation_activities_service.highest_number_of_jobs()
    body['activity_with_biggest_wage_avg'] = occupation_activities_service.activity_with_biggest_wage_average()
    body['activity_with_biggest_wage_avg_value'] = occupation_activities_service.biggest_wage_average()
    body['year'] = occupation_activities_service.year()
    
    rais_max_year = db.session.query(func.max(Yo.year)).first()[0]

    if location:
        max_year_query_location = db.session.query(func.max(Ybo.year)).filter(
            Ybo.cbo_id == occupation_id,
            Ybo.bra_id == bra_id)

        rais_query = Ybo.query.filter(
            Ybo.cbo_id_len == len(occupation_id),
            Ybo.bra_id == bra_id,
            Ybo.year == max_year_query_location)\
            .order_by(Ybo.num_jobs.desc())
    else:
        max_year_query = db.session.query(func.max(Yo.year)).filter(
        Yo.cbo_id == occupation_id)

        rais_query = Yo.query.filter(
            Yo.cbo_id_len == len(occupation_id),
            Yo.year == max_year_query)\
            .order_by(Yo.num_jobs.desc())
        
    rais = rais_query.all()
    for index, occ in enumerate(rais):
        if rais[index].cbo_id == occupation_id:
            header['ranking'] = index + 1
            break

    if tab in tabs:
        if menu and url:
            graph = {
                'menu': menu,
                'url': url,
            }
        else:
            graph = None
    else:
        abort(404)

    if header['total_employment'] == None or rais_max_year != header['year']:
        abort(404)
    else:
        return render_template('occupation/index.html', header=header, body=body, occupation=occupation, location=location, language=language, tab=tab, graph=graph)
