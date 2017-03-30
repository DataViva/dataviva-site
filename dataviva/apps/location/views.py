# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, abort, request
from dataviva import db
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.services import Location as LocationService, LocationGdpRankings, \
    LocationGdpPerCapitaRankings, LocationPopRankings, LocationAreaRankings, LocationMunicipalityRankings, Bra
from dataviva.api.secex.models import Ymb
from dataviva.api.secex.services import Location as LocationBodyService, LocationWld, LocationEciRankings
from dataviva.api.rais.services import LocationIndustry, LocationOccupation, \
    LocationJobs, LocationDistance, LocationOppGain
from dataviva.api.hedu.services import LocationUniversity, LocationMajor
from dataviva.api.sc.services import LocationSchool, LocationBasicCourse
from dataviva.api.attrs.services import All
from dataviva.api.secex.services import Product
from dataviva.api.rais.services import Industry
from dataviva.api.rais.services import Occupation
from dataviva.api.hedu.services import University
from dataviva.api.sc.services import Basic_course
from dataviva.api.hedu.services import Major
from dataviva.api.sc.services import AllScholar
from dataviva.api.sc.services import AllBasicCourse
from dataviva.api.attrs.models import Wld
from sqlalchemy import desc, func
from random import randint
from decimal import *
import sys


reload(sys)
sys.setdefaultencoding('utf8')

mod = Blueprint('location', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/location',
                static_folder='static')

tabs = {
        'general': [],
        'opportunities': [
            'product-space-scatter',
            'activities-space-network',
            'activities-space-scatter',
        ],

        'wages': [
            'jobs-industry-tree_map',
            'new-api-jobs-industry-tree_map',
            'jobs-industry-stacked',
            'jobs-occupation-tree_map',
            'new-api-jobs-occupation-tree_map',
            'jobs-occupation-stacked',
            'wage-industry-tree_map',
            'new-api-wage-industry-tree_map',
            'wage-industry-stacked',
            'wage-occupation-tree_map',
            'new-api-wage-occupation-tree_map',
            'wage-occupation-stacked',
        ],

        'trade-partner': [
            'trade-balance-location-line',
            'exports-products-tree_map',
            'new-api-exports-products-tree_map',
            'exports-products-stacked',
            'exports-destination-tree_map',
            'new-api-exports-destination-tree_map',
            'exports-destination-stacked',
            'imports-products-tree_map',
            'new-api-imports-products-tree_map',
            'imports-products-stacked',
            'imports-origin-tree_map',
            'new-api-imports-origin-tree_map',
            'imports-origin-stacked',
            'new-api-imports-port',
            'new-api-exports-port',
        ],

        'education': [
            'higher-education-university-tree_map',
            'education-course-tree_map',
            'professional-education-school-tree_map',
            'professional-education-course-tree_map',
            'basic-education-administrative-dependencie-tree_map',
            'basic-education-level-tree_map',
        ],
        'health': [
            'equipments-municipality-tree_map',
            'equipments-municipality-map',
            'equipments-municipality-stacked',
            'equipments-type-tree_map',
            'equipments-type-bar',
            'equipments-type-stacked',
            'equipments-sus-bond-bar',
            'establishments-municipality-tree_map',
            'establishments-municipality-map',
            'establishments-municipality-stacked',
            'establishments-provider-type-tree_map',
            'establishments-provider-type-stacked',
            'establishments-unit-type-tree_map',
            'establishments-unit-type-stacked',
            'beds-municipality-tree_map',
            'beds-municipality-map',
            'beds-municipality-stacked',
            'beds-bed-type-tree_map',
            'beds-bed-type-stacked', 
            'beds-type-speciality-tree_map',
            'beds-type-speciality-stacked',
            'beds-type-bar',
            'beds-sus-bond-bar',
            'beds-availability-bar',
            'professionals-municipality-tree_map',
            'professionals-municipality-map',
            'professionals-municipality-stacked',
            'professionals-provider-unit-tree_map',
            'professionals-provider-unit-stacked',
            'professionals-occupation-tree_map',
            'professionals-occupation-stacked',  
            'professionals-bond-tree_map',
            'professionals-bond-stacked',
        ]
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


def _location_service(depth, location):
    if depth == 'region':
        return handle_region_bra_id(location.id)
    if depth == 'mesoregion':
        return str(location.id_ibge)[:2] + str(location.id_ibge)[-2:]
    if depth == 'microregion':
        return str(location.id_ibge)[:2] + str(location.id_ibge)[-3:]
    else:
        return location.id_ibge


@mod.route('/<bra_id>/graphs/<tab>', methods=['POST'])
def graphs(bra_id, tab):
    if bra_id == 'all':
        location = Wld.query.filter_by(id='sabra').first()
        location.id = 'all'
        depth = None
        id_ibge = None
    else:
        location = Bra.query.filter_by(id=bra_id).first()
        depth = location_depth(bra_id)
        id_ibge = _location_service(depth, location)

    return render_template('location/graphs-' + tab + '.html', location=location, depth=depth, id_ibge=id_ibge, graph=None)


@mod.route('/all', defaults={'tab': 'general'})
@mod.route('/all/<tab>')
def all(tab):
    location_service_brazil = All()
    product_service = Product(product_id=None)
    industry_service = Industry(cnae_id=None)
    occupation_service = Occupation(occupation_id=None)
    university_service = University(university_id=None)
    basic_course_service = Basic_course(course_sc_id=None)
    major_service = Major(course_hedu_id=None, bra_id=None)
    scholar_service = AllScholar()
    basic_course_service = AllBasicCourse()

    location = Wld.query.filter_by(id='sabra').first_or_404()
    location.id = 'all'
    is_municipality = False
    menu = request.args.get('menu')
    url = request.args.get('url')

    graph = {}

    if menu:
        graph['menu'] = menu
    if url:
        url_prefix = menu.split('-')[-1] + '/' if menu and menu.startswith('new-api-') or tab == 'health' else 'embed/'
        graph['url'] = url_prefix + url

    profile = {}

    header = {
        'bg_class_image': 'bg-all',
        'gdp': location_service_brazil.gdp(),
        'population': location_service_brazil.population(),
        'gdp_per_capita': location_service_brazil.gdp_per_capita(),
        'eci': 0.151,
        'year_yb': location_service_brazil.year_yb(),
        'year_ybs': location_service_brazil.year_ybs()
    }

    body = {
        'product_year': product_service.year(),
        'main_product_by_export_value': product_service.highest_export_value(),
        'main_product_by_export_value_name': product_service.highest_export_value_name(),
        'main_product_by_import_value': product_service.highest_import_value(),
        'main_product_by_import_value_name': product_service.highest_import_value_name(),
        'total_imports': product_service.all_imported(),
        'total_exports': product_service.all_exported(),
        'all_trade_balance': product_service.all_trade_balance(),

        'industry_year': industry_service.get_year(),
        'main_industry_by_num_jobs': industry_service.main_industry_by_num_jobs(),
        'main_industry_by_num_jobs_name': industry_service.main_industry_by_num_jobs_name(),
        'main_occupation_by_num_jobs': occupation_service.main_occupation_by_num_jobs(),
        'main_occupation_by_num_jobs_name': occupation_service.main_occupation_by_num_jobs_name(),
        'avg_wage': industry_service.avg_wage(),
        'wage': industry_service.all_salary_mass(),
        'total_jobs': industry_service.total_jobs(),

        'university_year': university_service.year(),
        'highest_enrolled_by_university': university_service.highest_enrolled_by_university(),
        'highest_enrolled_by_university_name': university_service.highest_enrolled_by_university_name(),
        'highest_enrolled_by_major': major_service.highest_enrolled_by_major(),
        'highest_enrolled_by_major_name': major_service.highest_enrolled_by_major_name(),
        'highest_enrolled_by_school': scholar_service.highest_enrolled_by_school(),
        'highest_enrolled_by_school_name': scholar_service.highest_enrolled_by_school_name(),
        'highest_enrolled_by_basic_course': basic_course_service.highest_enrolled_by_basic_course(),
        'highest_enrolled_by_basic_course_name': basic_course_service.highest_enrolled_by_basic_course_name()
    }

    if body['total_exports'] is None and body['total_imports'] is None and body['total_jobs'] is None and \
            body['highest_enrolled_by_university'] is None and body['highest_enrolled_by_basic_course'] is None and \
            body['highest_enrolled_by_major'] is None:
            abort(404)

    if tab not in tabs:
        abort(404)

    if menu and menu not in tabs[tab]:
        abort(404)

    else:
        return render_template('location/index.html',
                            header=header, body=body, profile=profile, location=location, is_municipality=is_municipality, tab=tab, graph=graph)


@mod.route('/<bra_id>', defaults={'tab': 'general'})
@mod.route('/<bra_id>/<tab>')
def index(bra_id, tab):
    location = Bra.query.filter_by(id=bra_id).first_or_404()
    is_municipality = location and len(location.id) == 9
    menu = request.args.get('menu')
    url = request.args.get('url')

    if bra_id == 'all':
        depth = None
        id_ibge = None
    else:
        depth = location_depth(bra_id)
        id_ibge = _location_service(depth, location)

    if location:
        location_id = location.id
    else:
        location_id = None

    graph = {}

    if menu:
        graph['menu'] = menu
    if url:
        url_prefix = menu.split('-')[-1] + '/' if menu and menu.startswith('new-api-') else 'embed/'
        graph['url'] = url_prefix + url

    depth = location_depth(bra_id)
    if depth == 'region':
        id_ibge = handle_region_bra_id(location.id)
    elif depth == 'mesoregion':
        id_ibge = str(location.id_ibge)[:2] + str(location.id_ibge)[-2:]
    elif depth == 'microregion':
        id_ibge = str(location.id_ibge)[:2] + str(location.id_ibge)[-3:]
    else:
        id_ibge = location.id_ibge

    if not is_municipality:
        tabs['wages'] += [
            'jobs-municipalities-tree_map',
            'new-api-jobs-municipalities-tree_map',
            'jobs-municipalities-geo_map',
            'jobs-municipalities-stacked',
            'wages-municipalities-tree_map',
            'new-api-wages-municipalities-tree_map',
            'wages-municipalities-geo_map',
            'wages-municipalities-stacked',
        ]

        tabs['wages'] += [
            'jobs-municipality-tree_map',
            'new-api-jobs-municipality-tree_map',
            'jobs-municipality-stacked',
            'wages-municipality-tree_map',
            'new-api-wages-municipality-tree_map',
            'wages-municipality-stacked',
        ]

        tabs['trade-partner'] += [
            'exports-municipality-tree_map',
            'new-api-exports-municipality-tree_map',
            'exports-municipality-stacked',
            'imports-municipality-tree_map',
            'new-api-imports-municipality-tree_map',
            'imports-municipality-stacked',

        ]

        tabs['education'] += [
            'education-municipality-tree_map',
            'new-api-education-municipality-tree_map',
            'basic-education-municipality-tree_map',
            'new-api-basic-education-municipality-tree_map',
        ]

    location_service = LocationService(bra_id=bra_id)
    location_gdp_rankings_service = LocationGdpRankings(
        bra_id=bra_id, stat_id='gdp')
    location_gdp_pc_rankings_service = LocationGdpPerCapitaRankings(
        bra_id=bra_id)
    location_pop_rankings_service = LocationPopRankings(bra_id=bra_id)
    location_eci_rankings_service = LocationEciRankings(bra_id=bra_id)
    location_area_rankings_service = LocationAreaRankings(bra_id=bra_id)
    location_municipality_rankings_service = LocationMunicipalityRankings(bra_id=bra_id)
    location_wld_service = LocationWld(bra_id=bra_id)
    location_secex_service = LocationBodyService(bra_id=bra_id)
    location_industry_service = LocationIndustry(bra_id=bra_id)
    location_occupation_service = LocationOccupation(bra_id=bra_id)
    location_jobs_service = LocationJobs(bra_id=bra_id)
    location_distance_service = LocationDistance(bra_id=bra_id)
    location_opp_gain_service = LocationOppGain(bra_id=bra_id)
    location_university_service = LocationUniversity(bra_id=bra_id)
    location_major_service = LocationMajor(bra_id=bra_id)
    location_school_service = LocationSchool(bra_id=bra_id)
    location_basic_course_service = LocationBasicCourse(bra_id=bra_id)

    ''' Query básica para SECEX'''
    max_year_query = db.session.query(
        func.max(Ymb.year)).filter_by(bra_id=bra_id, month=12)

    eci = Ymb.query.filter(
        Ymb.bra_id == bra_id,
        Ymb.month == 0,
        Ymb.year == max_year_query) \
        .order_by(desc(Ymb.year)).limit(1).first()

    ''' Background Image'''
    if len(bra_id) == 1:
        countys = Bra.query.filter(Bra.id.like(bra_id + '%'), func.length(Bra.id) == 3).all()
        background_image = "bg-" + str(countys[randint(0, len(countys) - 1)].id) + "_" + str(randint(1, 2))
    else:
        background_image = "bg-" + location.id[:3] + "_" + str(randint(1, 2))

    if len(bra_id) != 9 and len(bra_id) != 3:
        header = {
            'name': location_service.name(),
            'gdp': location_service.gdp(),
            'population': location_service.population(),
            'gdp_per_capita': location_service.gdp() / location_service.population(),
            'bg_class_image': background_image,
            'year': location_service.year()
        }
    else:
        header = {
            'name': location_service.name(),
            'gdp': location_service.gdp(),
            'life_expectation': location_service.life_expectation(),
            'population': location_service.population(),
            'gdp_per_capita': location_service.gdp_per_capita(),
            'hdi': location_service.hdi(),
            'bg_class_image': background_image,
            'year': location_service.year()
        }

    if eci is not None:
        header['eci'] = eci.eci
        header['eci_year'] = eci.year

    body = {
        'product_year': location_secex_service.year(),
        'main_product_by_export_value': location_secex_service.main_product_by_export_value(),
        'main_product_by_export_value_name': location_secex_service.main_product_by_export_value_name(),
        'main_product_by_import_value': location_secex_service.main_product_by_import_value(),
        'main_product_by_import_value_name': location_secex_service.main_product_by_import_value_name(),
        'total_exports': location_secex_service.total_exports(),
        'total_imports': location_secex_service.total_imports(),
        'less_distance_by_product': location_secex_service.less_distance_by_product(),
        'less_distance_by_product_name': location_secex_service.less_distance_by_product_name(),
        'opportunity_gain_by_product': location_secex_service.opportunity_gain_by_product(),
        'opportunity_gain_by_product_name': location_secex_service.opportunity_gain_by_product_name(),
        'main_destination_by_export_value': location_wld_service.main_destination_by_export_value(),
        'main_destination_by_export_value_name': location_wld_service.main_destination_by_export_value_name(),
        'main_destination_by_import_value': location_wld_service.main_destination_by_import_value(),
        'main_destination_by_import_value_name': location_wld_service.main_destination_by_import_value_name(),
        'secex_year': location_secex_service.year(),

        'industry_year': location_industry_service.year(),
        'main_industry_by_num_jobs': location_industry_service.main_industry_by_num_jobs(),
        'main_industry_by_num_jobs_name': location_industry_service.main_industry_by_num_jobs_name(),
        'main_occupation_by_num_jobs': location_occupation_service.main_occupation_by_num_jobs(),
        'main_occupation_by_num_jobs_name': location_occupation_service.main_occupation_by_num_jobs_name(),
        'avg_wage': location_jobs_service.avg_wage(),
        'wage': location_jobs_service.wage(),
        'total_jobs': location_jobs_service.total_jobs(),
        'rais_year': location_jobs_service.year(),

        'less_distance_by_occupation': location_distance_service.less_distance_by_occupation(),
        'less_distance_by_occupation_name': location_distance_service.less_distance_by_occupation_name(),
        'opportunity_gain_by_occupation': location_opp_gain_service.opportunity_gain_by_occupation(),
        'opportunity_gain_by_occupation_name': location_opp_gain_service.opportunity_gain_by_occupation_name(),

        'university_year': location_university_service.year(),
        'highest_enrolled_by_university': location_university_service.highest_enrolled_by_university(),
        'highest_enrolled_by_university_name': location_university_service.highest_enrolled_by_university_name(),
        'highest_enrolled_by_school': location_school_service.highest_enrolled_by_school(),
        'highest_enrolled_by_school_name': location_school_service.highest_enrolled_by_school_name(),
        'highest_enrolled_by_major': location_major_service.highest_enrolled_by_major(),
        'highest_enrolled_by_major_name': location_major_service.highest_enrolled_by_major_name(),
        'major_year': location_major_service.year(),
        'highest_enrolled_by_basic_course': location_basic_course_service.highest_enrolled_by_basic_course(),
        'highest_enrolled_by_basic_course_name': location_basic_course_service.highest_enrolled_by_basic_course_name(),
        'basic_course_year': location_basic_course_service.year()
    }

    if len(bra_id) == 9:
        profile = {
            'number_of_municipalities': location_service.number_of_locations(len(bra_id)),
            'bra_id': bra_id,
            'state_name': location_service.location_name(3),
            'mesoregion_name': location_service.location_name(5),
            'gdp_rank': location_gdp_rankings_service.gdp_rank(),
            'area': Decimal(location_service.area())
        }
    elif len(bra_id) == 7:
        profile = {
            'number_of_microregions': location_service.number_of_locations(len(bra_id)),
            'bra_id': bra_id,
            'state_name': location_service.location_name(3),
            'mesoregion_name': location_service.location_name(5),
            'number_of_municipalities': location_service.number_of_municipalities()
        }
    elif len(bra_id) == 5:
        profile = {
            'number_of_mesoregions': location_service.number_of_locations(len(bra_id)),
            'bra_id': bra_id,
            'state_name': location_service.location_name(3),
            'eci_rank': location_eci_rankings_service.eci_rank()
        }
    elif len(bra_id) == 1:
        profile = {
            'number_of_regions': location_service.number_of_locations(len(bra_id)),
            'bra_id': bra_id,
            'gdp_pc_rank': location_gdp_pc_rankings_service.gdp_pc_rank(),
            'pop_rank': location_pop_rankings_service.pop_rank(),
            'region_states': location_service.states_in_a_region()
        }
    else:
        profile = {
            'number_of_states': location_service.number_of_locations(len(bra_id)),
            'region_name': location_service.location_name(1),
            'number_of_municipalities': location_service.number_of_locations(9),
            'pop_rank': location_pop_rankings_service.pop_rank(),
            'area_rank': location_area_rankings_service.area_rank(),
            'neighbors': location_service.neighbors(),
            'municipality_rank': location_municipality_rankings_service.municipality_rank()
        }

    if body['total_exports'] is None and body['total_imports'] is None and body['total_jobs'] is None and \
            body['highest_enrolled_by_university'] is None and body['highest_enrolled_by_basic_course'] is None and \
            body['highest_enrolled_by_major'] is None:
            abort(404)

    if tab not in tabs:
        abort(404)

    if menu and menu not in tabs[tab]:
        abort(404)

    else:
        return render_template('location/index.html',
                            header=header, body=body, profile=profile, location=location, is_municipality=is_municipality, tab=tab, graph=graph, id_ibge=id_ibge)
