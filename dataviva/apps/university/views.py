# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, abort
from dataviva.apps.general.views import get_locale
from dataviva.api.hedu.services import University, UniversityMajors
from dataviva.api.attrs.models import University as UniversityModel
from dataviva.api.hedu.models import Yu
from dataviva import db
from sqlalchemy.sql.expression import func

mod = Blueprint('university', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/university',
                static_folder='static')


@mod.before_request
def before_request():
    g.page_type = 'category'


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/<university_id>/graphs/<tab>', methods=['POST'])
def graphs(university_id, tab):
    university = UniversityModel.query.filter_by(id=university_id).first_or_404()
    return render_template('university/graphs-'+tab+'.html', university=university)


@mod.route('/<university_id>')
def index(university_id):

    university = UniversityModel.query.filter_by(id=university_id).first_or_404()

    university_service = University(university.id)
    majors_service = UniversityMajors(university.id)

    header = {
        'year': university_service.year(),
        'type': university_service.university_type(),
        'enrolled': university_service.enrolled(),
        'entrants': university_service.entrants(),
        'graduates': university_service.graduates()
    }

    body = {
        'major_with_more_enrollments': majors_service.major_with_more_enrollments(),
        'highest_enrollment_number_by_major': majors_service.highest_enrolled_number(),
        'major_with_more_entrants': majors_service.major_with_more_entrants(),
        'highest_entrant_number_by_major': majors_service.highest_entrants_number(),
        'major_with_more_graduates': majors_service.major_with_more_graduates(),
        'highest_graduate_number_by_major': majors_service.highest_graduates_number(),
        'year': majors_service.year(),
    }

    hedu_max_year = db.session.query(func.max(Yu.year)).first()[0]

    if header['enrolled'] is None or hedu_max_year != body['year']:
        abort(404)
    else:
        return render_template('university/index.html', university=university, header=header, body=body)
