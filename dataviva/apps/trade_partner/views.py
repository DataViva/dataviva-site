# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.secex.services import TradePartner, TradePartnerMunicipalityByExport, \
TradePartnerMunicipalityByImport, TradePartnerProductByImport, TradePartnerProductByExport, \
TradePartnerProductByHighestBalance, TradePartnerProductByLowestBalance
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

    trade_partner_service = TradePartner(wld_id=wld_id)
    municipality_by_export_service = TradePartnerMunicipalityByExport(wld_id=wld_id)
    municipality_by_import_service = TradePartnerMunicipalityByImport(wld_id=wld_id)
    product_by_import_service = TradePartnerProductByImport(wld_id=wld_id)
    product_by_export_service = TradePartnerProductByExport(wld_id=wld_id)
    product_by_highest_balance_service = TradePartnerProductByHighestBalance(wld_id=wld_id)
    product_by_lowest_balance_service = TradePartnerProductByLowestBalance(wld_id=wld_id)

    header = {
        'name': trade_partner_service.country_name(),
        'year': trade_partner_service.year(),
        'trade_balance': trade_partner_service.trade_balance(),
        'total_exported': trade_partner_service.total_exported(),
        'unity_weight_export_price': trade_partner_service.unity_weight_export_price(),
        'total_imported': trade_partner_service.total_imported(),
        'unity_weight_import_price': trade_partner_service.unity_weight_import_price()
    }

    body {
        'municipality_with_more_exports' : municipality_by_export_service.municipality_with_more_exports()
        'highest_export_value_by_municipality' : municipality_by_export_service.highest_export_value_by_municipality()
        'municipality_with_more_imports' : product_by_import_service.municipality_with_more_imports()
        'highest_import_value_by_municipality' : product_by_import_service.highest_import_value_by_municipality()
        'product_with_more_imports' : product_by_import_service.product_with_more_imports()
        'highest_import_value_by_product' : product_by_import_service.highest_import_value_by_product()
        'product_with_more_exports' : product_by_export_service.product_with_more_exports()
        'highest_export_value_by_product' : product_by_export_service.highest_export_value_by_product()
        'product_with_highest_balance' : product_by_highest_balance_service.product_with_highest_balance()
        'highest_balance_by_product' : product_by_highest_balance_service.highest_balance_by_product()
        'product_with_lowest_balance' : product_by_lowest_balance_service.product_with_lowest_balance()
        'lowest_balance_by_product' : product_by_lowest_balance_service.lowest_balance_by_product()
    }

    return render_template('trade_partner/index.html', body_class='perfil-estado', header=header, trade=trade)