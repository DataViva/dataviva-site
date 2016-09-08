# -*- coding: utf-8 -*-
from flask import Blueprint, g, url_for, render_template, flash, redirect
from dataviva.translations.dictionary import dictionary
from dataviva.apps.general.views import get_locale
from flask.ext.babel import gettext
from dataviva.utils.send_mail import send_mail
from forms import ContactForm
from models import Form
from dataviva import db
from datetime import datetime


mod = Blueprint('contact', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/contact')


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
    form = ContactForm()
    return render_template('contact/index.html', form=form, action=url_for('contact.create'))


@mod.route('/', methods=['POST'])
def create():
    form = ContactForm()
    if form.validate() is False:
        for error_type in form.errors:
            if form.errors[error_type][0] in dictionary():
                form.errors[error_type][0] = dictionary()[form.errors[error_type][0]]
        return render_template('contact/index.html', form=form, action=url_for('contact.create'))
    else:
        contact = Form()
        contact.name = form.name.data
        contact.email = form.email.data
        contact.subject = form.subject.data
        contact.message = form.message.data
        contact.postage_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        message_tpl = render_template('contact/message_template.html', contact=contact)

        db.session.add(contact)
        db.session.commit()
        send_mail("Contato - DataViva", ["contato@dataviva.info"], message_tpl)

        message = gettext("Your message has been sent successfully. We will soon get back to you.")
        flash(message, 'success')

        return redirect(url_for('contact.create'))
