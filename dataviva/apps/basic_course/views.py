# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.sc.services import Basic_course
from dataviva.api.attrs.models import School, Bra, Course_sc
from dataviva.api.sc.models import Yc_sc, Ysc, Ybc_sc, Ybsc
from dataviva import db
from sqlalchemy import func

mod = Blueprint('basic_course', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/basic_course',
                static_folder='static')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/<course_sc_id>/<bra_id>')
def index(course_sc_id, bra_id):

    sc_service = Basic_course(course_sc_id= course_sc_id,bra_id=bra_id)

    header = {

        'course_name' : sc_service.course_name(),
        'course_description' : sc_service.course_description(),
        'course_classes' : sc_service.course_classes(),
        'course_age' : sc_service.course_age(),
        'course_enrolled' : sc_service.course_enrolled(),
        'course_average_class_size' : sc_service.course_average_class_size(),
        'course_year' : sc_service.course_year(),

    }

    body = {
        'schools_count' : sc_service.schools_count(),
        'enrollment_statistics_description' : sc_service.enrollment_statistics_description(),
        'school_name' : sc_service.school_name(),
        'school_enrolled' : sc_service.school_enrolled(),
        'city_name' : sc_service.city_name(),
        'city_enrolled' : sc_service.city_enrolled(),
    }

    return render_template('basic_course/index.html', header=header, body=body, body_class='perfil-estado')