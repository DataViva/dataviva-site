# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, redirect, url_for, flash
from dataviva.apps.general.views import get_locale
from forms import RegistrationForm
from models import Form
from dataviva import db
from datetime import datetime


mod = Blueprint('contact', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/contact')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/', methods=['GET'])
def index():
    form = RegistrationForm()
    return render_template('contact/index.html', form=form, action=url_for('contact.create'))


@mod.route('/contact/new', methods=['POST'])
def create():
    form = RegistrationForm()
    if form.validate() is False:
        return render_template('contact/index.html', form=form)
    else:
        form = Form()
        form.name = form.name.data
        form.email = form.email.data
        form.message = form.message.data
        form.postage_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        db.session.add(form)
        db.session.commit()

        message = u'Sua mensagem foi enviada com sucesso. Em breve retornaremos.'
        flash(message, 'success')
        return redirect(url_for('scholar.index'))
