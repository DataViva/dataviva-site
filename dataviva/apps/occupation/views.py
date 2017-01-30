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


@mod.before_request
def before_request():
    g.page_type = 'category'


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())

def location_depth(bra_id):
    locations = {
        1: "region",    #todo
        3: "state",
        5: "mesoregion",
        7: "microregion",
        9: "municipality"
    }

    return locations[len(bra_id)]

def handle_region_bra_id(bra_id):
    return {
        "1": "1",
        "2": "2",
        "3": "5",
        "4": "3",
        "5": "4"
    }[bra_id]

def location_service(depth, location):
    if depth == 'region':
        return handle_region_bra_id(location.id)
    if depth == 'mesoregion':
        return str(location.id_ibge)[:2] + str(location.id_ibge)[-2:]
    if depth == 'microregion':
        return str(location.id_ibge)[:2] + str(location.id_ibge)[-3:]
    else:
        return location.id_ibge

@mod.route('/<occupation_id>/graphs/<tab>', methods=['POST'])
def graphs(occupation_id, tab):
    occupation = Cbo.query.filter_by(id=occupation_id).first_or_404()
    location = Bra.query.filter_by(id=request.args.get('bra_id')).first()

    bra_id = request.args.get('bra_id')
    if not bra_id:
        depth = None
        id_ibge = None
    else:
        depth = location_depth(bra_id)
        id_ibge = location_service(depth, location)

    return render_template('occupation/graphs-'+tab+'.html', occupation=occupation, location=location, graph=None, id_ibge=id_ibge)

@mod.route('/<occupation_id>', defaults={'tab': 'general'})
@mod.route('/<occupation_id>/<tab>')
def index(occupation_id, tab):
    occupation = Cbo.query.filter_by(id=occupation_id).first_or_404()

    bra_id = request.args.get('bra_id')
    bra_id = bra_id if bra_id != 'all' else None

    menu = request.args.get('menu')
    url = request.args.get('url')

    location = Bra.query.filter_by(id=bra_id).first()
    is_municipality = location and len(location.id) == 9
    header = {}
    body = {}
    graph = {}
    
    if menu:
        graph['menu'] = menu
    if url:
        graph['url'] = url

    if not bra_id:
        depth = None
        id_ibge = None
    else:
        depth = location_depth(bra_id)
        id_ibge = location_service(depth, location)

    if location:
        location_id = location.id
    else:
        location_id = None


    header['family_id'] = occupation_id[0]

    if len(occupation_id) == 4:
        body['is_family'] = True
    else:
        body['is_family'] = False

    if bra_id:
        occupation_service = OccupationByLocation(
            occupation_id=occupation_id, bra_id=bra_id)
    else:
        occupation_service = Occupation(occupation_id=occupation_id)

    tabs = {
        'general': [],
        'opportunities': [
            'economic-opportunities-rings'
        ],

        'wages': [
            'jobs-economic-activities-tree_map',
            'jobs-economic-activities-stacked',
            'wages-economic-activities-tree_map',
            'wages-economic-activities-stacked',
        ],
    }

    if not is_municipality:
        tabs['wages'] += [
            'jobs-municipality-tree_map',
            'jobs-municipality-geo_map',
            'jobs-municipality-stacked',
            'wages-municipality-tree_map',
            'wages-municipality-geo_map',
            'wages-municipality-stacked',
        ]

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

    if not is_municipality:
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

    if tab not in tabs:
        abort(404)

    if menu and menu not in tabs[tab]:
        abort(404)

    if header['total_employment'] == None or rais_max_year != header['year']:
        abort(404)
    else:
        return render_template('occupation/index.html', header=header, body=body, occupation=occupation, location=location, is_municipality=is_municipality, tab=tab, graph=graph, id_ibge=id_ibge)
