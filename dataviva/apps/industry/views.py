# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.rais.services import Industry as RaisIndustryService
from dataviva.api.rais.services import IndustryByLocation as RaisIndustryByLocationService
from dataviva.apps.industry.controler import templates_preview_controler


mod = Blueprint('industry', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/industry',
                static_folder='static')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/')
def index():
 
    bra_id = None #'4mg000000' # Alfredo Vasconcelos
    cnae_id = 'g47113' #supermarkets
    industry = {}

    industry = { 
        'background_image':  unicode("'static/img/bg-profile-location.jpg'", 'utf8'),
        'portrait' : unicode('https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d7748245.803118934!2d-49.94643868147362!3d-18.514293729997753!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xa690a165324289%3A0x112170c9379de7b3!2sMinas+Gerais!5e0!3m2!1spt-BR!2sbr!4v1450524997110', 'utf8') ,        
        'text_profile' : unicode('Texto de perfil para Supermercados.', 'utf8'),
        'text_salary_job' : unicode('Texto para Salários e empregos', 'utf8'),
        'text_economic_opportunity' : unicode('Texto para Oportunidades Econômicas', 'utf8'),
    }


    industry.update(templates_preview_controler(bra_id=bra_id, cnae_id=cnae_id))

    ####EXTRACTY 
    
    rais_industry_service = RaisIndustryService(cnae_id=cnae_id)

    industry['name'] = rais_industry_service.get_name()

    if bra_id == None :
        industry['year'] = rais_industry_service.get_year()
 
        industry['average_monthly_income'] = rais_industry_service.average_monthly_income()
        industry['salary_mass'] = rais_industry_service.salary_mass()
        industry['total_jobs'] = rais_industry_service.num_jobs()
        industry['total_establishments'] = rais_industry_service.num_establishments()

        industry.update(rais_industry_service.get_occ_with_more_number_jobs())
        industry.update(rais_industry_service.get_occ_with_more_wage_avg())
        industry.update(rais_industry_service.get_municipality_with_more_num_jobs())
        industry.update(rais_industry_service.get_municipality_with_more_wage_avg())

    else:
        rais_industry_by_location_service = RaisIndustryByLocationService(bra_id=bra_id, cnae_id=cnae_id)

        industry['year'] = rais_industry_by_location_service.get_year()
            
        industry['average_monthly_income'] = rais_industry_by_location_service.average_monthly_income()
        industry['salary_mass'] = rais_industry_by_location_service.salary_mass()
        industry['total_jobs'] = rais_industry_by_location_service.num_jobs()
        industry['total_establishments'] = rais_industry_by_location_service.num_establishments()
        industry['rca_domestic'] = rais_industry_by_location_service.rca()
        industry['distance'] = rais_industry_by_location_service.distance()
        industry['opportunity_gain'] = rais_industry_by_location_service.opportunity_gain()


        industry.update(rais_industry_by_location_service.get_occ_with_more_number_jobs())
        industry.update(rais_industry_by_location_service.get_occ_with_more_wage_avg())
        if len(bra_id) != 9 :
            industry.update(rais_industry_by_location_service.get_municipality_with_more_num_jobs())
            industry.update(rais_industry_by_location_service.get_municipality_with_more_wage_avg())
        
            
    return render_template('industry/index.html', body_class='perfil-estado', industry=industry)





