# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, jsonify, request
from dataviva.apps.general.views import get_locale
from models import HelpSubject
from dataviva.apps.embed.models import Crosswalk_oc, Crosswalk_pi
from urlparse import urlparse


mod = Blueprint('help', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/help')


@mod.before_request
def before_request():
    g.page_type = mod.name


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/')
def index():
    subjects = HelpSubject.query.all()
    return render_template('help/index.html', subjects=subjects)


@mod.route('/admin', methods=['GET'])
def admin():
    subjects = HelpSubject.query.all()
    return render_template('help/admin.html', subjects=subjects)


@mod.route('/subject/all', methods=['GET'])
def all_posts():
    result = HelpSubject.query.all()
    subjects = []
    questions = []
    answers = []
    for row in result:
        for question in row.questions:
            subjects += [(row.id, row.name(), question.description(), question.answer())]
    return jsonify(subjects=subjects)


@mod.route('/tab-brazilian-locations')
def brazilian_locations():
    return render_template('help/tab-brazilian-locations.html')


@mod.route('/tab-products')
def products():
    return render_template('help/tab-products.html')


@mod.route('/tab-basic-courses')
def basic_courses():
    return render_template('help/tab-basic-courses.html')


@mod.route('/tab-industries')
def industries():
    return render_template('help/tab-industries.html')


@mod.route('/tab-occupations')
def occupations():
    return render_template('help/tab-occupations.html')


@mod.route('/tab-trade-partners')
def trade_partners():
    return render_template('help/tab-trade-partners.html')


@mod.route('/crosswalk/pi')
@mod.route('/crosswalk/ip')
@mod.route('/crosswalk/oc')
@mod.route('/crosswalk/co')
def crosswalk():
    url = urlparse(request.url)
    crosswalk_table = url.path.split('/')[-1]

    data = []

    if crosswalk_table == 'pi' or crosswalk_table == 'ip':
        result = Crosswalk_pi.query.all()
        if crosswalk_table == 'pi':
            for row in result:
                data += [(row.hs_id, row.cnae_id)]
        else:
            for row in result:
                data += [(row.cnae_id, row.hs_id)]
    else:
        result = Crosswalk_oc.query.all()
        if crosswalk_table == 'oc':
            for row in result:
                data += [(row.cbo_id, row.course_hedu_id)]
        else:
            for row in result:
                data += [(row.course_hedu_id, row.cbo_id)]

    return jsonify(data=data)


@mod.route('/tab-crosswalk-pi')
def crosswalk_pi():
    return render_template('help/tab-crosswalk-pi.html')


@mod.route('/tab-crosswalk-ip')
def crosswalk_ip():
    return render_template('help/tab-crosswalk-ip.html')


@mod.route('/tab-crosswalk-oc')
def crosswalk_oc():
    return render_template('help/tab-crosswalk-oc.html')


@mod.route('/tab-crosswalk-co')
def crosswalk_co():
    return render_template('help/tab-crosswalk-co.html')
