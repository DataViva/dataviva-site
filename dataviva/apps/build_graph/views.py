# -*- coding: utf-8 -*-
import re
from flask import Blueprint, render_template, g, jsonify, request
from dataviva.apps.general.views import get_locale
from dataviva.apps.embed.models import Build
from sqlalchemy import not_
import hashlib
import json


mod = Blueprint('build_graph', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/build_graph')


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
@mod.route('/<dataset>/<filter0>/<filter1>/<filter2>')
def index(dataset=None, filter0=None, filter1=None, filter2=None):
    ''' 
    URL Tests:
        rais/all/all/all
        rais/4sp090607/i56112/all?view=kCV1oruwCB
        rais/4sp090607/i56112/all?graph=stacked
        rais/4sp090607/i56112/all?view=kCV1oruwCB&graph=stacked
        rais/4sp090607/i56112/all?view=kCV1oruwCB&graph=compare&compare=4rj020212
    '''
    view = request.args.get('view').replace(' ', '+') #Needs to treat '+' in parameters properly
    graph = request.args.get('graph')
    compare = request.args.get('compare')

    cross = {
        'rais'  : ['Rais', 'cnae', 'cbo'], 
        'secex' : ['Secex', 'hs', 'wld'], 
        'hedu'  : ['Higher Education', 'university', 'course_hedu'], 
        'sc'    : ['School Census', '', 'course_sc']
    }

    metadata = {}

    if filter0:
        location = filter0

    if filter1 == 'all':
        cross[dataset][1] = 'all'

    if filter2 == 'all':
        cross[dataset][2] = 'all'

    if dataset:
        metadata['dataset'] = cross[dataset][0]

        if graph == 'compare':
            location = filter0 + '_' + compare
        
        json_request = views(dataset, location, cross[dataset][1], cross[dataset][2])
        json_dict = json.loads(json_request.data)

    if view is not None:
        metadata['view'] = json_dict['views'][view]['name']
        if graph is not None:
            metadata['graph'] = json_dict['views'][view]['graphs'][graph]['name']

    return render_template(
        'build_graph/index.html', dataset=dataset, filter0=filter0, filter1=filter1, filter2=filter2, 
                                    graph=graph, view=view, compare=compare, metadata=metadata)


def parse_filter(filter):
    if filter != 'all':
        return '<%s>' % filter
    else:
        return filter


@mod.route('/views/<dataset>/<bra>/<filter1>/<filter2>')
def views(dataset, bra, filter1, filter2):
    '''/views/secex/hs/wld'''

    build_query = Build.query.filter(
        Build.dataset == dataset,
        Build.filter1 == parse_filter(filter1),
        Build.filter2 == parse_filter(filter2))

    if bra != 'all':
        build_query.filter(not_(Build.bra.like('all')))

    views = {}
    for build in build_query.all():
        if bra:
            build.set_bra(bra)

        if filter1 != 'all':
            build.set_filter1(request.args.get('filter1'))

        if filter2 != 'all':
            build.set_filter2(request.args.get('filter2'))

        title = re.sub(r'\s\(.*\)', r'', build.title())

        id = hashlib.md5(build.slug2_en).digest().encode("base64")[0:10]

        if id not in views:
            views[id] = {
                'id': id,
                'name': title,
                'graphs': {},
            }

        views[id]['graphs'][build.app.type] = {
            'url': build.url(),
            'name': build.app.name()
        }

    return jsonify(views=views)
