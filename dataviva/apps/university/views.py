# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import University, Course_hedu
from dataviva.api.hedu.models import Yu, Yuc
from dataviva import db
from sqlalchemy.sql.expression import func, desc

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
    university_id = '00575'

    ''' Queries que pegam o ano mais recente dos dados '''
    yu_max_year_query = db.session.query(func.max(Yu.year)).filter_by(university_id=university_id)
    yuc_max_year_query = db.session.query(func.max(Yuc.year)).filter_by(university_id=university_id)

    yu_query = Yu.query.join(University).filter(
            Yu.university_id == university_id,
            Yu.year == yu_max_year_query)

    yuc_query = Yuc.query.join(Course_hedu).filter(
            Yuc.university_id == university_id,
            Yuc.year == yuc_max_year_query,
            func.length(Yuc.course_hedu) == 6).order_by(desc(Yuc.enrolled)).limit(1)

    yu_query_data = yu_query.values(
        University.name_pt,
        Yu.enrolled,
        Yu.entrants,
        Yu.graduates,
        Yu.year)

    yuc_query_data = yuc_query.values(
        Course_hedu.name_pt,
        Yuc.enrolled
    )

    university = {}

    for name_pt, enrolled, entrants, graduates, year in yu_query_data:
        university['name'] = name_pt
        university['enrollments'] = enrolled
        university['entrants'] = entrants
        university['graduates'] =  graduates
        university['year'] =  year



    course = {}

    for name_pt, enrolled in yuc_query_data:
        course['name'] = name_pt,
        course['enrollments'] = enrolled

    return render_template('index.html', university=university, course=course, body_class='perfil_estado')


