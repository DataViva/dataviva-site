# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import Wld, Bra, Hs
from dataviva.api.secex.models import Ymw, Ymbw, Ympw
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
	ymbw_max_year = db.session.query(func.max(Ymbw.year)).filter_by(wld_id=wld_id)

	ymw_query = Ymw.query.join(Wld).filter(
		Ymw.wld_id == wld_id,
		Ymw.month == 0,
		Ymw.year == ymw_max_year)

	ymbw_county_export_query = Ymbw.query.join(Bra).filter(
		Ymbw.wld_id == wld_id,
		Ymbw.month == 0,
		Ymbw.year == ymbw_max_year,
		func.length(Ymbw.bra_id) == 9).order_by(desc(Ymbw.export_val)).limit(1)

	ymbw_county_import_query = Ymbw.query.join(Bra).filter(
		Ymbw.wld_id == wld_id,
		Ymbw.month == 0,
		Ymbw.year == ymbw_max_year,
		func.length(Ymbw.bra_id) == 9).order_by(desc(Ymbw.import_val)).limit(1)

	ympw_county_export_query = Ympw.query.join(Hs)

	ymw_data = ymw_query.values(
		Wld.name_pt,
		Ymw.year,
		(Ymw.export_val-Ymw.import_val),
		Ymw.export_val,
		(Ymw.export_kg/Ymw.export_val),
		Ymw.import_val,
		(Ymw.import_kg/Ymw.import_val))

	ymbw_county_export_data = ymbw_county_export_query.values(
		Bra.name_pt,
		Ymbw.export_val)

	ymbw_county_import_data = ymbw_county_import_query.values(
		Bra.name_pt,
		Ymbw.import_val)

	country = {}
	trade = {}

	for name_pt, year, trade_balance, total_exported, unity_weight_export_price, total_imported, unity_weight_import_price in ymw_data:
		country['name'] = name_pt
		country['year'] = year
		country['trade_balance'] = trade_balance
		country['total_exported'] = total_exported
		country['unity_weight_export_price'] = unity_weight_export_price
		country['total_imported'] = total_imported
		country['unity_weight_import_price'] = unity_weight_import_price

	for name_pt, export_val in ymbw_county_export_data:
		trade['leading_export_county'] = name_pt
		trade['leading_export_county_value'] = export_val

	for name_pt, import_val in ymbw_county_import_data:
		trade['leading_import_county'] = name_pt
		trade['leading_import_county_value'] = import_val

	return render_template('trade_partner/index.html', body_class='perfil-estado', country=country, trade=trade)


	