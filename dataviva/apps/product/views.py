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
    context = {
        'name':'Produto',
        'background_image':'Imagem de background',
        'portrait':'Imagem do Produto',
        'trade_balance': 1,
        'total_value_exp': 1,
        'rel_net_weight_tve': 1,
        'total_value_imp': 1,
        'rel_net_weight_tvi': 1,
        'prod_complex_index': 1,
        'rca_international': 1,
        'international_distance': 1,
        'ganho_oportunidade_internacional': 1,
        'year': 9999,
        'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.',
        'main_munic_total_exp': 'Produto',
        'main_munic_total_exp_value': 1,
        'main_munic_total_imp': 'Produto',
        'main_munic_total_imp_value': 1,
        'main_destination_total_exp': 'Brasil',
        'main_destination_total_exp_value': 1,
        'main_source_total_imp': 'Brasil',
        'main_source_total_imp_value': 1,
        'desc_international_trade': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.',
        'desc_economic_opp': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.',
        'selector_index': 'posicoes',  #posicoes ou secoes
        'region': 'Regiao' #Brazil for filter test
    }
    return render_template('product/index.html', body_class='perfil-estado', context=context)
