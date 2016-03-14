# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request
from dataviva.apps.general.views import get_locale
from dataviva.api.hedu.models import Yc_hedu, Ybc_hedu
from dataviva.api.hedu.services import Major, MajorUniversities, MajorMunicipalities
from dataviva import db
from sqlalchemy.sql.expression import func

static_folder = '../../static/img/icons/course_hedu'
mod = Blueprint('major', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/major',
                static_folder=static_folder)


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/<course_hedu_id>')
def index(course_hedu_id):
    bra_id = request.args.get('bra_id')

    max_year_query = db.session.query(
        func.max(Yc_hedu.year)).filter_by(course_hedu_id=course_hedu_id)

    if bra_id:
        major_service = Major(course_hedu_id, bra_id)
        universities_service = MajorUniversities(course_hedu_id, bra_id)
        municipalities_service = MajorMunicipalities(course_hedu_id, bra_id)

        rank_query = Ybc_hedu.query.filter(
            Ybc_hedu.year == max_year_query,
            Ybc_hedu.bra_id == bra_id,
            func.length(Ybc_hedu.course_hedu_id) == 6).order_by(Ybc_hedu.course_hedu_id.desc())
    else:
        major_service = Major(course_hedu_id, '')
        universities_service = MajorUniversities(course_hedu_id, '')
        municipalities_service = MajorMunicipalities(course_hedu_id, '')

        rank_query = Yc_hedu.query.filter(
            Yc_hedu.year == max_year_query,
            func.length(Yc_hedu.course_hedu_id) == 6).order_by(Yc_hedu.course_hedu_id.desc())

    rank = rank_query.all()

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
            'bra_id': bra_id,
            'location_name': major_service.location_name()
        }

    body = {
        'university_with_more_enrolled': universities_service.university_with_more_enrolled(),
        'highest_enrolled_number_by_university': universities_service.highest_enrolled_number(),
        'municipality_with_more_enrolled': municipalities_service.municipality_with_more_enrolled(),
        'highest_enrolled_number_by_municipality': municipalities_service.highest_enrolled_number(),
        'university_with_more_entrants': universities_service.university_with_more_entrants(),
        'highest_entrant_number_by_university': universities_service.highest_entrants_number(),
        'municipality_with_more_entrants': municipalities_service.municipality_with_more_entrants(),
        'highest_entrant_number_by_municipality': municipalities_service.highest_entrants_number(),
        'university_with_more_graduates': universities_service.university_with_more_graduates(),
        'highest_graduate_number_by_university': universities_service.highest_graduates_number(),
        'municipality_with_more_graduates': municipalities_service.municipality_with_more_graduates(),
        'highest_graduate_number_by_municipality': municipalities_service.highest_graduates_number()
    }

    for index, maj in enumerate(rank):
        if rank[index].course_hedu_id == course_hedu_id:
            header['rank'] = index
            break

    return render_template('major/index.html', static_folder=static_folder, header=header, body=body)
