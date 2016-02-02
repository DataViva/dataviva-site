# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
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


@mod.route('/')
def index():

    #None database fields must be treated to do math operations and templates with no data...
    #section (depth == 2)
    #positon (depth == 6)
    #brazil (bra_id == None)

    product_id = '052601' #05 #052601
    bra_id = None #None #4mg #4mg01 #4mg0000 #4mg010206 #2ce020008
    product = {}

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

    secex_product_service = SecexProductService(bra_id=bra_id, product_id=product_id)
    product.update(secex_product_service.name())
    product.update(secex_product_service.pci())

    if bra_id == None:
        product.update(secex_product_service.brazil_section_position())
        product.update(secex_product_service.brazil_export())
        product.update(secex_product_service.brazil_import())
        product.update(secex_product_service.brazil_dest_export())
        product.update(secex_product_service.brazil_src_import())

    else:
        product.update(secex_product_service.location_dest_export())
        product.update(secex_product_service.location_src_import()) 
        
        if len(product_id) == 6:
            product.update(secex_product_service.location_postion())

        elif len(product_id) == 2:
            product.update(secex_product_service.location_section())

        if len(bra_id) != 9:
            product.update(secex_product_service.location_diff_munic_export())
            product.update(secex_product_service.location_diff_munic_import())

    return render_template('product/index.html', body_class='perfil-estado', product=product, context=context)
