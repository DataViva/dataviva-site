# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.services import Product as AttrsProductService
from dataviva.api.secex.services import Product as SecexProductService
from dataviva.api.secex.services import ProductByLocation as SecexProductByLocationService


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

    #None database fields must be treated to do math operations
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
        'desc_general': 'Sample Text',
        'desc_international_trade': 'Sample Text',
        'desc_economic_opp': 'Sample Text'
    }

    context['bra_id'] = bra_id
    if bra_id:
        context['bra_id_len'] = len(bra_id)
    context['depth'] = len(product_id)

    product = {}

    #dividir entre indicadores header e body
    #implementar heranca para os metodos do service iguais

    attrs_product_service = AttrsProductService(product_id=product_id)
    product['name'] = attrs_product_service.name()

    if bra_id:
        secex_product_service = SecexProductByLocationService(bra_id=bra_id, product_id=product_id)

        product.update(secex_product_service.destination_with_more_exports())
        product.update(secex_product_service.origin_with_more_imports())

        if len(product_id) == 6:
            product['pci'] = secex_product_service.pci()
            product['rca_wld'] = secex_product_service.rca_wld()
            product['distance_wld'] = secex_product_service.distance_wld()
            product['opp_gain_wld'] = secex_product_service.opp_gain_wld()

        if len(bra_id) != 9:
            product.update(secex_product_service.municipality_with_more_exports())
            product.update(secex_product_service.municipality_with_more_imports())

    else:
        secex_product_service = SecexProductService(product_id=product_id)
        product.update(secex_product_service.municipality_with_more_exports())

        product['munic_name_import'] = secex_product_service.municipality_with_more_imports()
        product['munic_import_value'] = secex_product_service.highest_import_value_by_municipality()

        product.update(secex_product_service.destination_with_more_exports())
        product.update(secex_product_service.origin_with_more_imports())

    product['year'] = secex_product_service.year()
    product['trade_balance'] = secex_product_service.trade_balance()
    product['export_val'] = secex_product_service.export_val()
    product['export_net_weight'] = secex_product_service.export_net_weight()
    product['import_val'] = secex_product_service.import_val()
    product['import_net_weight'] = secex_product_service.import_net_weight()

    return render_template('product/index.html', body_class='perfil-estado', product=product, context=context)