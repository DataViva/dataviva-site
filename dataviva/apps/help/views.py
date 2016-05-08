# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, jsonify
from dataviva.apps.general.views import get_locale
from models import HelpSubject
from dataviva.apps.embed.models import Crosswalk_oc, Crosswalk_pi


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


@mod.route('/crosswalk-pi/all')
def all_crosswalk_pi():
    result = Crosswalk_pi.query.all()
    product_industry = []
    for row in result:
        product_industry += [(row.hs_id, row.cnae_id)]
    return jsonify(product_industry=product_industry)


@mod.route('/tab-crosswalk-pi')
def crosswalk_pi():
    return render_template('help/tab-crosswalk-pi.html')
