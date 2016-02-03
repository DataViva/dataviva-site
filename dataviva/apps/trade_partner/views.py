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
	country = trade_partner_service.main_info()
	trade = trade_partner_service.trade_info()

	return render_template('trade_partner/index.html', body_class='perfil-estado', country=country, trade=trade)