# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import Wld, Bra, Hs
from dataviva.api.secex.models import Ymw, Ymbw, Ympw
from dataviva import db
from sqlalchemy.sql.expression import func, desc, asc

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
	ympw_max_year = db.session.query(func.max(Ympw.year)).filter_by(wld_id=wld_id)

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

	ympw_product_export_query = Ympw.query.join(Hs).filter(
		Ympw.wld_id == wld_id,
		Ympw.month == 0,
		Ympw.hs_id_len == 6,
		Ympw.year == ympw_max_year).order_by(desc(Ympw.export_val)).limit(1)

	ympw_product_import_query = Ympw.query.join(Hs).filter(
		Ympw.wld_id == wld_id,
		Ympw.month == 0,
		Ympw.hs_id_len == 6,
		Ympw.year == ympw_max_year).order_by(desc(Ympw.import_val)).limit(1)

	ympw_highest_balance_query = Ympw.query.join(Hs).filter(
		Ympw.wld_id == wld_id,
		Ympw.month == 0,
		Ympw.hs_id_len == 6,
		Ympw.year == ympw_max_year).order_by(desc(Ympw.export_val-Ympw.import_val)).limit(1)

	ympw_lowest_balance_query = Ympw.query.join(Hs).filter(
		Ympw.wld_id == wld_id,
		Ympw.month == 0,
		Ympw.hs_id_len == 6,
		Ympw.year == ympw_max_year).order_by(asc(Ympw.export_val-Ympw.import_val)).limit(1)

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

	ympw_product_export_data = ympw_product_export_query.values(
		Hs.name_pt,
		Ympw.export_val)

	ympw_product_import_data = ympw_product_import_query.values(
		Hs.name_pt,
		Ympw.import_val)

	ympw_highest_balance_data = ympw_highest_balance_query.values(
		Hs.name_pt,
		(Ympw.export_val - Ympw.import_val))

	ympw_lowest_balance_data = ympw_lowest_balance_query.values(
		Hs.name_pt,
		(Ympw.export_val - Ympw.import_val))


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

	for name_pt, export_val in ympw_product_export_data:
		trade['leading_export_product'] = name_pt
		trade['leading_export_product_value'] = export_val

	for name_pt, import_val in ympw_product_import_data:
		trade['leading_import_product'] = name_pt
		trade['leading_import_product_value'] = import_val

	for name_pt, trade_balance in ympw_highest_balance_data:
		trade['highest_product_balance'] = name_pt
		trade['highest_product_balance_value'] = trade_balance

	for name_pt, trade_balance in ympw_lowest_balance_data:
		trade['lowest_product_balance'] = name_pt
		trade['lowest_product_balance_value'] = trade_balance

	return render_template('trade_partner/index.html', body_class='perfil-estado', country=country, trade=trade)


	