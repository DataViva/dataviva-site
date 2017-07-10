# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request
from dataviva.apps.general.views import get_locale
from dataviva.api.hedu.models import Yc_hedu, Ybc_hedu
from dataviva.api.attrs.models import Bra, Course_hedu
from dataviva.api.hedu.services import Major, MajorUniversities, MajorMunicipalities
from dataviva import db
from sqlalchemy.sql.expression import func

mod = Blueprint('major', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/major',
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


@mod.route('/<course_hedu_id>', defaults={'tab': 'general'})
@mod.route('/<course_hedu_id>/<tab>')
def index(course_hedu_id, tab):
    bra_id = request.args.get('bra_id')
    bra_id = bra_id if bra_id != 'all' else None

    menu = request.args.get('menu')
    url = request.args.get('url')
    graph = {}

    if menu:
        graph['menu'] = menu
    if url:
        url_prefix = menu.split('-')[-1] + '/' if menu and menu.startswith('new-api-') else 'embed/'
        graph['url'] = url_prefix + url

    max_year_query = db.session.query(
        func.max(Yc_hedu.year)).filter_by(course_hedu_id=course_hedu_id)

    if bra_id:
        major_service = Major(course_hedu_id, bra_id)
        universities_service = MajorUniversities(course_hedu_id, bra_id)
        municipalities_service = MajorMunicipalities(course_hedu_id, bra_id)

        rank_query = Ybc_hedu.query.filter(
            Ybc_hedu.year == max_year_query,
            Ybc_hedu.bra_id == bra_id,
            func.length(Ybc_hedu.course_hedu_id) == len(course_hedu_id))\
            .order_by(Ybc_hedu.enrolled.desc())
    else:
        major_service = Major(course_hedu_id, '')
        universities_service = MajorUniversities(course_hedu_id, '')
        municipalities_service = MajorMunicipalities(course_hedu_id, '')

        rank_query = Yc_hedu.query.filter(
            Yc_hedu.year == max_year_query,
            func.length(Yc_hedu.course_hedu_id) == len(course_hedu_id))\
            .order_by(Yc_hedu.enrolled.desc())

    rank = rank_query.all()
    hedu_max_year = db.session.query(func.max(Yc_hedu.year)).first()[0]

    if not bra_id:
        header = {
            'name': major_service.name(),
            'enrolled': major_service.enrolled(),
            'entrants': major_service.entrants(),
            'graduates': major_service.graduates(),
            'profile': major_service.profile(),
            'year': major_service.year(),
            'field_id': course_hedu_id[:2]
        }
    else:
        header = {
            'name': major_service.name(),
            'enrolled': major_service.enrolled(),
            'entrants': major_service.entrants(),
            'graduates': major_service.graduates(),
            'profile': major_service.profile(),
            'year': major_service.year(),
            'field_id': course_hedu_id[:2],
            'id': course_hedu_id,
            'bra_id': bra_id,
            'location_name': major_service.location_name()
        }

    body = {
        'university_with_more_enrolled': universities_service.university_with_more_enrolled(),
        'highest_enrolled_number_by_university': universities_service.highest_enrolled_number(),
        'municipality_with_more_enrolled': municipalities_service.municipality_with_more_enrolled(),
        'municipality_with_more_enrolled_state': municipalities_service.municipality_with_more_enrolled_state(),
        'highest_enrolled_number_by_municipality': municipalities_service.highest_enrolled_number(),
        'university_with_more_entrants': universities_service.university_with_more_entrants(),
        'highest_entrant_number_by_university': universities_service.highest_entrants_number(),
        'municipality_with_more_entrants': municipalities_service.municipality_with_more_entrants(),
        'municipality_with_more_entrants_state': municipalities_service.municipality_with_more_entrants_state(),
        'highest_entrant_number_by_municipality': municipalities_service.highest_entrants_number(),
        'university_with_more_graduates': universities_service.university_with_more_graduates(),
        'highest_graduate_number_by_university': universities_service.highest_graduates_number(),
        'municipality_with_more_graduates': municipalities_service.municipality_with_more_graduates(),
        'municipality_with_more_graduates_state': municipalities_service.municipality_with_more_graduates_state(),
        'highest_graduate_number_by_municipality': municipalities_service.highest_graduates_number()
    }

    tabs = {
        'general': [],
        'enrollments': [
            'enrollments-university-tree_map',
            'enrollments-municipality-geo_map',
            'enrollments-municipality-stacked',
            'enrollments-municipality-tree_map',
            'enrollments-status-line',
            'new-api-enrollments-status-line',
            'enrollments-shift-stacked',
        ],
    }
    id_ibge =   None
    for index, maj in enumerate(rank):
        if rank[index].course_hedu_id == course_hedu_id:
            header['rank'] = index + 1
            break

    location = Bra.query.filter(Bra.id == bra_id).first()

    if bra_id:
        depth = location_depth(bra_id)
        id_ibge = _location_service(depth, location)
        is_municipality = True if depth == 'municipality' else False

    major = Course_hedu.query.filter(Course_hedu.id == course_hedu_id).first()

    if tab not in tabs:
        abort(404)

    if menu and menu not in tabs[tab]:
        abort(404)

    if header['enrolled'] is None or hedu_max_year != header['year']:
        abort(404)
    else:
        return render_template('major/index.html', header=header, body=body, id_ibge=id_ibge, location=location, major=major, tab=tab, graph=graph)


@mod.route('/<course_hedu_id>/graphs/<tab>', methods=['POST'])
def graphs(course_hedu_id, tab):
    bra = request.args.get('bra_id')
    major = Course_hedu.query.filter_by(id=course_hedu_id).first_or_404()
    location = Bra.query.filter_by(id=bra).first()

    return render_template('major/graphs-'+tab+'.html', major=major, location=location, graph=None)
