# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import Hs, Bra
from dataviva.api.secex.models import Ymp, Ymbp
from dataviva import db
from sqlalchemy import func, desc

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


def brasil_posicao_secao(bra_id, product_id, product, ymp_max_year_subquery, name, pci):

    ymp_query = Ymp.query.filter(
        Ymp.hs_id==product_id,
        Ymp.year==ymp_max_year_subquery,
        Ymp.month==0
    ).limit(1)

    ymp_data = ymp_query.values(
        Ymp.year,
        Ymp.export_val,
        Ymp.import_val,
        Ymp.export_kg,
        Ymp.import_kg
    )

    product['name'] = name
    product['pci'] = pci

    for year, export_val, import_val, export_kg, import_kg in ymp_data:
        product['year'] = year
        product['export_val'] = export_val
        product['import_val'] = import_val
        product['export_kg'] = export_kg
        product['import_kg'] = import_kg
        product['trade_balance'] = export_val - import_val
        product['export_net_weight'] = export_kg / export_val
        product['import_net_weight'] = import_kg / import_val

    return product

def localidade_posicao(bra_id, product_id, product, ymbp_max_year_subquery, name, pci):

    ymbp_query = Ymbp.query.filter(
        Ymbp.hs_id==product_id,
        Ymbp.year==ymbp_max_year_subquery,
        Ymbp.bra_id==bra_id,
        Ymbp.month==0
    ).limit(1)

    ymbp_data = ymbp_query.values(
        Ymbp.year,
        Ymbp.export_val,
        Ymbp.import_val,
        Ymbp.export_kg,
        Ymbp.import_kg,
        Ymbp.rca_wld,
        Ymbp.distance_wld,
        Ymbp.opp_gain_wld
    )

    product['name'] = name
    product['pci'] = pci

    for year, export_val, import_val, export_kg, import_kg, rca_wld, distance_wld, opp_gain_wld in ymbp_data:
        product['year'] = year
        product['export_val'] = export_val
        product['import_val'] = import_val
        product['export_kg'] = export_kg
        product['import_kg'] = import_kg
        product['trade_balance'] = export_val - import_val
        product['export_net_weight'] = export_kg / export_val
        product['import_net_weight'] = import_kg / import_val
        product['rca_wld'] = rca_wld
        product['distance_wld'] = distance_wld
        product['opp_gain_wld'] = opp_gain_wld

    return product

def localidade_secao(bra_id, product_id, product, ymbp_max_year_subquery, name):

    ymbp_query = Ymbp.query.filter(
        Ymbp.hs_id==product_id,
        Ymbp.year==ymbp_max_year_subquery,
        Ymbp.bra_id==bra_id,
        Ymbp.month==0
    ).limit(1)

    ymbp_data = ymbp_query.values(
        Ymbp.year,
        Ymbp.export_val,
        Ymbp.import_val,
        Ymbp.export_kg,
        Ymbp.import_kg
    )

    product['name'] = name

    for year, export_val, import_val, export_kg, import_kg in ymbp_data:
        product['year'] = year
        product['export_val'] = export_val
        product['import_val'] = import_val
        product['export_kg'] = export_kg
        product['import_kg'] = import_kg
        product['trade_balance'] = export_val - import_val
        product['export_net_weight'] = export_kg / export_val
        product['import_net_weight'] = import_kg / import_val

    return product

def brasil_export(product_id, product, ymbp_max_year_subquery):

    ymbp_query = Ymbp.query.join(Bra).filter(
        Ymbp.hs_id==product_id,
        Ymbp.year==ymbp_max_year_subquery,
        Ymbp.bra_id_len==9,
        Ymbp.month==0
    ).order_by(desc(Ymbp.export_val)).limit(1)

    ymbp_bra_data = ymbp_query.values(
        Bra.name_pt,
        Ymbp.export_val
    )

    for name_pt, export_val in ymbp_bra_data:
        product['munic_name_export'] = name_pt
        product['munic_export_value'] = export_val

    return product

def localidade_diff_municipio_export(bra_id, product_id, product, ymbp_max_year_subquery):

    ymbp_query = Ymbp.query.join(Bra).filter(
        Ymbp.hs_id==product_id,
        Ymbp.year==ymbp_max_year_subquery,
        Ymbp.bra_id_len==9,
        Ymbp.bra_id.like(str(bra_id)+'%'),
        Ymbp.month==0
    ).order_by(desc(Ymbp.export_val)).limit(1)

    ymbp_bra_data = ymbp_query.values(
        Bra.name_pt,
        Ymbp.export_val
    )

    for name_pt, export_val in ymbp_bra_data:
        product['munic_name_export'] = name_pt
        product['munic_export_value'] = export_val

    return product

def brasil_import(product_id, product, ymbp_max_year_subquery):

    ymbp_query = Ymbp.query.join(Bra).filter(
        Ymbp.hs_id==product_id,
        Ymbp.year==ymbp_max_year_subquery,
        Ymbp.bra_id_len==9,
        Ymbp.month==0
    ).order_by(desc(Ymbp.import_val)).limit(1)

    ymbp_bra_data = ymbp_query.values(
        Bra.name_pt,
        Ymbp.import_val
    )

    for name_pt, import_val in ymbp_bra_data:
        product['munic_name_import'] = name_pt
        product['munic_import_value'] = import_val

    return product

def localidade_diff_municipio_import(bra_id, product_id, product, ymbp_max_year_subquery):

    ymbp_query = Ymbp.query.join(Bra).filter(
        Ymbp.hs_id==product_id,
        Ymbp.year==ymbp_max_year_subquery,
        Ymbp.bra_id_len==9,
        Ymbp.bra_id.like(str(bra_id)+'%'),
        Ymbp.month==0
    ).order_by(desc(Ymbp.import_val)).limit(1)

    ymbp_bra_data = ymbp_query.values(
        Bra.name_pt,
        Ymbp.import_val
    )

    for name_pt, import_val in ymbp_bra_data:
        product['munic_name_import'] = name_pt
        product['munic_import_value'] = import_val



@mod.route('/')
def index():

    context = {
        #vars in index.html
        'background_image':'static/img/bg-profile-location.jpg',
        'portrait':'static/img/mineric_product.jpg',
        'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.',
        #vars in tab-geral.html and tab-comercio-internacional.html
        'main_destination_total_exp': 'Brasil',
        'main_destination_total_exp_value': 1,
        'main_source_total_imp': 'Brasil',
        'main_source_total_imp_value': 1,
        #vars in tab-comercio-internacional.html
        'desc_international_trade': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.',
        #vars in tab-oportunidade-economica.html
        'desc_economic_opp': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.'
    }

    product_id = '05' #052601
    bra_id = '4mg01' #None #'4mg'
    product = {}

    context['bra_id'] = bra_id
    if bra_id: context['bra_id_len'] = len(bra_id)
    context['depth'] = len(product_id)

    '''

    general query's

    '''

    ###### Product Name #####
    name = Hs.query.filter(Hs.id == product_id).first().name()

    ##### Max year Ymp
    ymp_max_year_subquery = db.session.query(func.max(Ymp.year)).filter_by(hs_id=product_id)

    ##### Max year Ymbp
    if bra_id == None:
        ymbp_max_year_subquery = db.session.query(func.max(Ymbp.year)).filter_by(hs_id=product_id)
    else:
        ymbp_max_year_subquery = db.session.query(func.max(Ymbp.year)).filter_by(hs_id=product_id, bra_id=bra_id)
        
    ##### pci Ymp
    ymp_pci_query = Ymp.query.filter(Ymp.hs_id==product_id,
                                     Ymp.year==ymp_max_year_subquery,
                                     Ymp.month==0).limit(1)
    pci = ymp_pci_query.one().pci

    '''

    tab-geral query's

    '''

    ##### 'BRASIL' (bra_id == None) and 'SEÇÃO' (depth == 2) #####
    ##### 'BRASIL' (bra_id == None) and 'POSIÇÃO' (depth == 6) ##### > Show pci
    if bra_id == None and len(product_id) == 2 or len(product_id) == 6:
        brasil_posicao_secao(bra_id=bra_id, product_id=product_id, product=product, ymp_max_year_subquery=ymp_max_year_subquery, 
            name=name, pci=pci)

    ##### 'LOCALIDADE' and 'POSIÇÃO' (depth == 6) #####
    if bra_id != None and len(product_id) == 6:
        localidade_posicao(bra_id=bra_id, product_id=product_id, product=product, ymbp_max_year_subquery=ymbp_max_year_subquery,
           name=name, pci=pci)

    ##### 'LOCALIDADE' and 'SEÇÃO' (depth == 2) #####
    if bra_id != None and len(product_id) == 2:
        localidade_secao(bra_id=bra_id, product_id=product_id, product=product, ymbp_max_year_subquery=ymbp_max_year_subquery,
           name=name)        

    '''

    tab-comercio-internacional query's

    '''

    ##### 'BRASIL' (bra_id == None) #####
    if bra_id == None:
        brasil_export(product_id=product_id, product=product, ymbp_max_year_subquery=ymbp_max_year_subquery)
        brasil_import(product_id=product_id, product=product, ymbp_max_year_subquery=ymbp_max_year_subquery)

    ##### 'LOCALIDADE' (bra_id == None) and 'LOCALIDADE' != 'MUNICIPIO' (len(bra_id) !=9 #####
    if bra_id != None and len(bra_id) != 9:
        localidade_diff_municipio_export(bra_id=bra_id, product_id=product_id, product=product, ymbp_max_year_subquery=ymbp_max_year_subquery)
        localidade_diff_municipio_import(bra_id=bra_id, product_id=product_id, product=product, ymbp_max_year_subquery=ymbp_max_year_subquery)

    return render_template('product/index.html', body_class='perfil-estado', product=product, context=context)
