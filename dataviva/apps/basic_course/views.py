# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request
from dataviva.apps.general.views import get_locale
from dataviva.api.sc.services import Basic_course, Basic_course_by_location, Basic_course_school, \
    Basic_course_school_by_location, Basic_course_city, Basic_course_city_by_location, Basic_course_by_state
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


@mod.route('/<course_sc_id>')
def index(course_sc_id):

    bra_id = request.args.get('bra_id')

    max_year_query = db.session.query(
        func.max(Ybc_sc.year)).filter_by(course_sc_id=course_sc_id)

    if bra_id:
        sc_service = Basic_course_by_location(
            course_sc_id=course_sc_id, bra_id=bra_id)
        school_service = Basic_course_school_by_location(
            course_sc_id=course_sc_id, bra_id=bra_id)
        city_service = Basic_course_city_by_location(
            course_sc_id=course_sc_id, bra_id=bra_id)
        state_service = Basic_course_by_state(
            course_sc_id=course_sc_id, bra_id=bra_id)

        rank_query = Ybc_sc.query.filter(
            Ybc_sc.year == max_year_query,
            Ybc_sc.course_sc_id == course_sc_id,
            Ybc_sc.bra_id.like(bra_id[:3]+'%'),
            Ybc_sc.bra_id_len == 9).order_by(Ybc_sc.enrolled.desc())

        import pdb; pdb.set_trace()

        rank = rank_query.all()
    else:
        bra_id = ''
        sc_service = Basic_course(course_sc_id=course_sc_id)
        school_service = Basic_course_school(course_sc_id=course_sc_id)
        city_service = Basic_course_city(course_sc_id=course_sc_id)

    header = {
        'course_sc_id': course_sc_id,
        'field_id': course_sc_id[0:2],
        'course_name': sc_service.course_name(),
        'course_classes': sc_service.course_classes(),
        'course_age': sc_service.course_age(),
        'course_enrolled': sc_service.course_enrolled(),
        'course_average_class_size': sc_service.course_average_class_size(),
        'course_year': sc_service.course_year(),
        'school_count': school_service.school_count(),
        'bra_id': bra_id
    }

    if bra_id:
        header.update({'location_name': sc_service.location_name()})

    if len(bra_id) == 1:
        header.update({'location_rank': state_service.location_rank(),
                       'location_enrolled': state_service.location_enrolled()})
    else:
        header.update({'location_rank': city_service.city_name(),
                       'location_enrolled': city_service.city_enrolled(),
                       'state_name': sc_service.state_name()})

    body = {
        'bra_id': bra_id,
        'school_name': school_service.school_name(),
        'school_enrolled': school_service.school_enrolled(),
        'city_name': city_service.city_name(),
        'city_enrolled': city_service.city_enrolled(),
    }

    if bra_id and len(bra_id) == 9:
        for index, maj in enumerate(rank):
            if rank[index].bra_id == bra_id:
                header['rank'] = index+1
                break

    return render_template('basic_course/index.html', header=header, body=body, body_class='perfil-estado')
