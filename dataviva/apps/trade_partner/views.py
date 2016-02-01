# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import Wld
from dataviva.api.secex.models import Ymw
from dataviva import db
from sqlalchemy.sql.expression import func, desc

mod = Blueprint('trade_partner', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/trade_partner',
                static_folder='static')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())

@mod.route('/')
def index():
	wld_id = 'nausa'

	''' Queries que pegam o ano mais recente dos dados '''
	ymw_max_year = db.session.query(func.max(Ymw.year)).filter_by(wld_id=wld_id)

	ymw_query = Ymw.query.join(Wld).filter(
		Ymw.wld_id == wld_id,
		Ymw.month == 0,
		Ymw.year == ymw_max_year)

	ymw_data = ymw_query.values(
		Wld.name_pt,
		Ymw.year,
		(Ymw.export_val-Ymw.import_val),
		Ymw.export_val,
		(Ymw.export_kg/Ymw.export_val),
		Ymw.import_val,
		(Ymw.import_kg/Ymw.import_val))

	country = {}

	for name_pt, year, trade_balance, total_exported in ymw_data:
		country['name'] = name_pt
		country['year'] = year
		country['trade_balance'] = trade_balance
		country['total_exported'] = total_exported

	return render_template('trade_partner/index.html', body_class='perfil-estado', country=country)


	