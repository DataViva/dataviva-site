# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import Ybs, Stat
from dataviva.api.secex.models import Ymb
from dataviva import db
from sqlalchemy import func, desc

mod = Blueprint('location', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/location',
                static_folder='static')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/')
def index():

    bra_id = '4mg'

    # subquery do ano máximo YBS
    ybs_max_year = db.session.query(
        func.max(Ybs.year)).filter_by(bra_id=bra_id)

    ''' Query básica para YBS'''
    ybs_query = Ybs.query.filter_by(bra_id=bra_id).join(Stat)
    # Exemplo de um resultado
    gdp = ybs_query.filter_by(id='gdp') \
        .first().stat_val
    # Exemplo de um resultado usando a subquery
    life_expectancy = ybs_query.filter(
        Stat.id == 'life_exp',
        Ybs.year == ybs_max_year) \
        .first().stat_val
    # Query com todos os filtros no mesmo lugar
    population = Ybs.query.join(Stat).filter(
        Ybs.bra_id == bra_id,
        Ybs.year == ybs_max_year,
        Stat.id == 'pop') \
        .first().stat_val

    ''' Método mais genérico que retorna todos os valores'''
    ybs_list = Ybs.query.join(Stat).filter(
        Ybs.bra_id == bra_id,
        Ybs.year == ybs_max_year) \
        .all()
    # Retirando um valor da lista de objetos YBS
    gdp_pc = filter(lambda x: x.stat_id == 'gdp_pc', ybs_list)[0].stat_val

    ''' Método listando todas as estatisticas, mas definindo colunas'''
    # O que é um generator?
    # https://wiki.python.org/moin/Generators
    # ou
    # http://anandology.com/python-practice-book/iterators.html#generators
    statistics_generator = Ybs.query.join(Stat).filter(
        Ybs.bra_id == bra_id,
        Ybs.year == ybs_max_year) \
        .values(Stat.id,
                Stat.name_pt,
                Ybs.stat_val)

    # Veja como utilizar este generator, iterando para pegar criar um dict
    context = {}

    for id, name_pt, stat_val in statistics_generator:
        context[id] = {
            'name_pt': name_pt,
            'stat_val': stat_val,
        }

    ''' Query básica para SECEX'''
    context['eci'] = Ymb.query.filter_by(bra_id=bra_id, month=0) \
        .order_by(desc(Ymb.year)).limit(1).first().eci

    return render_template('location/index.html', context=context, body_class='perfil-estado')
