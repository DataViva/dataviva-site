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
        'header_num_enrolled':10.3,
        'header_num_classes':6.8,
        'header_num_schools':11.3,
        'header_size_avg_classes':27.3,
        'header_avg_age':12.7,
        'indicador06':unicode('Colégio Magnum', 'utf8'),
        'indicador07':'Belo Horizonte',
        'indicador08':'Escola Municipal',
        'indicador09':'Escola Estadual',
        'label01':'Belo Horizonte',
        'label02': unicode('Colégio Magnum','utf8'),
        'indicadorLabel01':2.2,
        'indicadorLabel02':15,
        'year':2014,
    }
    return render_template('basic_course/index.html', context=context, body_class='perfil-estado')
