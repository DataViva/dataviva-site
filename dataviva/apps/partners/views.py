# -*- coding: utf8 -*-
from flask import Blueprint, render_template, g, redirect, url_for, flash
from dataviva.apps.general.views import get_locale
from forms import RegistrationForm
from models import Edict
from dataviva import db


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
    edicts = Edict.query.all()
    return render_template('partners/be-a-partner.html', edicts=edicts)


@mod.route('/edict/new', methods=['GET'])
def new():
    form = RegistrationForm();
    return render_template('partners/new.html', form=form)

@mod.route('/edict/new', methods=['POST'])
def create():
    form = RegistrationForm()
    if form.validate() is False:
        return render_template('partners/new.html', form=form)
    else:
        edict = Edict()
        edict.title = form.title.data
        edict.link = form.link.data

        db.session.add(edict)
        db.session.commit()

        message = u'Muito obrigado! Seu edital foi submetido com sucesso!'
        flash(message, 'success')
        return redirect(url_for('partners.index'))


@mod.route('/edict/<id>/edit', methods=['GET'])
def edit(id):
    form = RegistrationForm()
    edict = Edict.query.filter_by(id=id).first_or_404()
    form.title.data = edict.title
    form.link.data = edict.link
    return render_template('partners/edit.html', form=form, action=url_for('partners.update', id=id))



@mod.route('/edict/<id>/edit', methods=['POST'])
def update(id):
    form = RegistrationForm()
    if form.validate() is False:
        return render_template('partners/new.html', form=form)
    else:
        edict = Edict.query.filter_by(id=id).first_or_404()
        edict.title = form.title.data
        edict.link = form.link.data

        db.session.commit()

        message = u'Edital editado com sucesso!'
        flash(message, 'success')
        return redirect(url_for('partners.index'))


@mod.route('/edict/<id>/delete', methods=['GET'])
def delete(id):
    pass




    