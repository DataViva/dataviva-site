# -*- coding: utf8 -*-
from flask import Blueprint, render_template, g, redirect, url_for, flash, make_response, jsonify, request
from dataviva.apps.general.views import get_locale
from forms import RegistrationForm
from models import Call
from dataviva import db
from flask.ext.login import login_required
from dataviva.apps.admin.views import required_roles


mod = Blueprint('calls', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/calls')


@mod.before_request
def before_request():
    g.page_type = mod.name


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/admin/call/new', methods=['GET'])
@login_required
@required_roles(1)
def new():
    form = RegistrationForm()
    return render_template('calls/new.html', form=form)


@mod.route('/admin/call/new', methods=['POST'])
@login_required
@required_roles(1)
def create():
    form = RegistrationForm()
    if form.validate() is False:
        return render_template('calls/new.html', form=form)
    else:
        call = Call()
        call.title = form.title.data
        call.link = form.link.data
        call.active = 0

        db.session.add(call)
        db.session.commit()

        message = u'Muito obrigado! sua Chamada foi submetida com sucesso!'
        flash(message, 'success')
        return redirect(url_for('calls.admin'))


@mod.route('/admin/call/<id>/edit', methods=['GET'])
@login_required
@required_roles(1)
def edit(id):
    form = RegistrationForm()
    call = Call.query.filter_by(id=id).first_or_404()
    form.title.data = call.title
    form.link.data = call.link
    return render_template('calls/edit.html', form=form, action=url_for('calls.update', id=id))


@mod.route('/admin/call/<id>/edit', methods=['POST'])
@login_required
@required_roles(1)
def update(id):
    form = RegistrationForm()
    if form.validate() is False:
        return render_template('calls/new.html', form=form)
    else:
        call = Call.query.filter_by(id=id).first_or_404()
        call.title = form.title.data
        call.link = form.link.data

        db.session.commit()

        message = u'Chamada editada com sucesso!'
        flash(message, 'success')
        return redirect(url_for('calls.admin'))


@mod.route('/admin/delete', methods=['POST'])
@login_required
@required_roles(1)
def admin_delete():
    ids = request.form.getlist('ids[]')
    if ids:
        calls = Call.query.filter(Call.id.in_(ids)).all()
        for call in calls:
            db.session.delete(call)

        db.session.commit()
        return u"Chamada(s) excluída(s) com sucesso!", 200
    else:
        return u'Selecione alguma chamada para excluí-la.', 205


@mod.route('/admin', methods=['GET'])
@login_required
@required_roles(1)
def admin():
    calls = Call.query.all()
    return render_template('calls/admin.html', calls=calls)


@mod.route('/admin/call/<status>/<status_value>', methods=['POST'])
@login_required
@required_roles(1)
def admin_update(status, status_value):
    for id in request.form.getlist('ids[]'):
        call = Call.query.filter_by(id=id).first_or_404()
        setattr(call, status, status_value == u'true')
        db.session.commit()
    message = u"Chamada(s) atualizados com sucesso!"
    return message


@mod.route('/all', methods=['GET'])
def all():
    result = Call.query.all()
    calls = []
    for row in result:
        calls += [(row.id, row.title, row.link, row.active)]
    return jsonify(calls=calls)

