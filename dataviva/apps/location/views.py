# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
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

mod = Blueprint('location', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/location',
                static_folder='static')


@mod.before_request
def before_request():
    g.page_type = 'category'


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/<bra_id>/graphs/<tab>', methods=['POST'])
def graphs(bra_id, tab):
    if bra_id == 'all':
        location = Wld.query.filter_by(id='sabra').first()
        location.id = 'all'
    else:
        location = Bra.query.filter_by(id=bra_id).first()
    return render_template('location/graphs-'+tab+'.html', location=location)


@mod.route('/all')
def all():
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
        'main_product_by_export_value': product_service.highest_export_value(),
        'main_product_by_export_value_name': product_service.highest_export_value_name(),
        'main_product_by_import_value': product_service.highest_import_value(),
        'main_product_by_import_value_name': product_service.highest_import_value_name(),
        'total_imports': product_service.all_imported(),
        'total_exports': product_service.all_exported(),
        'all_trade_balance': product_service.all_trade_balance(),

        'main_industry_by_num_jobs': industry_service.main_industry_by_num_jobs(),
        'main_industry_by_num_jobs_name': industry_service.main_industry_by_num_jobs_name(),
        'main_occupation_by_num_jobs': occupation_service.main_occupation_by_num_jobs(),
        'main_occupation_by_num_jobs_name': occupation_service.main_occupation_by_num_jobs_name(),
        'avg_wage': industry_service.avg_wage(),
        'wage': industry_service.all_salary_mass(),
        'total_jobs': industry_service.total_jobs(),


        'highest_enrolled_by_university': university_service.highest_enrolled_by_university(),
        'highest_enrolled_by_university_name': university_service.highest_enrolled_by_university_name(),
        'highest_enrolled_by_major': major_service.highest_enrolled_by_major(),
        'highest_enrolled_by_major_name': major_service.highest_enrolled_by_major_name(),
        'highest_enrolled_by_school': scholar_service.highest_enrolled_by_school(),
        'highest_enrolled_by_school_name': scholar_service.highest_enrolled_by_school_name(),
        'highest_enrolled_by_basic_course': basic_course_service.highest_enrolled_by_basic_course(),
        'highest_enrolled_by_basic_course_name': basic_course_service.highest_enrolled_by_basic_course_name()
    }

    profile = {}

    return render_template('location/index.html', header=header, body=body, profile=profile, location=location)

@mod.route('/<bra_id>')
def index(bra_id):

    location = Bra.query.filter_by(id=bra_id).first_or_404()

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
    location_body_service = LocationBodyService(bra_id=bra_id)
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
    eci = Ymb.query.filter_by(bra_id=bra_id, month=0) \
        .order_by(desc(Ymb.year)).limit(1).first()

    ''' Background Image'''
    if len(bra_id) == 1:
        countys = Bra.query.filter(Bra.id.like(bra_id+'%'), func.length(Bra.id) == 3).all()
        background_image = "bg-"+str(countys[randint(0, len(countys)-1)].id)+"_"+str(randint(1, 2))
    else:
        background_image = "bg-"+location.id[:3]+"_"+str(randint(1, 2))

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

    body = {
        'main_product_by_export_value': location_body_service.main_product_by_export_value(),
        'main_product_by_export_value_name': location_body_service.main_product_by_export_value_name(),
        'main_product_by_import_value': location_body_service.main_product_by_import_value(),
        'main_product_by_import_value_name': location_body_service.main_product_by_import_value_name(),
        'total_exports': location_body_service.total_exports(),
        'total_imports': location_body_service.total_imports(),
        'main_destination_by_export_value': location_wld_service.main_destination_by_export_value(),
        'main_destination_by_export_value_name': location_wld_service.main_destination_by_export_value_name(),
        'main_destination_by_import_value': location_wld_service.main_destination_by_import_value(),
        'main_destination_by_import_value_name': location_wld_service.main_destination_by_import_value_name(),
        'main_industry_by_num_jobs': location_industry_service.main_industry_by_num_jobs(),
        'main_industry_by_num_jobs_name': location_industry_service.main_industry_by_num_jobs_name(),
        'main_occupation_by_num_jobs': location_occupation_service.main_occupation_by_num_jobs(),
        'main_occupation_by_num_jobs_name': location_occupation_service.main_occupation_by_num_jobs_name(),
        'avg_wage': location_jobs_service.avg_wage(),
        'wage': location_jobs_service.wage(),
        'total_jobs': location_jobs_service.total_jobs(),
        'less_distance_by_occupation': location_distance_service.less_distance_by_occupation(),
        'less_distance_by_occupation_name': location_distance_service.less_distance_by_occupation_name(),
        'opportunity_gain_by_occupation': location_opp_gain_service.opportunity_gain_by_occupation(),
        'opportunity_gain_by_occupation_name': location_opp_gain_service.opportunity_gain_by_occupation_name(),
        'less_distance_by_product': location_body_service.less_distance_by_product(),
        'less_distance_by_product_name': location_body_service.less_distance_by_product_name(),
        'opportunity_gain_by_product': location_body_service.opportunity_gain_by_product(),
        'opportunity_gain_by_product_name': location_body_service.opportunity_gain_by_product_name(),
        'highest_enrolled_by_university': location_university_service.highest_enrolled_by_university(),
        'highest_enrolled_by_university_name': location_university_service.highest_enrolled_by_university_name(),
        'highest_enrolled_by_school': location_school_service.highest_enrolled_by_school(),
        'highest_enrolled_by_school_name': location_school_service.highest_enrolled_by_school_name(),
        'highest_enrolled_by_major': location_major_service.highest_enrolled_by_major(),
        'highest_enrolled_by_major_name': location_major_service.highest_enrolled_by_major_name(),
        'highest_enrolled_by_basic_course': location_basic_course_service.highest_enrolled_by_basic_course(),
        'highest_enrolled_by_basic_course_name': location_basic_course_service.highest_enrolled_by_basic_course_name()
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

    return render_template('location/index.html',
                           header=header, body=body, profile=profile, location=location)
