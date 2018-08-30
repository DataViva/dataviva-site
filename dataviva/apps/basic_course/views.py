# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request, abort
from dataviva.apps.general.views import get_locale
from dataviva.api.sc.services import Basic_course, Basic_course_by_location, Basic_course_school, \
    Basic_course_school_by_location, Basic_course_city, Basic_course_city_by_location, Basic_course_by_state
from dataviva.api.attrs.models import Bra, Course_sc
from dataviva.api.sc.models import Ybc_sc, Yc_sc
from dataviva import db
from sqlalchemy import func

mod = Blueprint('basic_course', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/basic_course',
                static_folder='static')

def location_depth(bra_id):
    locations = {
        1: "region",
        3: "state",
        5: "mesoregion",
        7: "microregion",
        9: "municipality"
    }

    return locations[len(bra_id)]

def handle_region_bra_id(bra_id):
    return {
        "1": "1",
        "2": "2",
        "3": "5",
        "4": "3",
        "5": "4"
    }[bra_id]


def _location_service(depth, location):
    if depth == 'region':
        return handle_region_bra_id(location.id)
    if depth == 'mesoregion':
        return str(location.id_ibge)[:2] + str(location.id_ibge)[-2:]
    if depth == 'microregion':
        return str(location.id_ibge)[:2] + str(location.id_ibge)[-3:]
    else:
        return location.id_ibge

@mod.before_request
def before_request():
    g.page_type = 'category'


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/<basic_course_id>/graphs/<tab>', methods=['POST'])
def graphs(basic_course_id, tab):
    basic_course = Course_sc.query.filter_by(id=basic_course_id).first_or_404()
    location = Bra.query.filter_by(id=request.args.get('bra_id')).first()
    return render_template('basic_course/graphs-' + tab + '.html', basic_course=basic_course, location=location, graph=None)


@mod.route('/<course_sc_id>', defaults={'tab': 'general'})
@mod.route('/<course_sc_id>/<tab>')
def index(course_sc_id, tab):

    basic_course = Course_sc.query.filter_by(id=course_sc_id).first_or_404()
    bra_id = request.args.get('bra_id')
    bra_id = bra_id if bra_id != 'all' else None

    menu = request.args.get('menu')
    url = request.args.get('url')
    graph = {}

    if menu:
        graph['menu'] = menu
    if url:
        graph['url'] = url

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
            Ybc_sc.bra_id.like(bra_id[:3] + '%'),
            Ybc_sc.bra_id_len == 9).order_by(Ybc_sc.enrolled.desc())

        rank = rank_query.all()
        location = Bra.query.filter_by(id=bra_id).first()

    else:
        bra_id = ''
        sc_service = Basic_course(course_sc_id=course_sc_id)
        school_service = Basic_course_school(course_sc_id=course_sc_id)
        city_service = Basic_course_city(course_sc_id=course_sc_id)
        location = None

    header = {
        'course_enrolled': sc_service.course_enrolled(),
        'course_average_class_size': sc_service.course_average_class_size(),
        'course_year': sc_service.course_year(),
    }

    if bra_id:
        header.update({'state_name': sc_service.state_name()})

    if len(bra_id) == 1:
        header.update({'location_rank': state_service.location_rank(),
                       'location_enrolled': state_service.location_enrolled()})
    else:
        header.update({'location_rank': city_service.city_name(),
                       'location_enrolled': city_service.city_enrolled()})

    body = {
        'city_name': city_service.city_name(),
        'city_state': city_service.city_state(),
        'city_enrolled': city_service.city_enrolled(),
    }

    tabs = {
        'general': [],
        'enrollments': [
            'enrollments-municipality-geo_map',
            'enrollments-municipality-stacked',
            'enrollments-municipality-tree_map',
            'enrollments-school-tree_map',
        ],
    }

    if len(bra_id) == 9:
        for index, basic_course_ranking in enumerate(rank):
            if rank[index].bra_id == bra_id:
                header['rank'] = index + 1
                break

    sc_max_year = db.session.query(func.max(Yc_sc.year)).first()[0]

    id_ibge =   None


    location = Bra.query.filter(Bra.id == bra_id).first()

    if bra_id:
        depth = location_depth(bra_id)
        id_ibge = _location_service(depth, location)
        is_municipality = True if depth == 'municipality' else False

    if tab not in tabs:
        abort(404)

    if menu and menu not in tabs[tab]:
        abort(404)

    if header['course_enrolled'] is None or sc_max_year != header['course_year']:
        abort(404)
    else:
        return render_template('basic_course/index.html', header=header, body=body, body_class='perfil-estado', location=location, id_ibge=id_ibge, basic_course=basic_course, tab=tab, graph=graph)
