# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale

mod = Blueprint('occupation', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/occupation',
                static_folder='static')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())

dict = {
	'occupation' : 'Engenheiros em Computacao', 
	'texto_perfil':'Engenharia de Computacao e o ramo da engenharia que lida com a realizacao de projeto e construcaoo de computadores e de sistemas que integram hardware e software, viabilizando a producao de novas maquinas e de equipamentos computacionais para serem utilizados em diversos setores.',
	'municipio_por_empregos' : 'Sao Paulo',
	'num_empregos_principal_municipio' : 1.62 ,
	'unidade_empregos_principal_municipio' : 'milhares'
} 

@mod.route('/')
def index():
	return render_template('occupation/index.html', body_class='perfil-estado', dic = dict)#occupation = occupation, texto_perfil = text_perfil_geral, family = True)