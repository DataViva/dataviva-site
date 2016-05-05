# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request, abort
from dataviva.apps.general.views import get_locale
from dataviva.api.rais.services import Industry, IndustryOccupation, IndustryMunicipality, IndustryByLocation
from dataviva.api.attrs.models import Cnae, Bra


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


@mod.route('/<industry_id>/graphs/<tab>', methods=['POST'])
def graphs(industry_id, tab):
    industry = Cnae.query.filter_by(id=industry_id).first_or_404()
    location = Bra.query.filter_by(id=request.args.get('bra_id')).first()
    return render_template('industry/graphs-'+tab+'.html', industry=industry, location=location)


@mod.route('/<cnae_id>')
def index(cnae_id):

    header = {}
    body = {}

    industry = Cnae.query.filter_by(id=cnae_id).first_or_404()
    location = Bra.query.filter_by(id=request.args.get('bra_id')).first()

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
    header['num_establishments'] = industry_service.num_establishments()
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

    industry_service_num_establishments = Industry(cnae_id=industry.id)
    header['num_establishments_brazil'] = industry_service_num_establishments.num_establishments()
    header['year'] = industry_service.get_year()

    rais_max_year = db.session.query(func.max(Yi.year)).first()[0]

    if header['num_jobs'] is None or rais_max_year != header['year']:
        abort(404)
    else:
        return render_template('industry/index.html', header=header, body=body, industry=industry, location=location)
