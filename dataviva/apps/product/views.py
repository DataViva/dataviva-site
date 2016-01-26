# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale

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
        mock_dict = {
        'page_nav1':'Home',
        'page_nav2':'Atividade Economica',
        'page_nav3':'Produto',
        'product':'Produto',
        'background_image':'Imagem de background',
        'product_image':'Imagem do Produto',
        'saldo_da_balanca_comercial': 1,
        'valor_total_exportado': 1,
        'relacao_peso_liquidoVTE': 1,
        'valor_total_importado': 1,
        'relacao_peso_liquidoVTI': 1,
        'indice_complexidade_produto': 1,
        'rca_internacional': 1,
        'distancia_internacional': 1,
        'ganho_oportunidade_internacional': 1,
        'year': 9999,
        'desc': 'Sucinta descricao do produto',
        'principal_produtoVTE': 'Produto',
        'principal_produtoVTE_value': 1,
        'principal_produtoVTI': 'Produto',
        'principal_produtoVTI_value': 1,
        'principal_destinoVTE': 'Brasil',
        'principal_destinoVTE_value': 1,
        'principal_origemVTI': 'Brasil',
        'principal_origemVTI_value': 1,
        'selector_index': 'posicoes',  #posicoes ou secoes
        'region': 'Regiao' #Brazil for filter test
    }
    return render_template('product/index.html', body_class='perfil-estado', data=mock_dict)
