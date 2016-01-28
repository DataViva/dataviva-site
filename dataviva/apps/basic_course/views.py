# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale

mod = Blueprint('basic_course', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/basic_course',
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
        'title': unicode('Quinta Série', 'utf8'),
        'indicador1':0,
        'indicador2':1,
        'indicador3':2,
        'indicador4':3,
        'indicador5':4,
    }
    return render_template('basic_course/index.html', context=context, body_class='perfil-estado')
