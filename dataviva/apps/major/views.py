# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale

mod = Blueprint('major', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/major',
                static_folder='static')

@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')

@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())

@mod.route('/')
def index():
    context = {
        'body_class' : 'perfil-estado', 
        'major_name' : 'Engenharia de Computacao',
        'enrollment_number' : str(280),
        'newcomers_number' : str(8),
        'graduates_number' : str(3),
        'enrollment_profile' : 'Engenharia de Computacao e um curso denominado nota 5 pelo MEC em algumas universidades.',
        'profile' : 'Engenharia de Computacao e um curso denominado nota 5 pelo MEC em algumas universidades.',
        'year' : 2013,
        'main_enrollment_university' : 'UFRGS',
        'main_enrollment_university_number': str(2),
        'main_enrollment_county' : 'Porto Alegre',
        'main_enrollment_county_number' : str(15),
        'main_newcomers_university' : 'CEFET-MG',
        'main_newcomers_university_number' : str(40),
        'main_newcomers_county' : 'Belo Horizonte',
        'main_newcomers_county_number' : str(400),
        'main_graduates_university' : 'UFRGS',
        'main_graduates_university_number' : str(15),
        'main_graduates_county' : 'Porto Alegre',
        'main_graduates_county_number' : str(500),
        'logo_name' : 'university-logo',
        'background_name' : 'bg-profile-university'
    }
    return render_template('major/index.html', major_context=context)


