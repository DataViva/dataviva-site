# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import School
from dataviva.api.sc.models import Yc_sc, Ysc, Ybc_sc, Ybsc
from dataviva import db
from sqlalchemy import func, desc

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

    course_sc_id = '01006'
    bra_id = '4mg030001'
    course = {}
    enrollment = {}
    school = {}

    if bra_id == '4mg030000':

        max_year_subquery = db.session.query(
            func.max(Ybc_sc.year)).filter_by(course_sc_id=course_sc_id,bra_id=bra_id)

        ybsc_max_year_subquery = db.session.query(
            func.max(Ybsc.year)).filter_by(course_sc_id=course_sc_id,bra_id=bra_id)

        ybc_query = Ybc_sc.query.filter(Ybc_sc.course_sc_id == course_sc_id,
                                      Ybc_sc.year == max_year_subquery,
                                      Ybc_sc.bra_id == bra_id)

        ybsc_query = Ybsc.query.filter(Ybsc.course_sc_id == course_sc_id,
                                     Ybsc.year == ybsc_max_year_subquery,
                                     Ybsc.bra_id == bra_id)

        course['schools_count'] = ybsc_query.count()

        ybc_data = ybc_query.values(Ybc_sc.classes,
                                   Ybc_sc.age,
                                   Ybc_sc.enrolled,
                                   Ybc_sc.year)

        for classes, age, enrolled, year in ybc_data:
            course['classes'] = classes
            course['age'] = age
            course['enrolled'] = enrolled
            course['average_class_size'] = enrolled / classes
            course['year'] = year

    else:

        max_year_subquery = db.session.query(
            func.max(Yc_sc.year)).filter_by(course_sc_id=course_sc_id)

        ysc_max_year_subquery = db.session.query(
            func.max(Ysc.year)).filter_by(course_sc_id=course_sc_id)

        yc_query = Yc_sc.query.filter(Yc_sc.course_sc_id == course_sc_id,
                                      Yc_sc.year == max_year_subquery)

        ysc_query = Ysc.query.filter(Ysc.course_sc_id == course_sc_id,
                                     Ysc.year == ysc_max_year_subquery)

        course['schools_count'] = ysc_query.count()

        yc_data = yc_query.values(Yc_sc.classes,
                                   Yc_sc.age,
                                   Yc_sc.enrolled,
                                   Yc_sc.year)

        for classes, age, enrolled, year in yc_data:
            course['classes'] = classes
            course['age'] = age
            course['enrolled'] = enrolled
            course['average_class_size'] = enrolled / classes
            course['year'] = year

        school_max_enrolled_query = Ysc.query.filter(Ysc.course_sc_id == course_sc_id,
                                      Ysc.year == max_year_subquery).order_by(Ysc.enrolled)

        enrollment['enrolled_count'] = school_max_enrolled_query.first()

        school_data = school_max_enrolled_query.values(Ysc.school_id,
                                                        Ysc.enrolled)

        for school_id, enrolled in school_data:
            enrollment['school_id'] = school_id
            enrollment['enrolled'] = enrolled

        school_name_max_enrolled_query = db.session.query(
            (School.name_pt)).filter_by(id=school_id)

        school['name'] = school_name_max_enrolled_query.one()
        school_name = school_name_max_enrolled_query.values(School.name_pt)

        for name_pt in school_name:
            school['name_pt'] = name_pt

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
        'year':'2015',
        'general_description': unicode('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla tellus magna, consectetur eu convallis sed, malesuada sed ipsum. Integer ligula sapien, ullamcorper id tristique eu, ullamcorper eget eros. Maecenas pretium consectetur tempus. Nam blandit vestibulum justo. Etiam quis dignissim magna, at lacinia enim. Mauris fermentum blandit dui ac pellentesque. Vivamus eget ullamcorper eros. Mauris in feugiat est. Suspendisse venenatis tincidunt tempor. Maecenas ut est id libero rutrum feugiat. Mauris at convallis odio.','utf8'),
        'enrollment_statistics_description': unicode('O Censo Escolar é aplicado anualmente em todo o Brasil, coletando informações sobre diversos aspectos das escolas brasileiras, em especial as matrículas e infraestrutura. Todos os níveis de ensino são envolvidos: ensino infantil, ensino fundamental, ensino médio e EJA.', 'utf8'),
            }

    return render_template('basic_course/index.html', context=context, course=course, enrollment=enrollment, school=school, body_class='perfil-estado')