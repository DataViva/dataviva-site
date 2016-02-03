# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.sc.services import Basic_course as ScBasicCourse
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


@mod.route('/')
def index():

    course_sc_id = '01006'
    bra_id = None

    sc_service = ScBasicCourse(course_sc_id= course_sc_id,bra_id=bra_id)
    basic_course_statistics = sc_service.__statistics__()

    
    return render_template('basic_course/index.html', basic_course_statistics=basic_course_statistics, body_class='perfil-estado')