# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request
from dataviva.apps.general.views import get_locale 
from dataviva.api.rais.services import Industry, IndustryOccupation, IndustryMunicipality, IndustryByLocation


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


@mod.route('/<cnae_id>')
def index(cnae_id):
 
    bra_id = request.args.get('bra_id')

    industry = {}
    header = {}
    body = {}

    industry = { 
        'background_image':  unicode("'static/img/bg-profile-location.jpg'", 'utf8'),
        'portrait' : unicode('https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d7748245.803118934!2d-49.94643868147362!3d-18.514293729997753!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xa690a165324289%3A0x112170c9379de7b3!2sMinas+Gerais!5e0!3m2!1spt-BR!2sbr!4v1450524997110', 'utf8') ,        
        'text_profile' : unicode('Texto de perfil para Supermercados.', 'utf8'),
        'text_salary_job' : unicode('Texto para Salários e empregos', 'utf8'),
        'text_economic_opportunity' : unicode('Texto para Oportunidades Econômicas', 'utf8'),
    }

    if bra_id == None :
        industry['flag_preview_headers'] = False
        industry['county'] = True # view county where no country
    else : 
        industry['flag_preview_headers'] = True    
     
        if len(bra_id) == 9 : # municipatity
            industry['county'] = False
        else :
            industry['county'] = True    

    if len(cnae_id) == 6 : # class 
        industry['class'] = True
    else : 
        industry['class'] = False


    if bra_id :
        industry_service = IndustryByLocation(bra_id=bra_id, cnae_id=cnae_id)

        header['rca'] = industry_service.rca()
        header['distance'] = industry_service.distance()
        header['opportunity_gain'] = industry_service.opportunity_gain()
    else:
        industry_service = Industry(cnae_id=cnae_id)
  
    industry_occupation_service = IndustryOccupation(bra_id=bra_id, cnae_id=cnae_id)
    industry_municipality_service = IndustryMunicipality(bra_id=bra_id, cnae_id=cnae_id)
   
    header['name'] = industry_service.get_name() 
    header['year'] = industry_service.get_year()
    
    header['average_monthly_income'] = industry_service.average_monthly_income()
    header['salary_mass'] = industry_service.salary_mass()
    header['num_jobs'] = industry_service.num_jobs()
    header['num_establishments'] = industry_service.num_establishments()

    
    
    body['occ_with_more_number_jobs_name'] = industry_occupation_service.occupation_with_more_jobs()
    body['occ_with_more_number_jobs_value'] = industry_occupation_service.highest_number_of_jobs()
    
    
    body['occ_with_more_wage_avg_name'] = industry_occupation_service.occupation_with_biggest_wage_average()
    body['occ_with_more_wage_avg_value'] = industry_occupation_service.biggest_wage_average()
    
    if bra_id == None  or len(bra_id) != 9 :
        body['municipality_with_more_num_jobs_value'] = industry_municipality_service.highest_number_of_jobs()
        body['municipality_with_more_num_jobs_name'] = industry_municipality_service.municipality_with_more_num_jobs()

        body['municipality_with_more_wage_avg_name'] = industry_municipality_service.municipality_with_more_wage_average()
        body['municipality_with_more_wage_avg_value'] = industry_municipality_service.biggest_wage_average()
             
    

    return render_template('industry/index.html', body_class='perfil-estado', header=header, body=body, industry=industry)





