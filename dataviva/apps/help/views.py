# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, jsonify, request
from dataviva.apps.general.views import get_locale
from flask.ext.login import login_required
from dataviva.apps.admin.views import required_roles
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
@login_required
@required_roles(1)
def admin():
    subjects = HelpSubject.query.all()
    return render_template('help/admin.html', subjects=subjects)


@mod.route('/subject/all', methods=['GET'])
def all_posts():
    result = HelpSubject.query.all()
    subjects = []
    for row in result:
        for question in row.questions:
            subjects += [(row.id, row.name(), question.description(), question.answer())]
    return jsonify(subjects=subjects)


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

    aggregated_data = []
    row_index = 0
    data.sort() 
    while row_index < (len(data)):
        category = data[row_index][0]
        crossings = [data[row_index][1]]
        
        if row_index == len(data)-1:
            aggregated_data += [(category, crossings)];
            break;
            
        while category == data[row_index+1][0]:
            crossings.append(data[row_index+1][1])
            row_index += 1

            if row_index == len(data)-1: 
                break;

        aggregated_data += [(category, crossings)];
        row_index += 1
        
    return jsonify(data=aggregated_data)
