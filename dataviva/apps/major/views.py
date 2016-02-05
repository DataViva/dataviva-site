# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.hedu.services import Major, MajorUniversities, MajorMunicipalities

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
    major_service = Major(course_hedu_id='523E04')
    universities_service = MajorUniversities(course_hedu_id='523E04')
    municipalities_service = MajorMunicipalities(course_hedu_id='523E04')

    major = {
        'name' : major_service.name(),
        'enrolled' : major_service.enrolled(),
        'entrants' : major_service.entrants(),
        'graduates' : major_service.graduates(),
        'profile' : major_service.profile(),
        'year' : major_service.year()
    }

    enrollments = {
        'university_with_more_enrolled' : universities_service.university_with_more_enrolled(),
        'highest_enrolled_number_by_university' : universities_service.highest_enrolled_number(),
        'municipality_with_more_enrolled' : municipalities_service.municipality_with_more_enrolled(),
        'highest_enrolled_number_by_municipality' : municipalities_service.highest_enrolled_number(), 
        'university_with_more_entrants' : universities_service.university_with_more_entrants(),
        'highest_entrant_number_by_university' : universities_service.highest_entrants_number(),
        'municipality_with_more_entrants' : municipalities_service.municipality_with_more_entrants(),
        'highest_entrant_number_by_municipality' : municipalities_service.highest_entrants_number(),
        'university_with_more_graduates' : universities_service.university_with_more_graduates(),
        'highest_graduate_number_by_university' : universities_service.highest_graduates_number(),
        'municipality_with_more_graduates' : municipalities_service.municipality_with_more_graduates(),
        'highest_graduate_number_by_municipality' : municipalities_service.highest_graduates_number()
    }
    
    return render_template('major/index.html', major=major, enrollments=enrollments, body_class='perfil-estado')


