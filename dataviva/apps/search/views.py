# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, redirect, url_for, flash, jsonify, request
from dataviva.apps.general.views import get_locale

mod = Blueprint('search', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/search')


@mod.before_request
def before_request():
    g.page_type = mod.name


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/', methods=['GET'])
def index():
    pass


@mod.route('/admin', methods=['GET'])
def admin():
    return render_template('search/admin.html')


@mod.route('/admin/question/new', methods=['GET'])
def new():
    form = RegistrationForm()
    return render_template('search/new.html', form=form, action=url_for('search.create'))


@mod.route('/admin/question/new', methods=['POST'])
def create():
    pass
