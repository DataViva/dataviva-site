# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.hedu.services import Major

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
    major = major_service.main_info()
    enrollments = major_service.enrollments_info()

    ''' Queries que pegam o ano mais recente dos dados '''

    return render_template('major/index.html', major=major, enrollments=enrollments, body_class='perfil-estado')


