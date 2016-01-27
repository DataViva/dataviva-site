# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale

mod = Blueprint('university', __name__,
                template_folder='templates/university',
                url_prefix='/<lang_code>/university',
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
        'university_name' : 'Universidade Federal de Minas Gerais',
        'enrollment_number' : str(33),
        'newcomers_number' : str(3.4),
        'graduates_number' : str(4.02),
        'enrollment_profile' : 'A UFMG teve 33 mil matriculas em 2013.',
        'profile' : 'A UFMG esta localizada no bairro da Pampulha em BH.',
        'year' : 2013,
        'main_enrollment_area' : 'Direito',
        'main_enrollment_number': str(2.28),
        'main_newcomers_area' : 'Medicina',
        'main_newcomers_number' : str(260),
        'main_graduates_area' : 'Administracao',
        'main_graduates_number' : str(50),
        'logo_name' : 'university-logo',
        'background_name' : 'bg-profile-university'
    }
    return render_template('index.html', context=context)


