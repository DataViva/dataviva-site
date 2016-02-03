# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request
from dataviva.apps.general.views import get_locale
from dataviva.api.secex.services import Product as SecexProductService


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

    #criar o name service na HS
    #verificar local pci
    #verificar as tabelas usadas em cada classe

    if bra_id:
        secex_product_service = SecexProductByLocationService(bra_id=bra_id, product_id=product_id)

        #product.update(secex_product_service.location_destination_with_more_imports())
        #product.update(secex_product_service.location_origin_with_more_imports())

    else:
        secex_product_service = SecexProductService(product_id=product_id)


    product['year'] = secex_product_service.year()
    product['export_val'] = secex_product_service.export_val()
    product['import_val'] = secex_product_service.import_val()
    product['export_kg'] = secex_product_service.export_kg()
    product['import_kg'] = secex_product_service.import_kg()
    product['trade_balance'] = secex_product_service.trade_balance()
    product['export_net_weight'] = secex_product_service.export_net_weight()
    product['import_net_weight'] = secex_product_service.import_net_weight()
    product.update(secex_product_service.brazil_municipality_with_more_exports())
    product.update(secex_product_service.brazil_municipality_with_more_imports())
    product.update(secex_product_service.brazil_destination_with_more_exports())
    product.update(secex_product_service.brazil_origin_with_more_import())
    product.update(secex_product_service.name())
    product.update(secex_product_service.pci())

    #verificar campo year
    #return object pci name

    if bra_id == None:
        product['year'] = secex_product_service.year()
        product['export_val'] = secex_product_service.export_val()
        product['import_val'] = secex_product_service.import_val()
        product['export_kg'] = secex_product_service.export_kg()
        product['import_kg'] = secex_product_service.import_kg()
        product['trade_balance'] = secex_product_service.trade_balance()
        product['export_net_weight'] = secex_product_service.export_net_weight()
        product['import_net_weight'] = secex_product_service.import_net_weight()
        product.update(secex_product_service.brazil_municipality_with_more_exports())
        product.update(secex_product_service.brazil_municipality_with_more_imports())
        product.update(secex_product_service.brazil_destination_with_more_exports())
        product.update(secex_product_service.brazil_origin_with_more_import())

    else:

        if len(product_id) == 6:
            secex_product_service.
            product.update(secex_product_service.location_postion())

        elif len(product_id) == 2:
            product.update(secex_product_service.location_section())

        if len(bra_id) != 9:
            product.update(secex_product_service.location_municipality_with_more_exports())
            product.update(secex_product_service.location_municipality_with_more_imports())

    return render_template('product/index.html', body_class='perfil-estado', product=product, context=context)