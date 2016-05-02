# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request
from dataviva.apps.general.views import get_locale
from dataviva.api.secex.services import Product as ProductService
from dataviva.api.secex.services import ProductTradePartners as ProductTradePartnersService
from dataviva.api.secex.services import ProductMunicipalities as ProductMunicipalitiesService
from dataviva.api.secex.services import ProductLocations as ProductLocationsService
from dataviva.api.attrs.models import Bra, Hs

mod = Blueprint('product', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/product',
                static_folder='static')


@mod.before_request
def before_request():
    g.page_type = 'category'


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/<product_id>/graphs/<tab>', methods=['POST'])
def graphs(product_id, tab):
    product = Hs.query.filter_by(id=product_id).first_or_404()
    location = Bra.query.filter_by(id=request.args.get('bra_id')).first()
    return render_template('product/graphs-'+tab+'.html', product=product, location=location)


@mod.route('/<product_id>')
def index(product_id):

    header = {}
    body = {}
    product = Hs.query.filter_by(id=product_id).first_or_404()
    location = Bra.query.filter_by(id=request.args.get('bra_id')).first()
    language = g.locale

    if location:
        location_id = location.id
    else:
        location_id = None

    trade_partners_service = ProductTradePartnersService(
        product_id=product.id, bra_id=location_id)
    municipalities_service = ProductMunicipalitiesService(
        product_id=product.id, bra_id=location_id)

    if len(product.id) == 6:
        product_service = ProductService(product_id=product.id)
        header['pci'] = product_service.product_complexity()

    if location:
        product_service = ProductLocationsService(
            product_id=product.id, bra_id=location_id)

        body[
            'destination_name_export'] = trade_partners_service.destination_with_more_exports()
        body[
            'destination_export_value'] = trade_partners_service.highest_export_value()
        body[
            'origin_name_import'] = trade_partners_service.origin_with_more_imports()
        body[
            'origin_import_value'] = trade_partners_service.highest_import_value()
        body[
            'export_value_growth_in_five_years'] = product_service.export_value_growth_in_five_years()


        if len(product.id) == 6:
            header['rca_wld'] = product_service.rca_wld()
            header['distance_wld'] = product_service.distance_wld()
            header['opportunity_gain_wld'] = product_service.opp_gain_wld()

        if len(location_id) != 9:
            body[
                'municipality_name_export'] = municipalities_service.municipality_with_more_exports()
            body[
                'municipality_state_export'] = municipalities_service.municipality_with_more_exports_state()
            body[
                'municipality_export_value'] = municipalities_service.highest_export_value()
            body[
                'municipality_name_import'] = municipalities_service.municipality_with_more_imports()
            body[
                'municipality_state_import'] = municipalities_service.municipality_with_more_imports_state()
            body[
                'municipality_import_value'] = municipalities_service.highest_import_value()

    else:
        product_service = ProductService(product_id=product.id)

        body[
            'municipality_name_export'] = municipalities_service.municipality_with_more_exports()
        body[
            'municipality_state_export'] = municipalities_service.municipality_with_more_exports_state()
        body[
            'municipality_export_value'] = municipalities_service.highest_export_value()
        body[
            'municipality_name_import'] = municipalities_service.municipality_with_more_imports()
        body[
            'municipality_state_import'] = municipalities_service.municipality_with_more_imports_state()
        body[
            'municipality_import_value'] = municipalities_service.highest_import_value()
        body[
            'destination_name_export'] = trade_partners_service.destination_with_more_exports()
        body[
            'destination_export_value'] = trade_partners_service.highest_export_value()
        body[
            'origin_name_import'] = trade_partners_service.origin_with_more_imports()
        body[
            'origin_import_value'] = trade_partners_service.highest_import_value()
        body['export_value_growth_in_five_years'] = product_service.export_value_growth_in_five_years()

    header['year'] = product_service.year()
    header['trade_balance'] = product_service.trade_balance()
    header['export_value'] = product_service.total_exported()
    header['export_net_weight'] = product_service.unity_weight_export_price()
    header['import_value'] = product_service.total_imported()
    header['import_net_weight'] = product_service.unity_weight_import_price()

    # Get rankings vars, code should be refactored
    from dataviva.api.secex.models import Ymp
    from dataviva import db
    from sqlalchemy.sql.expression import func, desc

    max_year_query = db.session.query(
        func.max(Ymp.year)).filter(Ymp.hs_id == product.id)

    secex_query = Ymp.query.filter(
        Ymp.year == max_year_query,
        Ymp.hs_id_len == len(product.id),
        Ymp.month == 0).order_by(Ymp.export_val.desc())
    secex = secex_query.all()

    for ranking, product_ranking in enumerate(secex):
        if secex[ranking].hs_id == product_id:
            header['export_value_ranking'] = ranking + 1
            break

    secex_query = Ymp.query.filter(
        Ymp.year == max_year_query,
        Ymp.hs_id_len == len(product_id),
        Ymp.month == 0).order_by(Ymp.import_val.desc())
    secex = secex_query.all()

    for ranking, product_ranking in enumerate(secex):
        if secex[ranking].hs_id == product_id:
            header['import_value_ranking'] = ranking + 1
            break

    return render_template('product/index.html', header=header, body=body, product=product, location=location, language=language)
