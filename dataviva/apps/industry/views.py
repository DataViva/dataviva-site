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


@mod.route('/')
def index():
    dic = { 'location' : False ,
            'average_monthly_income' : 371,
            'salary_mass' : 17.9,
            'total_jobs' 6.8, 
            'total_establishments' 6.8,
            'rca_domestic' : 6.8,
            'distance' : 75.3,
            'opportunity_gain' 17.9,

            'occupation_max_number_jobs_name' : 'Ministério de Ferro',
            'occupation_max_number_jobs_value' : 12.2,
            'county_max_number_jobs_name' : 'China',
            'county_max_number_jobs_value' : 8.82,            
            'occupation_max_monthly_income' : 29.3,
            'county_max_monthly_income' : 11        
    }
    return render_template('industry/index.html', body_class='perfil-estado', dic=dic)

