# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.secex.services import TradePartner, \
    TradePartnerMunicipalities, TradePartnerProducts
from dataviva.api.secex.models import Ymw
from dataviva.api.attrs.models import Wld
from dataviva import db
from sqlalchemy.sql.expression import func, desc

mod = Blueprint('trade_partner', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/trade_partner')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())

@mod.route('/<wld_id>')
def index(wld_id):

    trade_partner_service = TradePartner(wld_id)
    municipalities_service = TradePartnerMunicipalities(wld_id)
    products_service = TradePartnerProducts(wld_id)

    max_year_query = db.session.query(func.max(Ymw.year)).filter_by(wld_id=wld_id)
    export_rank_query = Ymw.query.join(Wld).filter(
        Ymw.month == 0,
        Ymw.year == max_year_query).order_by(Ymw.export_val.desc())

    import_rank_query = Ymw.query.join(Wld).filter(
        Ymw.month == 0,
        Ymw.year == max_year_query).order_by(Ymw.import_val.desc())

    export_rank = export_rank_query.all()
    import_rank = import_rank_query.all()

    header = {
        'name': trade_partner_service.country_name(),
        'year': trade_partner_service.year(),
        'trade_balance': trade_partner_service.trade_balance(),
        'total_exported': trade_partner_service.total_exported(),
        'unity_weight_export_price': trade_partner_service.unity_weight_export_price(),
        'total_imported': trade_partner_service.total_imported(),
        'unity_weight_import_price': trade_partner_service.unity_weight_import_price(),
        'wld_id': wld_id
    }

    body = {
        'municipality_with_more_exports': municipalities_service.municipality_with_more_exports(),
        'highest_export_value': municipalities_service.highest_export_value(),
        'municipality_with_more_imports': municipalities_service.municipality_with_more_imports(),
        'highest_import_value': municipalities_service.highest_import_value(),

        'product_with_more_imports': products_service.product_with_more_imports(),
        'highest_import_value': products_service.highest_import_value(),
        'product_with_more_exports': products_service.product_with_more_exports(),
        'highest_export_value': products_service.highest_export_value(),
        'product_with_highest_balance': products_service.product_with_highest_balance(),
        'highest_balance': products_service.highest_balance(),
        'product_with_lowest_balance': products_service.product_with_lowest_balance(),
        'lowest_balance': products_service.lowest_balance(),
        'world_trade_description': 'World trade description.',
    }

    for index, trp in enumerate(export_rank):
        if export_rank[index].wld_id == 'nausa':
            header['export_rank'] = index
            break

    for index, trp in enumerate(import_rank):
        if import_rank[index].wld_id == 'nausa':
            header['import_rank'] = index
            break

    return render_template('trade_partner/index.html', body_class='perfil-estado', header=header, body=body)
