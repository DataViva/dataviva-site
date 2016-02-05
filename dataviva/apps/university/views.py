# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import Course_hedu
from dataviva.api.hedu.models import Yuc
from dataviva.api.hedu.services import University, UniversityMajors
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
    majors_service = UniversityMajors(university_id='00575')

    header = {
        'name' : university_service.name(),
        'enrolled' : university_service.enrolled(),
        'entrants' : university_service.entrants(),
        'graduates' : university_service.graduates(),
        'profile' : university_service.profile(),
        'year' : university_service.year()
    }

    content = {
        'major_with_more_enrollments' : majors_service.major_with_more_enrollments(),
        'highest_enrollment_number_by_major' : majors_service.highest_enrolled_number(),
        'major_with_more_entrants' : majors_service.major_with_more_entrants(),
        'highest_entrant_number_by_major' : majors_service.highest_entrants_number(),
        'major_with_more_graduates' : majors_service.major_with_more_graduates(),
        'highest_graduate_number_by_major' : majors_service.highest_graduates_number()
    }
    return render_template('index.html', header=header, content=content, body_class='perfil_estado')


