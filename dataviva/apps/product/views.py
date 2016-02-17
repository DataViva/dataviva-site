# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request
from dataviva.apps.general.views import get_locale
from dataviva.api.secex.services import Product as ProductService
from dataviva.api.secex.services import ProductTradePartners as ProductTradePartnersService
from dataviva.api.secex.services import ProductMunicipalities as ProductMunicipalitiesService
from dataviva.api.secex.services import ProductLocations as ProductLocationsService


mod = Blueprint('product', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/product',
                static_folder='static')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/<product_id>')
def index(product_id):

    bra_id = request.args.get('bra_id')

    #None database fields must be treated (/05?bra_id=2ce020008)
    #and templates with no data shall be omitted...

    #Vars to do tests:
    #section (depth == 2)
    #positon (depth == 6)
    #brazil (bra_id == None)
    #product_id = #05 #052601
    #bra_id = #None #4mg #4mg01 #4mg0000 #4mg010206 #2ce020008

    context = {
        'background_image':'static/img/bg-profile-location.jpg',
        'portrait':'static/img/mineric_product.jpg',
        'desc_international_trade': 'Sample Text',
        'desc_economic_opp': 'Sample Text'
    }

    context['bra_id'] = bra_id
    if bra_id:
        context['bra_id_len'] = len(bra_id)
    context['depth'] = len(product_id)

    header = {}
    body = {}

    trade_partners_service = ProductTradePartnersService(product_id=product_id, bra_id=bra_id)
    municipalities_service = ProductMunicipalitiesService(product_id=product_id, bra_id=bra_id)

    if len(product_id) == 6:
            product_service = ProductService(product_id=product_id)
            header['pci'] = product_service.product_complexity()

    if bra_id:
        product_service = ProductLocationsService(product_id=product_id, bra_id=bra_id)

        body['destination_name_export'] = trade_partners_service.destination_with_more_exports()
        body['destination_export_value'] = trade_partners_service.highest_export_value()
        body['origin_name_import'] = trade_partners_service.origin_with_more_imports()
        body['origin_import_value'] = trade_partners_service.highest_import_value()
        body['export_value_growth_in_five_years'] = product_service.export_value_growth_in_five_years()

        if len(product_id) == 6:
            header['rca_wld'] = product_service.rca_wld()
            header['distance_wld'] = product_service.distance_wld()
            header['opp_gain_wld'] = product_service.opp_gain_wld()

        if len(bra_id) != 9:
            body['municipality_name_export'] = municipalities_service.municipality_with_more_exports()
            body['municipality_export_value'] = municipalities_service.highest_export_value()
            body['municipality_name_import'] = municipalities_service.municipality_with_more_imports()
            body['municipality_import_value'] = municipalities_service.highest_import_value()

    else:
        product_service = ProductService(product_id=product_id)

        body['municipality_name_export'] = municipalities_service.municipality_with_more_exports()
        body['municipality_export_value'] = municipalities_service.highest_export_value()
        body['municipality_name_import'] = municipalities_service.municipality_with_more_imports()
        body['municipality_import_value'] = municipalities_service.highest_import_value()
        body['destination_name_export'] = trade_partners_service.destination_with_more_exports()
        body['destination_export_value'] = trade_partners_service.highest_export_value()
        body['origin_name_import'] = trade_partners_service.origin_with_more_imports()
        body['origin_import_value'] = trade_partners_service.highest_import_value()
        body['export_value_growth_in_five_years'] = product_service.export_value_growth_in_five_years()

    header['name'] = product_service.product_name()
    header['year'] = product_service.year()
    header['trade_balance'] = product_service.trade_balance()
    header['export_value'] = product_service.total_exported()
    header['export_net_weight'] = product_service.unity_weight_export_price()
    header['import_value'] = product_service.total_imported()
    header['import_net_weight'] = product_service.unity_weight_import_price()

    return render_template('product/index.html', body_class='perfil-estado', header=header, body=body, context=context)