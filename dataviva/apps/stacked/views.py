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


def location_service(id_ibge):
	locations = {
		1: "region",
		2: "state",
		4: "mesoregion",
		5: "microregion",
		7: "municipality"
	}

	return (locations[len(id_ibge)], id_ibge)


def product_service(product):
	if len(product) == 2:
		return ('section', product[:2])
	elif len(product) == 4:
		return ('chapter', product[2:4])
	else:
		return ('product', product[2:])


def wld_service(wld):
   if wld.isdigit():
       wld = '%03d' % int(wld)

   wlds = {
       2: "continent",
       3: "country"
   }

   return (wlds[len(wld)], wld)


@mod.route('/<dataset>/<area>/<value>')
def index(dataset, area, value):
	filters = []
	
	for key, value in request.args.items():
		if key not in ['depths', 'values', 'group'] and value:
			if key == 'product':
				filters.append(product_service(value))
			elif key == 'id_ibge':
				filters.append(location_service(value))
			elif key == 'wld':
				filters.append(wld_service(value))
			else:
				filters.append((key, value))

	filters = urllib.urlencode(filters)

	group = request.args.get('group') or ''
	type = request.args.get('type') or ''

	params = {}
	for param in ['depths', 'values']:
		value = request.args.get(param)
		params[param] = value if value and len(value.split()) > 1 else ''


	return render_template('stacked/index.html',
							dataset=dataset,
							area=area,
							type=type,
							group=group,
							depths=params['depths'],
							values=params['values'],
							filters=filters,
							dictionary=json.dumps(dictionary()))	