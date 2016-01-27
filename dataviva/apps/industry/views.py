# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale

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


'''
ano 
imagens 

resolver ascci html
Template css para alinhar headers 

''' 




@mod.route('/')
def index():
    dic = { 'industry_name': 'Supermercados', 
            'location' : True ,
            'class' : True,
            'year' : 2010,
            'background_image':  "'static/img/bg-profile-location.jpg'", 
            'portrait' : 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d7748245.803118934!2d-49.94643868147362!3d-18.514293729997753!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xa690a165324289%3A0x112170c9379de7b3!2sMinas+Gerais!5e0!3m2!1spt-BR!2sbr!4v1450524997110', 
            'average_monthly_income' : 371,
            'salary_mass' : 17.9,
            'total_jobs' : 6.8, 
            'total_establishments' : 6.8,
            'rca_domestic' : 6.8,
            'distance' : 75.3,
            'opportunity_gain' : 17.9,

            'occupation_max_number_jobs_name' : 'Ministerio de Ferro',
            'occupation_max_number_jobs_value' : 12.2,
            'county_max_number_jobs_name' : 'China',
            'county_max_number_jobs_value' : 8.82,            
            'occupation_max_monthly_income' : 29.3,
            'county_max_monthly_income' : 11, 
            'text_profile' : 'Texto de perfil para Supermercados.'       
    }
    return render_template('industry/index.html', body_class='perfil-estado', dic=dic)

