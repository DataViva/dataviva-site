# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import Yuu, Stat
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

    # subquery do ano máximo no Yuu
    yu_max_year = db.session.query(
        func.max(Yuu.year).label('maximum')).filter_by(university_id=university_id).first()

    context = {
        'university_name' : 'UFMG',
        'year' : yu_max_year.maximum
    }
    return render_template('index.html', context=context, body_class='perfil_estado')


