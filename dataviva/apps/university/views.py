# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import University
from dataviva.api.hedu.models import Yu, Yc
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
    yc_max_year_query = db.session.query(func.max(Yc.year)).filter_by(university_id=university_id)

    yu_query = Yu.query.join(University).filter(
            Yu.university_id == university_id,
            Yu.year == yu_max_year_query)

    yu_query_data = yu_query.values(
        University.name_pt,
        Yu.enrolled,
        Yu.entrants,
        Yu.graduates,
        Yu.year).one()

    university_header = {}

    for name_pt, enrolled, entrants, graduates, year in yu_query_data:
        university_header['university_name'] = name_pt
        university_header['enrollment_header_data'] = enrolled
        university_header['entrants_header_data'] = entrants
        university_header['graduates_header_data'] =  graduates
        university_header['year'] =  year

    yc_query = Yc.query.join(University).filter(
            Yc.university_id == university_id,
            Yc.year == yc_max_year_query)

    return render_template('index.html', university_data=university_data, body_class='perfil_estado')


