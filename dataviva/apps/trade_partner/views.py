# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.secex.services import TradePartner
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
    trade_partner_service = TradePartner(wld_id='nausa')

    header = trade_partner_service.__country_info__()

    header = {
        'name': trade_partner_service.country_name(),
        'year': trade_partner_service.year(),
        'trade_balance': trade_partner_service.trade_balance(),
        'total_exported': trade_partner_service.total_exported(),
        'unity_weight_export_price': trade_partner_service.unity_weight_export_price(),
        'total_imported': trade_partner_service.total_imported(),
        'unity_weight_import_price': trade_partner_service.unity_weight_import_price()
    }

    trade = {
        'municipality_with_more_exports': trade_partner_service.municipality_with_more_exports(),
        'municipality_with_more_imports': trade_partner_service.municipality_with_more_imports(),
        'product_with_more_exports': trade_partner_service.product_with_more_exports(),
        'product_with_more_imports': trade_partner_service.product_with_more_imports(),
        'product_with_highest_balance': trade_partner_service.product_with_highest_balance(),
        'product_with_lowest_balance': trade_partner_service.product_with_lowest_balance()
    }

    return render_template('trade_partner/index.html', body_class='perfil-estado', header=header, trade=trade)