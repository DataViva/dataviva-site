# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.hedu.services import Major, EnrolledByUniversity, \
EnrolledByMunicipality, EntrantsByUniversity, EntrantsByMunicipality, \
GraduatesByUniversity, GraduatesByMunicipality

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
    enrolled_by_university = EnrolledByUniversity(course_hedu_id='523E04')
    enrolled_by_municipality = EnrolledByMunicipality(course_hedu_id='523E04')
    entrants_by_university = EntrantsByUniversity(course_hedu_id='523E04')
    entrants_by_municipality = EntrantsByMunicipality(course_hedu_id='523E04')
    graduates_by_university = GraduatesByUniversity(course_hedu_id='523E04')
    graduates_by_municipality = GraduatesByMunicipality(course_hedu_id='523E04')

    major = {
        'name' : major_service.name(),
        'enrolled' : major_service.enrolled(),
        'entrants' : major_service.entrants(),
        'graduates' : major_service.graduates(),
        'profile' : major_service.profile(),
        'year' : major_service.year()
    }

    enrollments = {
        'university_with_more_enrolled' : enrolled_by_university.university_with_more_enrolled(),
        'highest_enrolled_number_by_university' : enrolled_by_university.highest_enrolled_number_by_university(),
        'municipality_with_more_enrolled' : enrolled_by_municipality.municipality_with_more_enrolled(),
        'highest_enrolled_number_by_municipality' : enrolled_by_municipality.highest_enrolled_number_by_municipality(), 
        'university_with_more_entrants' : entrants_by_university.university_with_more_entrants(),
        'highest_entrant_number_by_university' : entrants_by_university.highest_entrant_number_by_university(),
        'municipality_with_more_entrants' : entrants_by_municipality.municipality_with_more_entrants(),
        'highest_entrant_number_by_municipality' : entrants_by_municipality.highest_entrant_number_by_municipality(),
        'university_with_more_graduates' : graduates_by_university.university_with_more_graduates(),
        'highest_graduate_number_by_university' : graduates_by_university.highest_graduate_number_by_university(),
        'municipality_with_more_graduates' : graduates_by_municipality.municipality_with_more_graduates(),
        'highest_graduate_number_by_municipality' : graduates_by_municipality.highest_graduate_number_by_municipality()
    }
    
    return render_template('major/index.html', major=major, enrollments=enrollments, body_class='perfil-estado')


