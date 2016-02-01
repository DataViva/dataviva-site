# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import Hs, Bra, Wld
from dataviva.api.secex.models import Ymp, Ymbp, Ympw, Ymbpw
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

def get_ymp_max_year_subquery(product_id):
    return db.session.query(func.max(Ymp.year)).filter_by(hs_id=product_id)

def get_pci(product_id, ymp_max_year_subquery):
    ymp_pci_query = Ymp.query.filter(Ymp.hs_id==product_id,
                                     Ymp.year==ymp_max_year_subquery,
                                     Ymp.month==0).limit(1)
    return ymp_pci_query.one().pci


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

def brasil_dest_export(product_id, product, ympw_max_year_subquery):
    ympw_query = Ympw.query.join(Wld).filter(
        Ympw.hs_id==product_id,
        Ympw.year==ympw_max_year_subquery,
        Ympw.wld_id_len==5,
        Ympw.month==0
    ).order_by(desc(Ympw.export_val)).limit(1)

    ympw_wld_data = ympw_query.values(
        Wld.name_pt,
        Ympw.export_val
    )

    for name_pt, export_val in ympw_wld_data:
        product['dest_name_export'] = name_pt
        product['dest_export_value'] = export_val

    return product

def brasil_src_import(product_id, product, ympw_max_year_subquery):
    ympw_query = Ympw.query.join(Wld).filter(
        Ympw.hs_id==product_id,
        Ympw.year==ympw_max_year_subquery,
        Ympw.wld_id_len==5,
        Ympw.month==0
    ).order_by(desc(Ympw.import_val)).limit(1)

    ympw_wld_data = ympw_query.values(
        Wld.name_pt,
        Ympw.import_val
    )

    for name_pt, import_val in ympw_wld_data:
        product['src_name_import'] = name_pt
        product['src_import_value'] = import_val

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
        export_val = export_val or 0
        import_val = import_val or 0
        export_kg = export_kg or 0
        import_kg = import_kg or 0

        product['year'] = year
        product['export_val'] = export_val
        product['import_val'] = import_val
        product['export_kg'] = export_kg
        product['import_kg'] = import_kg
        product['trade_balance'] = export_val - import_val
        
        if export_val == 0:
            product['export_net_weight'] = None
        else:
            product['export_net_weight'] = export_kg / export_val
        
        if import_val == 0:
            product['import_net_weight'] = None
        else:
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

def localidade_dest_export(bra_id, product_id, product, ymbpw_max_year_subquery):
    ymbpw_query = Ymbpw.query.join(Wld).filter(
        Ymbpw.hs_id==product_id,
        Ymbpw.year==ymbpw_max_year_subquery,
        Ymbpw.wld_id_len==5,
        Ymbpw.bra_id.like(str(bra_id)+'%'),
        Ymbpw.month==0
    ).order_by(desc(Ymbpw.export_val)).limit(1)

    ymbpw_wld_data = ymbpw_query.values(
        Wld.name_pt,
        Ymbpw.export_val
    )

    for name_pt, export_val in ymbpw_wld_data:
        product['dest_name_export'] = name_pt
        product['dest_export_value'] = export_val

    return product

def localidade_src_import(bra_id, product_id, product, ymbpw_max_year_subquery):
    ymbpw_query = Ymbpw.query.join(Wld).filter(
        Ymbpw.hs_id==product_id,
        Ymbpw.year==ymbpw_max_year_subquery,
        Ymbpw.wld_id_len==5,
        Ymbpw.bra_id.like(str(bra_id)+'%'),
        Ymbpw.month==0
    ).order_by(desc(Ymbpw.import_val)).limit(1)

    ymbpw_wld_data = ymbpw_query.values(
        Wld.name_pt,
        Ymbpw.import_val
    )

    for name_pt, import_val in ymbpw_wld_data:
        product['src_name_import'] = name_pt
        product['src_import_value'] = import_val

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

    return product

@mod.route('/')
def index():

    #None database fields must be treated to do math operations and templates with no data...
    
    #'SEÇÃO' (depth == 2)
    #'POSIÇÃO' (depth == 6)
    #'BRASIL' (bra_id == None)

    product_id = '052601' #05 #052601 
    bra_id = '2ce020008' #None #4mg #4mg01 #4mg0000 #4mg010206
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

    #Product Name
    name = Hs.query.filter(Hs.id == product_id).first().name()

    if bra_id == None:
        ymbp_max_year_subquery = db.session.query(func.max(Ymbp.year)).filter_by(hs_id=product_id)
        ympw_max_year_subquery = db.session.query(func.max(Ympw.year)).filter_by(hs_id=product_id)

        ymp_max_year_subquery = get_ymp_max_year_subquery(product_id=product_id)
        pci = get_pci(product_id=product_id, ymp_max_year_subquery=ymp_max_year_subquery)

        brasil_posicao_secao(
            bra_id=bra_id, 
            product_id=product_id, 
            product=product, 
            ymp_max_year_subquery=ymp_max_year_subquery, 
            name=name, 
            pci=pci
        )

        brasil_export(
            product_id=product_id,
            product=product,
            ymbp_max_year_subquery=ymbp_max_year_subquery
        )

        brasil_import(
            product_id=product_id,
            product=product,
            ymbp_max_year_subquery=ymbp_max_year_subquery
        )

        brasil_dest_export(
            product_id=product_id,
            product=product,
            ympw_max_year_subquery=ympw_max_year_subquery
        )

        brasil_src_import(
            product_id=product_id,
            product=product,
            ympw_max_year_subquery=ympw_max_year_subquery
        )
    
    else:
        ymbp_max_year_subquery = db.session.query(func.max(Ymbp.year)).filter_by(hs_id=product_id, bra_id=bra_id)
        ymbpw_max_year_subquery = db.session.query(func.max(Ymbpw.year)).filter_by(hs_id=product_id, bra_id=bra_id)

        ymp_max_year_subquery = get_ymp_max_year_subquery(product_id=product_id)
        pci = get_pci(product_id=product_id, ymp_max_year_subquery=ymp_max_year_subquery)

        if len(product_id) == 6:
            localidade_posicao(
                bra_id=bra_id,
                product_id=product_id,
                product=product,
                ymbp_max_year_subquery=ymbp_max_year_subquery,
                name=name,
                pci=pci
            )

        elif len(product_id) == 2:
            localidade_secao(
                bra_id=bra_id,
                product_id=product_id,
                product=product,
                ymbp_max_year_subquery=ymbp_max_year_subquery,
                name=name
            )  

        localidade_dest_export(
            bra_id=bra_id,
            product_id=product_id,
            product=product,
            ymbpw_max_year_subquery=ymbpw_max_year_subquery
        )

        localidade_src_import(
            bra_id=bra_id,
            product_id=product_id,
            product=product,
            ymbpw_max_year_subquery=ymbpw_max_year_subquery
        )

        if len(bra_id) != 9:
            localidade_diff_municipio_export(
                bra_id=bra_id,
                product_id=product_id,
                product=product,
                ymbp_max_year_subquery=ymbp_max_year_subquery
            )

            localidade_diff_municipio_import(
                bra_id=bra_id,
                product_id=product_id,
                product=product,
                ymbp_max_year_subquery=ymbp_max_year_subquery
            )

    return render_template('product/index.html', body_class='perfil-estado', product=product, context=context)
