# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import University
from dataviva.api.hedu.models import Yu
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


    # subquery do ano máximo no hedu_yu
    ''' Query que pega o ano mais recente dos dados '''
    yu_max_year_query = db.session.query(func.max(Yu.year)).filter_by(university_id=university_id)


    yu_query = Yu.query.join(University).filter(
            Yu.university_id == university_id,
            Yu.year == yu_max_year_query)

    print yu_query

    yu_results = yu_query.values(
        University.name_pt,
        Yu.enrolled,
        Yu.entrants,
        Yu.graduates)

    university = []
    for name_pt, enrolled, entrants, graduates in yu_results:
        university +=  (name_pt, enrolled, entrants, graduates)

    context = {
        'university_name' : university[0],
        'year' : 'yu_max_year.maximum'
    }
    return render_template('index.html', context=context, body_class='perfil_estado')


