# -*- coding: utf8 -*-
from flask import Blueprint, render_template, g, redirect, url_for, flash, make_response, jsonify, request
from dataviva.apps.general.views import get_locale
from forms import RegistrationForm
from models import Call
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
    calls = Call.query.filter_by(active=True).all()
    return render_template('partners/be-a-partner.html', calls=calls)


@mod.route('/call/new', methods=['GET'])
def new():
    form = RegistrationForm()
    return render_template('partners/new.html', form=form)


@mod.route('/call/new', methods=['POST'])
def create():
    form = RegistrationForm()
    if form.validate() is False:
        return render_template('partners/new.html', form=form)
    else:
        call = Call()
        call.title = form.title.data
        call.link = form.link.data
        call.active = 0

        db.session.add(call)
        db.session.commit()

        message = u'Muito obrigado! sua Chamada foi submetida com sucesso!'
        flash(message, 'success')
        return redirect(url_for('partners.be_a_partner'))


@mod.route('/call/<id>/edit', methods=['GET'])
def edit(id):
    form = RegistrationForm()
    call = Call.query.filter_by(id=id).first_or_404()
    form.title.data = call.title
    form.link.data = call.link
    return render_template('partners/edit.html', form=form, action=url_for('partners.update', id=id))


@mod.route('/call/<id>/edit', methods=['POST'])
def update(id):
    form = RegistrationForm()
    if form.validate() is False:
        return render_template('partners/new.html', form=form)
    else:
        call = Call.query.filter_by(id=id).first_or_404()
        call.title = form.title.data
        call.link = form.link.data

        db.session.commit()

        message = u'Chamada editada com sucesso!'
        flash(message, 'success')
        return redirect(url_for('partners.be_a_partner'))


@mod.route('/call/<id>/delete', methods=['GET'])
def delete(id):
    call = Call.query.filter_by(id=id).first_or_404()
    if call:
        db.session.delete(call)
        db.session.commit()
        message = u"Chamada excluída com sucesso!"
        flash(message, 'success')
        return redirect(url_for('partners.be_a_partner'))
    else:
        return make_response(render_template('not_found.html'), 404) 
       

@mod.route('/call/approval', methods=['GET'])
def approval():
    calls = Call.query.all()
    return render_template('partners/approval.html', calls=calls)


@mod.route('/approval', methods=['POST'])
def approval_update():
    for id, active in request.form.iteritems():
        call = Call.query.filter_by(id=id).first_or_404()
        call.active = active == u'true'
        db.session.commit()
    message = u"Estudo(s) atualizados com sucesso!"
    return message


@mod.route('/all', methods=['GET'])
def all():
    result = Call.query.all()
    calls = []
    for row in result:
        calls += [(row.id, row.title, row.link, row.active)]
    return jsonify(calls=calls)

