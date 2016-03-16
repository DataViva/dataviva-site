# -*- coding: utf8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale


mod = Blueprint('partners', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/partners')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())




@mod.route('/')
def index():
    return render_template('partners/index.html')

@mod.route('/be-a-partner')
def be_a_partner():
    edicts = [ 
    {"link" : ("http://www.fapemig.br/admin/editais/upload/20151215143334-Horizon%202020%20FAPEMIG%20guidelines.pdf").decode("utf-8"), "title" : ("Bolsa de Incentivo ao Pesquisador Público Estadual -  BIPDT.").decode("utf-8")},
    {"link": ("http://www.fapemig.br/admin/editais/upload/20160212152041-Versao%20retificada%20PPM%202016.pdf").decode("utf-8"), "title" : ("Apoio a Núcleo de Inovação Tecnológica").decode("utf-8")}]

    return render_template('partners/be-a-partner.html', edicts=edicts)


@mod.route('/article/<id>', methods=['GET'])
def show(id):
    pass

@mod.route('/article/new', methods=['GET'])
def new():
    pass

@mod.route('/article/<id>/edit', methods=['GET'])
def edit(id):
    pass


@mod.route('/article/new', methods=['POST'])
def create():
    pass


@mod.route('/article/<id>/edit', methods=['POST'])
def update(id):
    pass


@mod.route('/article/<id>/delete', methods=['GET'])
def delete(id):
    pass