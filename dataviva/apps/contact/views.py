# -*- coding: utf-8 -*-
from flask import Blueprint, g, redirect, url_for, flash, render_template, request
from dataviva.apps.general.views import get_locale
from dataviva.utils.send_mail import send_mail
from forms import ContactForm
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
    form = ContactForm()
    return render_template('contact/index.html', form=form, action=url_for('contact.create'))


@mod.route('/', methods=['POST'])
def create():
    form = ContactForm()
    if form.validate() is False:
        return render_template('contact/index.html', form=form)
    else:
        contact = Form()
        contact.name = form.name.data
        contact.email = form.email.data
        contact.subject = form.subject.data
        contact.message = form.message.data
        contact.postage_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        message_tpl = render_template(
            'contact/message_template.html', contact=contact)

        db.session.add(contact)
        db.session.commit()
        send_mail("Mensagem recebida via página de Contato",
                  ["contato@dataviva.info"], message_tpl)
        message = u'Sua mensagem foi enviada com sucesso. Em breve retornaremos.'
        flash(message, 'success')

        return redirect(request.referrer)
