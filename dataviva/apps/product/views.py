# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request, abort
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


@mod.route('/<product_id>', defaults={'tab': 'general'})
@mod.route('/<product_id>/<tab>')
def index(product_id, tab):
    product = Hs.query.filter_by(id=product_id).first_or_404()
    location = Bra.query.filter_by(id=request.args.get('bra_id')).first()
    is_municipality = location and len(location.id) == 9
    import pdb; pdb.set_trace()
    menu = request.args.get('menu')
    url = request.args.get('url')

    if location:
        location_id = location.id
    else:
        location_id = None

    header = {}
    body = {}
    graph = {}

    if menu:
        graph['menu'] = menu
    if url:
        graph['url'] = url

    tabs = {
        'general': [],
        'opportunities': [
            'economic-opportunities-rings'
        ],
        'trade-partner': [
            'trade-balance-product-',
            'exports-destination-tree',
            'exports-destination-line',
            'exports-destination-stacked',
            'imports-origin-tree',
            'imports-origin-line',
            'imports-origin-stacked',
        ],
    }

    if not is_municipality:
        tabs['trade-partner'] += [
            'exports-municipality-tree',
            'exports-municipality-geo',
            'exports-municipality-stacked',
            'imports-municipality-tree',
            'imports-municipality-geo',
            'imports-municipality-stacked',
        ]

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

        if is_municipality:
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
    from dataviva.api.secex.models import Ymp, Ymbp
    from dataviva import db
    from sqlalchemy.sql.expression import func, desc

    if location:
        max_year_query = db.session.query(
        func.max(Ymbp.year)).filter(Ymbp.hs_id == product.id, Ymbp.month == 12)

        secex_query_export = Ymbp.query.filter(
            Ymbp.year == max_year_query,
            Ymbp.hs_id_len == len(product.id),
            Ymbp.bra_id == location_id,
            Ymbp.month == 0).order_by(Ymbp.export_val.desc())
        secex_export = secex_query_export.all()

        secex_query_import = Ymbp.query.filter(
            Ymbp.year == max_year_query,
            Ymbp.hs_id_len == len(product_id),
            Ymbp.bra_id == location_id,
            Ymbp.month == 0).order_by(Ymbp.import_val.desc())
        secex_import = secex_query_import.all()

    else:
        max_year_query = db.session.query(
            func.max(Ymp.year)).filter(Ymp.hs_id == product.id, Ymp.month == 12)

        secex_query_export = Ymp.query.filter(
            Ymp.year == max_year_query,
            Ymp.hs_id_len == len(product.id),
            Ymp.month == 0).order_by(Ymp.export_val.desc())
        secex_export = secex_query_export.all()

        secex_query_import = Ymp.query.filter(
            Ymp.year == max_year_query,
            Ymp.hs_id_len == len(product_id),
            Ymp.month == 0).order_by(Ymp.import_val.desc())
        secex_import = secex_query_import.all()

    for ranking, product_ranking in enumerate(secex_export):
        if secex_export[ranking].hs_id == product_id:
            header['export_value_ranking'] = ranking + 1
            break

    for ranking, product_ranking in enumerate(secex_import):
        if secex_import[ranking].hs_id == product_id:
            header['import_value_ranking'] = ranking + 1
            break

    secex_max_year = db.session.query(func.max(Ymp.year)).filter(
        Ymp.month == 12).first()[0]

    if tab not in tabs:
        abort(404)

    if menu and menu not in tabs[tab]:
        abort(404)

    if header['export_value'] is None and header['import_value'] is None:
        abort(404)
    elif secex_max_year != header['year']:
        abort(404)
    else:
        return render_template('product/index.html', header=header, body=body, product=product, location=location, is_municipality=is_municipality, tab=tab, graph=graph)
