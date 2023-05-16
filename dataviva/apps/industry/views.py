# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request, abort
from dataviva.apps.general.views import get_locale
from dataviva.api.rais.services import Industry, IndustryOccupation, IndustryMunicipality, IndustryByLocation
from dataviva.api.attrs.models import Cnae, Bra
from os import walk
import os
import requests

mod = Blueprint('industry', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/industry')


@mod.before_request
def before_request():
    g.page_type = 'category'


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


def getRaisLatestYear():
    latestRaisYear = "2020"

    response = requests.get(g.api_url + "years/rais")

    if response.status_code == 200:
        data = response.json()
        localData = data["years"]
        
        latestRaisYear = localData[len(localData) - 1]

    return latestRaisYear

def location_depth(bra_id):
    locations = {
        1: "region",
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


@mod.route('/<industry_id>/graphs/<tab>', methods=['POST'])
def graphs(industry_id, tab):
    industry = Cnae.query.filter_by(id=industry_id).first_or_404()
    location = Bra.query.filter_by(id=request.args.get('bra_id')).first()

    bra_id = request.args.get('bra_id')
    if not bra_id:
        depth = None
        id_ibge = None
    else:
        depth = location_depth(bra_id)
        id_ibge = location_service(depth, location)
        
    latestRaisYear = getRaisLatestYear()
    return render_template('industry/graphs-'+tab+'.html', industry=industry, location=location, graph=None, id_ibge=id_ibge, latestRaisYear=latestRaisYear)


@mod.route('/<cnae_id>', defaults={'tab': 'general'})
@mod.route('/<cnae_id>/<tab>')
def index(cnae_id, tab):

    header = {}
    body = {}
    menu = request.args.get('menu')
    url = request.args.get('url')
    bra_id = request.args.get('bra_id')
    graph = {}

    if menu:
        graph['menu'] = menu
    if url:
        url_prefix = menu.split('-')[-1] + '/' if menu and menu.startswith('new-api-') else 'embed/'
        graph['url'] = url_prefix + url

    industry = Cnae.query.filter_by(id=cnae_id).first_or_404()
    location = Bra.query.filter_by(id=bra_id).first()

    bra_id = request.args.get('bra_id')
    bra_id = bra_id if bra_id != 'all' else None
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

    industry_occupation_service = IndustryOccupation(bra_id=location_id, cnae_id=industry.id)
    industry_municipality_service = IndustryMunicipality(bra_id=location_id, cnae_id=industry.id)

    if location:
        industry_service = IndustryByLocation(bra_id=location_id, cnae_id=industry.id)
        if len(industry.id) == 6:
            header['rca'] = industry_service.rca()
            header['distance'] = industry_service.distance()
            header['opportunity_gain'] = industry_service.opportunity_gain()

        if len(location_id) != 9:
            body['municipality_with_more_num_jobs_value'] = industry_municipality_service.highest_number_of_jobs()
            body[
                'municipality_with_more_num_jobs_name'] = industry_municipality_service.municipality_with_more_num_jobs()
            body[
                'municipality_with_more_num_jobs_state'] = industry_municipality_service.municipality_with_more_jobs_state()
            body[
                'municipality_with_more_wage_avg_name'] = industry_municipality_service.municipality_with_more_wage_average()
            body['municipality_with_more_wage_avg_value'] = industry_municipality_service.biggest_wage_average()
            body['municipality_with_more_wage_avg_state'] = industry_municipality_service.municipality_with_biggest_wage_average_state()


    else:
        industry_service = Industry(cnae_id=industry.id)

        body['municipality_with_more_num_jobs_value'] = industry_municipality_service.highest_number_of_jobs()
        body['municipality_with_more_num_jobs_name'] = industry_municipality_service.municipality_with_more_num_jobs()
        body[
            'municipality_with_more_wage_avg_name'] = industry_municipality_service.municipality_with_more_wage_average()
        body['municipality_with_more_wage_avg_value'] = industry_municipality_service.biggest_wage_average()
        body['municipality_with_more_num_jobs_state'] = industry_municipality_service.municipality_with_more_jobs_state()
        body['municipality_with_more_wage_avg_state'] = industry_municipality_service.municipality_with_biggest_wage_average_state()

    body['occ_with_more_wage_avg_name'] = industry_occupation_service.occupation_with_biggest_wage_average()
    body['occ_with_more_wage_avg_value'] = industry_occupation_service.biggest_wage_average()
    body['occ_with_more_number_jobs_name'] = industry_occupation_service.occupation_with_more_jobs()
    body['occ_with_more_number_jobs_value'] = industry_occupation_service.highest_number_of_jobs()

    header['average_monthly_income'] = industry_service.average_monthly_income()
    header['salary_mass'] = industry_service.salary_mass()
    header['num_jobs'] = industry_service.num_jobs()
    #header['name_bra'] = industry_service.name()

    # Get rankings vars, code should be refactored
    from dataviva import db
    from sqlalchemy import func, desc
    from dataviva.api.rais.models import Yi, Ybi

    if location:
        ybi_max_year = db.session.query(func.max(Ybi.year)).filter_by(cnae_id=industry.id, bra_id=location.id)
        list_rais = Ybi.query.filter(
            Ybi.year == ybi_max_year,
            Ybi.bra_id == location.id,
            Ybi.cnae_id_len == func.length(industry.id)).order_by(desc(Ybi.num_jobs)).all()

    else:
        yi_max_year = db.session.query(func.max(Yi.year)).filter_by(cnae_id=industry.id)
        list_rais = Yi.query.filter(
            Yi.year == yi_max_year,
            Yi.cnae_id_len == func.length(industry.id)).order_by(desc(Yi.num_jobs)).all()

    for index, rais in enumerate(list_rais):
        if rais.cnae_id == cnae_id:
            header['ranking'] = index + 1
            break

    header['year'] = industry_service.get_year()

    rais_max_year = db.session.query(func.max(Yi.year)).first()[0]
    
    tabs = {
        'general': [],

        'opportunities': [
            'economic-activities-rings',
            'new-api-economic-activities-rings'
        ],

        'wages': [
            'jobs-occupation-tree_map',
            'new-api-jobs-occupation-tree_map',
            'jobs-occupation-stacked',
            'new-api-jobs-occupation-stacked',
            'jobs-municipality-geo_map',
            'new-api-jobs-municipality-geo_map',
            'jobs-municipality-tree_map',
            'new-api-jobs-municipality-tree_map',
            'jobs-municipality-stacked',
            'new-api-jobs-municipality-stacked',
            'wages-occupation-tree_map',
            'new-api-wages-occupation-tree_map',
            'wages-occupation-stacked',
            'new-api-wages-occupation-stacked',
            'wages-municipality-geo_map',
            'new-api-wages-municipality-geo_map',
            'wages-municipality-tree_map',
            'new-api-wages-municipality-tree_map',
            'wages-municipality-stacked',
            'new-api-wages-municipality-stacked',
            'wages-distribution-bar',
        ]
    }

    if tab not in tabs:
        abort(404)

    if menu and menu not in tabs[tab]:
        abort(404)

    if header['num_jobs'] is None or rais_max_year != header['year']:
        abort(404)
    latestRaisYear = getRaisLatestYear()
    return render_template('industry/index.html', header=header, body=body, industry=industry, location=location, tab=tab, graph=graph, id_ibge=id_ibge, latestRaisYear=latestRaisYear)
