# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request, abort
from dataviva.apps.general.views import get_locale
from dataviva.translations.dictionary import dictionary
import urllib
import json

mod = Blueprint('stacked', __name__,
				template_folder='templates',
				url_prefix='/<lang_code>/stacked',
				static_folder='static')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
	g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
	values.setdefault('lang_code', get_locale())


@mod.route('/<dataset>/<area>')
def index(dataset, area):
	expected_filters = ['product', 'country', 'municipality']
	filters = []

	for filter in expected_filters:
		value = request.args.get(filter)
		if value:
			filters.append((filter, value[2:] if filter == 'product' else value))

	filters = urllib.urlencode(filters)

	group = request.args.get('group') or ''
	prod_type = request.args.get('type') or ''

	params = {}
	for param in ['depths', 'values']:
	    value = request.args.get(param)
	    params[param] = value if value and len(value.split()) > 1 else ''

	return render_template('stacked/index.html',
							dataset=dataset,
							area=area,
							prod_type=prod_type,
							group=group,
							depths=params['depths'],
							values=params['values'],
							filters=filters,
                            dictionary=json.dumps(dictionary()))	