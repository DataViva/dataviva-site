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

dic = {
	'occupation' : 'Engenheiros em Computacao', 
	'texto_perfil':'Engenharia de Computacao e o ramo da engenharia que lida com a realizacao de projeto e construcaoo de computadores e de sistemas que integram hardware e software, viabilizando a producao de novas maquinas e de equipamentos computacionais para serem utilizados em diversos setores.',
	'family' : True,


	'municipio_por_empregos' : 'Sao Paulo',
	'num_empregos_principal_municipio' : 1.62 ,
	'unidade_empregos_principal_municipio' : 'milhares',
	'atividade_por_empregos' : 'atividade x',
	'valor_atividade_por_empregos': 1.0,
	'unidade_atividade_por_empregos': 'bilhao',
	'valor_maior_renda_media_mensal': 12.3,
	'unidade_maior_renda_media_mensal': 'bilhoes',
	'atividade_maior_renda': 'Desenvolvimento Sob Encomenda ',
	'valor_atividade_maior_renda' : 990
} 

@mod.route('/')
def index():
	return render_template('occupation/index.html', body_class='perfil-estado', dic = dic)#occupation = occupation, texto_perfil = text_perfil_geral, family = True)