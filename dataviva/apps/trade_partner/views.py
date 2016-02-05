# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.secex.services import TradePartner, \
    TradePartnerMunicipalities, TradePartnerProducts

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
    municipalities_service = TradePartnerMunicipalities(wld_id=wld_id)
    products_service = TradePartnerProducts(wld_id=wld_id)

    header = {
        'name': trade_partner_service.country_name(),
        'year': trade_partner_service.year(),
        'trade_balance': trade_partner_service.trade_balance(),
        'total_exported': trade_partner_service.total_exported(),
        'unity_weight_export_price': trade_partner_service.unity_weight_export_price(),
        'total_imported': trade_partner_service.total_imported(),
        'unity_weight_import_price': trade_partner_service.unity_weight_import_price()
    }

    body = {
        'municipality_with_more_exports' : municipalities_service.municipality_with_more_exports(),
        'highest_export_value' : municipalities_service.highest_export_value(),
        'municipality_with_more_imports' : municipalities_service.municipality_with_more_imports(),
        'highest_import_value' : municipalities_service.highest_import_value(),

        'product_with_more_imports' : products_service.product_with_more_imports(),
        'highest_import_value' : products_service.highest_import_value(),
        'product_with_more_exports' : products_service.product_with_more_exports(),
        'highest_export_value' : products_service.highest_export_value(),
        'product_with_highest_balance' : products_service.product_with_highest_balance(),
        'highest_balance' : products_service.highest_balance(),
        'product_with_lowest_balance' : products_service.product_with_lowest_balance(),
        'lowest_balance' : products_service.lowest_balance(),
        'world_trade_description' : 'World trade description.',
    }

    return render_template('trade_partner/index.html', body_class='perfil-estado', header=header, body=body)
