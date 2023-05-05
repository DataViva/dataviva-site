# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request, abort
from dataviva.apps.general.views import get_locale
from dataviva.api.secex.services import Product as ProductService
from dataviva.api.secex.services import ProductTradePartners as ProductTradePartnersService
from dataviva.api.secex.services import ProductMunicipalities as ProductMunicipalitiesService
from dataviva.api.secex.services import ProductLocations as ProductLocationsService
from dataviva.api.attrs.models import Bra, Hs
import requests

mod = Blueprint('product', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/product',
                static_folder='static')

def getSecexLatestYear():
    latestSecexYear = "2022"

    response = requests.get(g.api_url + "secex/year")

    if response.status_code == 200:
        data = response.json()
        localData = data['data']
        
        localData.sort(key=lambda x: x[0], reverse=True)
        latestSecexYear = localData[0][0]

    return latestSecexYear

@mod.before_request
def before_request():
    g.page_type = 'category'


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


def location_depth(bra_id):
    locations = {
        1: "region",    #todo
        3: "state",
        5: "mesoregion",
        7: "microregion",
        9: "municipality"
    }

    return locations[len(bra_id)]


def handle_region_bra_id(bra_id):
    return {
        "1": "1",
        "2": "2",
        "3": "5",
        "4": "3",
        "5": "4"
    }[bra_id]


def location_service(depth, location):
    if depth == 'region':
        return handle_region_bra_id(location.id)
    if depth == 'mesoregion':
        return str(location.id_ibge)[:2] + str(location.id_ibge)[-2:]
    if depth == 'microregion':
        return str(location.id_ibge)[:2] + str(location.id_ibge)[-3:]
    else:
        return location.id_ibge


@mod.route('/<product_id>/graphs/<tab>', methods=['POST'])
def graphs(product_id, tab):
    product = Hs.query.filter_by(id=product_id).first_or_404()
    location = Bra.query.filter_by(id=request.args.get('bra_id')).first()

    bra_id = request.args.get('bra_id')
    if not bra_id:
        depth = None
        id_ibge = None
    else:
        depth = location_depth(bra_id)
        id_ibge = location_service(depth, location)
    
    latestSecexYear = getSecexLatestYear()

    return render_template('product/graphs-'+tab+'.html', product=product, location=location, graph=None, id_ibge=id_ibge, latestSecexYear=latestSecexYear)


@mod.route('/<product_id>', defaults={'tab': 'general'})
@mod.route('/<product_id>/<tab>')
def index(product_id, tab):
    product = Hs.query.filter_by(id=product_id).first_or_404()
    location = Bra.query.filter_by(id=request.args.get('bra_id')).first()
    is_municipality = location and len(location.id) == 9

    menu = request.args.get('menu')
    url = request.args.get('url')

    bra_id = request.args.get('bra_id')
    bra_id = bra_id if bra_id != 'all' else None
    if not bra_id:
        depth = None
        id_ibge = None
    else:
        depth = location_depth(bra_id)
        id_ibge = location_service(depth, location)

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
        url_prefix = menu.split('-')[-1] + '/' if menu and menu.startswith('new-api-') else 'embed/'
        graph['url'] = url_prefix + url

    tabs = {
        'general': [],
        'opportunities': [
            'economic-opportunities-rings',
            'new-api-economic-opportunities-rings'
        ],
        'trade-partner': [
            'trade-balance-product-line',
            'new-api-trade-balance-product-line',
            'exports-destination-tree_map',
            'new-api-exports-destination-tree_map',
            'new-api-exports-destination-line',
            'new-api-exports-port-line',
            'new-api-exports-port-bar',
            'new-api-exports-port-tree_map',
            'new-api-exports-destination-stacked',
            'exports-destination-line',
            'exports-destination-stacked',
            'imports-origin-tree_map',
            'new-api-imports-origin-tree_map',
            'new-api-imports-port-line',
            'new-api-imports-port-bar',
            'new-api-imports-port-tree_map',
            'new-api-imports-origin-stacked',
            'new-api-imports-origin-line',
            'imports-origin-line',
            'imports-origin-stacked',
        ],
    }

    if not is_municipality:
        tabs['trade-partner'] += [
            'exports-municipality-tree_map',
            'new-api-exports-municipality-tree_map',
            'exports-municipality-geo_map',
            'new-api-exports-municipality-geo_map',
            'exports-municipality-stacked',
            'new-api-exports-municipality-stacked',
            'imports-municipality-tree_map',
            'new-api-imports-municipality-tree_map',
            'imports-municipality-geo_map',
            'new-api-imports-municipality-geo_map',
            'imports-municipality-stacked',
            'new-api-imports-municipality-stacked'
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
        body['export_value_growth_in_five_years'] = product_service.export_value_growth_in_five_years()

    header['year'] = product_service.year()
    header['export_value'] = product_service.total_exported()
    header['export_net_weight'] = product_service.unity_weight_export_price()
    header['import_value'] = product_service.total_imported()

    # Get rankings vars, code should be refactored
    from dataviva.api.secex.models import Ymp, Ymbp
    from dataviva import db
    from sqlalchemy.sql.expression import func, desc

    if location:
        secex_query_export = Ymbp.query.filter(
            Ymbp.year == getSecexLatestYear(),
            Ymbp.hs_id_len == len(product.id),
            Ymbp.bra_id == location_id,
            Ymbp.month == 0).order_by(Ymbp.export_val.desc())
        secex_export = secex_query_export.all()

        secex_query_import = Ymbp.query.filter(
            Ymbp.year == getSecexLatestYear(),
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

    if tab not in tabs:
        abort(404)

    if menu and menu not in tabs[tab]:
        abort(404)

    if header['export_value'] is None and header['import_value'] is None:
        abort(404)

    else:
        latestSecexYear = getSecexLatestYear()
        return render_template('product/index.html', 
                               header=header, 
                               body=body, product=product, location=location, is_municipality=is_municipality, tab=tab, graph=graph, id_ibge=id_ibge, latestSecexYear=latestSecexYear)
