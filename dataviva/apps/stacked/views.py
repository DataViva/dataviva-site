# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request, abort
from dataviva.apps.general.views import get_locale
from dataviva.translations.dictionary import dictionary
from dataviva.apps.title.views import get_title
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


@mod.before_request
def before_request():
    g.page_type = mod.name


def location_service(id_ibge):
    locations = {
        1: "region",    #todo
        2: "state",
        4: "mesoregion",
        5: "microregion",
        7: "municipality"
    }

    return (locations[len(id_ibge)], id_ibge)


def product_service(product):
    if len(product) == 2:
        return ('product_section', product[:2])
    elif len(product) == 4:
        return ('product_chapter', product[2:4])
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


def occupation_service(occupation):
    occupations = {
        1: "occupation_group",
        4: "occupation_family"
    }

    return (occupations[len(occupation)], occupation)


def industry_service(industry):
    if len(industry) == 1:
        return ('industry_section', industry)
    elif len(industry) == 3:
        return ('industry_division', industry[1:])
    else:
        return ('industry_class', industry[1:])


@mod.route('/<dataset>/<area>/<value>')
def index(dataset, area, value):
	group = request.args.get('group', '')
	type = request.args.get('type', '')
	depths = request.args.get('depths', '')
	values = request.args.get('values', value)
	title_attrs = {}

	filters = []
	for key, value in request.args.items():
		if key not in ['depths', 'values', 'group', 'filters', 'hierarchy'] and value:
			if key == 'product':
				filters.append(product_service(value))
				title_attrs[product_service(value)[0]] = product_service(value)[1]
			elif key == 'id_ibge':
				filters.append(location_service(value))
				title_attrs[location_service(value)[0]] = location_service(value)[1]
			elif key == 'wld':
				filters.append(wld_service(value))
				title_attrs[wld_service(value)[0]] = wld_service(value)[1]
			elif key == 'occupation':
				filters.append(occupation_service(value))
				title_attrs[occupation_service(value)[0]] = occupation_service(value)[1]
			elif key == 'industry':
				filters.append(industry_service(value))
				title_attrs[industry_service(value)[0]] = industry_service(value)[1]
			else:
				filters.append((key, value))

	filters = urllib.urlencode(filters)

	title, subtitle = get_title(dataset, area, 'stacked', title_attrs)

	return render_template('stacked/index.html',
							dataset=dataset,
							area=area,
							type=type,
							group=group,
							depths=depths,
							values=values,
							title=title or '',
							subtitle=subtitle or '',
							filters=filters,
							dictionary=json.dumps(dictionary()))
