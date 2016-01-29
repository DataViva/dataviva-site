# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import Course_hedu, University, Bra
from dataviva.api.hedu.models import Yc_hedu, Ybc_hedu, Yuc
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
    yc_max_year_query = db.session.query(func.max(Yc_hedu.year))
    yuc_max_year_query = db.session.query(func.max(Yuc.year))
    ybc_max_year_query = db.session.query(func.max(Ybc_hedu.year))

    yc_query = Yc_hedu.query.join(Course_hedu).filter(
        Yc_hedu.course_hedu_id == course_id,
        Yc_hedu.year == yc_max_year_query
    )

    yuc_enrolled_query = Yuc.query.join(University).filter(
        Yuc.course_hedu_id == course_id,
        Yuc.year == yuc_max_year_query
    ).order_by(desc(Yuc.enrolled)).limit(1)

    ybc_enrolled_query =  Ybc_hedu.query.join(Bra).filter(
        Ybc_hedu.course_hedu_id == course_id,
        Ybc_hedu.year == ybc_max_year_query,
        func.length(Ybc_hedu.bra_id) == 9
    ).order_by(desc(Ybc_hedu.enrolled)).limit(1)

    yuc_entrants_query = Yuc.query.join(University).filter(
        Yuc.course_hedu_id == course_id,
        Yuc.year == yuc_max_year_query
    ).order_by(desc(Yuc.entrants)).limit(1)

    ybc_entrants_query =  Ybc_hedu.query.join(Bra).filter(
        Ybc_hedu.course_hedu_id == course_id,
        Ybc_hedu.year == ybc_max_year_query,
        func.length(Ybc_hedu.bra_id) == 9
    ).order_by(desc(Ybc_hedu.entrants)).limit(1)

    yuc_graduates_query = Yuc.query.join(University).filter(
        Yuc.course_hedu_id == course_id,
        Yuc.year == yuc_max_year_query
    ).order_by(desc(Yuc.graduates)).limit(1)

    ybc_graduates_query =  Ybc_hedu.query.join(Bra).filter(
        Ybc_hedu.course_hedu_id == course_id,
        Ybc_hedu.year == ybc_max_year_query,
        func.length(Ybc_hedu.bra_id) == 9
    ).order_by(desc(Ybc_hedu.graduates)).limit(1)

    yc_data = yc_query.values(
        Course_hedu.name_pt,
        Yc_hedu.year,
        Yc_hedu.enrolled,
        Yc_hedu.entrants,
        Yc_hedu.graduates
    )

    yuc_enrolled_data = yuc_enrolled_query.values(
        University.name_pt,
        Yuc.enrolled
    )

    ybc_enrolled_data = ybc_enrolled_query.values(
        Bra.name_pt,
        Ybc_hedu.enrolled
    )

    yuc_entrants_data = yuc_entrants_query.values(
        University.name_pt,
        Yuc.entrants
    )

    ybc_entrants_data = ybc_entrants_query.values(
        Bra.name_pt,
        Ybc_hedu.entrants
    )

    yuc_graduates_data = yuc_graduates_query.values(
        University.name_pt,
        Yuc.graduates
    )

    ybc_graduates_data = ybc_graduates_query.values(
        Bra.name_pt,
        Ybc_hedu.graduates
    )


    major = {}

    for name_pt, year, enrolled, entrants, graduates in yc_data:
        major['name'] = name_pt
        major['year'] = year
        major['enrolled'] = enrolled
        major['entrants'] = entrants
        major['graduates'] = graduates

    for name_pt, enrolled in yuc_enrolled_data:
        major['enrolled_university'] = name_pt
        major['enrolled_university_data'] = enrolled

    for name_pt, enrolled in ybc_enrolled_data:
        major['enrolled_county'] = name_pt
        major['enrolled_county_data'] = enrolled

    for name_pt, entrants in yuc_entrants_data:
        major['entrants_university'] = name_pt
        major['entrants_university_data'] = entrants

    for name_pt, entrants in ybc_entrants_data:
        major['entrants_county'] = name_pt
        major['entrants_county_data'] = entrants    

    for name_pt, graduates in yuc_graduates_data:
        major['graduates_university'] = name_pt
        major['graduates_university_data'] = graduates

    for name_pt, graduates in ybc_graduates_data:
        major['graduates_county'] = name_pt
        major['graduates_county_data'] = graduates 

    context = {
        'enrollments_profile' : 'Engenharia de Computacao e um curso denominado nota 5 pelo MEC em algumas universidades.',
        'profile' : 'Engenharia de Computacao e um curso denominado nota 5 pelo MEC em algumas universidades.',
        'year' : 2013,
        'main_graduates_university' : 'UFRGS',
        'main_graduates_university_number' : str(15),
        'main_graduates_county' : 'Porto Alegre',
        'main_graduates_county_number' : str(500),
        'logo_name' : 'university-logo',
        'background_name' : 'bg-profile-university'
    }
    return render_template('major/index.html', major=major, body_class='perfil-estado')


