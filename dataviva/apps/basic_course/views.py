# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import School, Bra
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

    course_sc_id = 'xx006'
    bra_id = '1ac'
    course = {}    
    school = {}
    city = {}

    if bra_id:

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

        school_max_enrolled_query = db.session.query(Ybsc, School).filter(Ybsc.school_id == School.id) \
                                        .filter(Ybsc.course_sc_id == course_sc_id,
                                        Ybsc.year == max_year_subquery,
                                        Ybsc.bra_id == bra_id).order_by(Ybsc.enrolled)

        school_data = school_max_enrolled_query.values(School.name_pt,
                                                        Ybsc.enrolled)

        for name_pt, enrolled in school_data:
            school['name'] = name_pt
            school['enrolled'] = enrolled


        city_max_enrolled_query = db.session.query(Ybc_sc, Bra).filter(Ybc_sc.bra_id == Bra.id) \
                                        .filter(Ybc_sc.course_sc_id == course_sc_id,
                                        Ybc_sc.year == max_year_subquery,
                                        Ybc_sc.bra_id_len == 9,
                                        Ybc_sc.bra_id.like(str(bra_id)+'%')).order_by(Ybc_sc.enrolled)

        city_data = city_max_enrolled_query.values(Bra.name_pt,
                                                        Ybc_sc.enrolled)

        for name_pt, enrolled in city_data:
            city['name'] = name_pt
            city['enrolled'] = enrolled

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

        
        school_max_enrolled_query = db.session.query(Ysc, School).filter(Ysc.school_id == School.id) \
                                        .filter(Ysc.course_sc_id == course_sc_id,
                                        Ysc.year == max_year_subquery).order_by(Ysc.enrolled)

        school['enrolled_count'] = school_max_enrolled_query.first()

        school_data = school_max_enrolled_query.values(School.name_pt,
                                                        Ysc.enrolled)

        for name_pt, enrolled in school_data:
            school['name'] = name_pt
            school['enrolled'] = enrolled


        city_max_enrolled_query = db.session.query(Ybc_sc, Bra).filter(Ybc_sc.bra_id == Bra.id) \
                                        .filter(Ybc_sc.course_sc_id == course_sc_id,
                                        Ybc_sc.year == max_year_subquery,
                                        Ybc_sc.bra_id_len == 9).order_by(Ybc_sc.enrolled)

        city['enrolled_count'] = city_max_enrolled_query.first()

        city_data = city_max_enrolled_query.values(Bra.name_pt,
                                                        Ybc_sc.enrolled)

        for name_pt, enrolled in city_data:
            city['name'] = name_pt
            city['enrolled'] = enrolled

    return render_template('basic_course/index.html', course=course, school=school, city=city, body_class='perfil-estado')