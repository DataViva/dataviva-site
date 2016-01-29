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
        'num_enrolled_br':10.3,
        'num_enrolled_location':10.3,
        'num_classes_br':6.8,
        'num_classes_location':6.8,
        'num_schools_br':11.3,
        'num_schools_location':11.3,
        'size_avg_classes_br':27.3,
        'size_avg_classes_location':27.3,
        'avg_age_br':12.7,
        'avg_age_location':12.7,
        'school_max_num_enrolled_br':unicode('Colégio Magnum', 'utf8'),
        'school_max_num_enrolled_location':unicode('Colégio Magnum', 'utf8'),
        'value_school_max_num_enrolled_br':2.2,
        'value_school_max_num_enrolled_location':2.2,
        'city_max_num_enrolled_br':unicode('Belo Horizonte', 'utf8'),
        'city_max_num_enrolled_location':unicode('Belo Horizonte', 'utf8'),
        'value_city_max_num_enrolled_br':15,
        'value_city_max_num_enrolled_location':15,
        'year':2014,
        'general_description': unicode('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla tellus magna, consectetur eu convallis sed, malesuada sed ipsum. Integer ligula sapien, ullamcorper id tristique eu, ullamcorper eget eros. Maecenas pretium consectetur tempus. Nam blandit vestibulum justo. Etiam quis dignissim magna, at lacinia enim. Mauris fermentum blandit dui ac pellentesque. Vivamus eget ullamcorper eros. Mauris in feugiat est. Suspendisse venenatis tincidunt tempor. Maecenas ut est id libero rutrum feugiat. Mauris at convallis odio.','utf8'),
        'enrollment_statistics_description': unicode('O Censo Escolar é aplicado anualmente em todo o Brasil, coletando informações sobre diversos aspectos das escolas brasileiras, em especial as matrículas e infraestrutura. Todos os níveis de ensino são envolvidos: ensino infantil, ensino fundamental, ensino médio e EJA.', 'utf8'),        
            }

    return render_template('basic_course/index.html', context=context, body_class='perfil-estado')