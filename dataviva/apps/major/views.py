# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import Course_hedu
from dataviva.api.hedu.models import Yc_hedu
from dataviva import db
from sqlalchemy.sql.expression import func, desc

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
    course_id = '523E04'

    ''' Queries que pegam o ano mais recente dos dados '''
    yc_max_year_query = db.session.query(func.max(Yc_hedu.year)).filter_by(course_hedu_id=course_id)

    yc_query = Yc_hedu.query.join(Course_hedu).filter(
        Yc_hedu.course_hedu_id == course_id,
        Yc_hedu.year == yc_max_year_query)

    yc_data = yc_query.values(
        Course_hedu.name_pt,
        Yc_hedu.year,
        Yc_hedu.enrolled,
        Yc_hedu.entrants,
        Yc_hedu.graduates
    )

    major = {}

    for name_pt, year, enrolled, entrants, graduates in yc_data:
        major['name'] = name_pt
        major['year'] = year
        major['enrolled'] = enrolled
        major['entrants'] = entrants
        major['graduates'] = graduates

    context = {
        'major_name' : 'Engenharia de Computacao',
        'enrollments_number' : str(280),
        'entrants_number' : str(8),
        'graduates_number' : str(3),
        'enrollments_profile' : 'Engenharia de Computacao e um curso denominado nota 5 pelo MEC em algumas universidades.',
        'profile' : 'Engenharia de Computacao e um curso denominado nota 5 pelo MEC em algumas universidades.',
        'year' : 2013,
        'main_enrollments_university' : 'UFRGS',
        'main_enrollments_university_number': str(2),
        'main_enrollments_county' : 'Porto Alegre',
        'main_enrollments_county_number' : str(15),
        'main_entrants_university' : 'CEFET-MG',
        'main_entrants_university_number' : str(40),
        'main_entrants_county' : 'Belo Horizonte',
        'main_entrants_county_number' : str(400),
        'main_graduates_university' : 'UFRGS',
        'main_graduates_university_number' : str(15),
        'main_graduates_county' : 'Porto Alegre',
        'main_graduates_county_number' : str(500),
        'logo_name' : 'university-logo',
        'background_name' : 'bg-profile-university'
    }
    return render_template('major/index.html', major=major, body_class='perfil-estado')


