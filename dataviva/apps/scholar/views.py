# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale

from mock import articles


mod = Blueprint('scholar', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/scholar')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/', methods=['GET'])
def index():
    return render_template('scholar/index.html', articles=articles)


@mod.route('/article/<id>', methods=['GET'])
def show(id):
    article_id = int(id) - 1
    article = articles[article_id]
    return render_template('scholar/show.html', article=article)


@mod.route('/article/new', methods=['GET'])
def new():
    return render_template('scholar/new.html')


@mod.route('/article/<id>/edit', methods=['GET'])
def edit(id):
    return render_template('scholar/edit.html')


@mod.route('/article', methods=['POST'])
def create():
    pass


@mod.route('/article/<id>', methods=['PATCH', 'PUT'])
def update():
    pass


@mod.route('/article/<id>', methods=['DELETE'])
def destroy():
    pass