# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import Course_hedu
from dataviva.api.hedu.models import Yuc
from dataviva.api.hedu.services import University
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
    university_service = University(university_id='00575')

    university = {
        'name' : university_service.name()
        'enrolled' : university_service.enrolled()
        'entrants' : university_service.entrants()
        'graduates' : university_service.graduates()
        'profile' : university_service.profile()
        'year' : university_service.year()
    }

    major = {
        'major_with_more_enrollments' : university_service.major_with_more_enrollments(),
        'major_with_more_entrants' : university_service.major_with_more_entrants(),
        'major_with_more_graduates' : university_service.major_with_more_graduates()
    }
    return render_template('index.html', university=university, major=major, body_class='perfil_estado')


