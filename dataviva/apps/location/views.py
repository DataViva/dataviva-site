# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.services import Location as LocationService
from dataviva.api.secex.models import Ymb
from dataviva.api.secex.services import Location as LocationBodyService, LocationWld
from dataviva.api.rais.services import LocationIndustry, LocationOccupation, \
                                       LocationJobs, LocationDistance, LocationOppGain                                       
from sqlalchemy import desc

mod = Blueprint('location', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/location',
                static_folder='static')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/<bra_id>')
def index(bra_id):

    location_service = LocationService(bra_id=bra_id)
    location_wld_service = LocationWld(bra_id=bra_id)
    location_body_service = LocationBodyService(bra_id=bra_id)
    location_industry_service = LocationIndustry(bra_id=bra_id)
    location_occupation_service = LocationOccupation(bra_id=bra_id)
    location_jobs_service = LocationJobs(bra_id=bra_id)
    location_distance_service = LocationDistance(bra_id=bra_id)
    location_opp_gain_service = LocationOppGain(bra_id=bra_id)

    ''' Query básica para SECEX'''
    eci = Ymb.query.filter_by(bra_id=bra_id, month=0) \
        .order_by(desc(Ymb.year)).limit(1).first().eci

    header = {
        'name': location_service.name(),
        'bra_id' : bra_id[:3],
        'gdp': location_service.gdp(),
        'life_expectation': location_service.life_expectation(),
        'population': location_service.population(),
        'gdp_per_capita': location_service.gdp_per_capita(),
        'hdi': location_service.hdi(),
        'eci': eci,
    }

    body = {
        'main_product_by_export_value' : location_body_service.main_product_by_export_value(),
        'main_product_by_export_value_name' : location_body_service.main_product_by_export_value_name(),
        'main_product_by_import_value' : location_body_service.main_product_by_import_value(),
        'main_product_by_import_value_name' : location_body_service.main_product_by_import_value_name(),
        'total_exports' : location_body_service.total_exports(),
        'total_imports' : location_body_service.total_imports(),
        'main_destination_by_export_value' : location_wld_service.main_destination_by_export_value(),
        'main_destination_by_export_value_name' : location_wld_service.main_destination_by_export_value_name(),
        'main_destination_by_import_value' : location_wld_service.main_destination_by_import_value(),
        'main_destination_by_import_value_name' : location_wld_service.main_destination_by_import_value_name(),
        'main_industry_by_num_jobs' : location_industry_service.main_industry_by_num_jobs(),
        'main_industry_by_num_jobs_name' : location_industry_service.main_industry_by_num_jobs_name(),
        'main_occupation_by_num_jobs' : location_occupation_service.main_occupation_by_num_jobs(),
        'main_occupation_by_num_jobs_name' : location_occupation_service.main_occupation_by_num_jobs_name(),
        'avg_wage' : location_jobs_service.avg_wage(),
        'wage' : location_jobs_service.wage(),
        'total_jobs' : location_jobs_service.total_jobs(),
        'less_distance_by_occupation' : location_distance_service.less_distance_by_occupation(),
        'less_distance_by_occupation_name' : location_distance_service.less_distance_by_occupation_name(),
        'biggest_opportunity_gain_by_occupation' : location_opp_gain_service.biggest_opportunity_gain_by_occupation(),
        'biggest_opportunity_gain_by_occupation_name' : location_opp_gain_service.biggest_opportunity_gain_by_occupation_name(),
        'less_distance_by_product' : location_body_service.less_distance_by_product(),
        'less_distance_by_product_name' : location_body_service.less_distance_by_product_name(),
        'biggest_opportunity_gain_by_product' : location_body_service.biggest_opportunity_gain_by_product(),
        'biggest_opportunity_gain_by_product_name' : location_body_service.biggest_opportunity_gain_by_product_name(),
    }

    return render_template('location/index.html',
                           header=header, body=body)
