# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import Hs
from dataviva import db

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
        #vars in index.html
        'background_image':'static/img/bg-profile-location.jpg',
        'name':'Produto',
        'portrait':'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d7748245.803118934!2d-49.94643868147362!3d-18.514293729997753!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xa690a165324289%3A0x112170c9379de7b3!2sMinas+Gerais!5e0!3m2!1spt-BR!2sbr!4v1450524997110',
        #vars in tab-geral.html
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
        #vars in tab-geral.html and tab-comercio-internacional.html
        'main_munic_total_exp': 'Produto',
        'main_munic_total_exp_value': 1,
        'main_munic_total_imp': 'Produto',
        'main_munic_total_imp_value': 1,
        'main_destination_total_exp': 'Brasil',
        'main_destination_total_exp_value': 1,
        'main_source_total_imp': 'Brasil',
        'main_source_total_imp_value': 1,
        #vars in tab-comercio-internacional.html
        'desc_international_trade': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.',
        #vars in tab-oportunidade-economica.html
        'desc_economic_opp': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.',
        #vars to application rules
        'selector_index': 'posicoes',  #'posicoes' or 'secoes' for filter test
        'region': 'Regiao', #'Brazil' for filter test
        'context.bra_id_len': 9
    }

    product_id = '052601'

    product = Hs.query.filter(
        Hs.id == product_id) \
        .first()

    context['name'] = product.name()

    import pdb; pdb.set_trace()
    return render_template('product/index.html', body_class='perfil-estado', context=context)
