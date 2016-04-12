# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, redirect, url_for, jsonify, request, flash
from dataviva.apps.general.views import get_locale
from dataviva.apps.account.models import User
from dataviva import db
from forms import RegistrationForm


mod = Blueprint('users', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/users')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/')
def users():
    return redirect(url_for('.admin_users'))


@mod.route('/admin', methods=['GET'])
def admin():
    users = User.query.all()
    return render_template('users/admin.html', users=users)


@mod.route('/all/', methods=['GET'])
def all():
    result = User.query.all()
    users = []
    for row in result:
        users += [(row.id, row.fullname, row.email, row.role)]
    return jsonify(users=users)


@mod.route('/admin/delete', methods=['POST'])
def admin_delete():
    ids = request.form.getlist('ids[]')
    if ids:
        users = User.query.filter(User.id.in_(ids)).all()
        for user in users:
            db.session.delete(user)

        db.session.commit()
        return u"Usuário(s) excluído(s) com sucesso!", 200
    else:
        return u'Selecione algum usuário para excluí-lo.', 205


@mod.route('/admin/users/<status>/<status_value>', methods=['POST'])
def admin_activate(status, status_value):
    for id in request.form.getlist('ids[]'):
        users = User.query.filter_by(id=id).first_or_404()
        if status_value == 'true':
            users.role = 1
        else:
            users.role = 0
        db.session.commit()

    message = u"Usuário(s) alterado(s) com sucesso!"
    return message, 200


@mod.route('/admin/users/<id>/edit', methods=['GET'])
def edit(id):
    form = RegistrationForm()
    users = User.query.filter_by(id=id).first_or_404()
    form.nickname.data = users.nickname
    form.email.data = users.email
    form.fullname.data = users.fullname
    form.country.data = users.country
    form.gender.data = users.gender
    return render_template('users/edit.html', form=form, action=url_for('users.update', id=id))


@mod.route('/admin/users/<id>/edit', methods=['POST'])
def update(id):
    form = RegistrationForm()
    id = int(id.encode())
    if form.validate() is False:
        return render_template('users/edit.html', form=form)
    else:
        users = User.query.filter_by(id=id).first_or_404()
        users.nickname = form.nickname.data
        users.email = form.email.data
        users.fullname = form.fullname.data
        users.country = form.country.data
        users.gender = form.gender.data

        db.session.commit()

        message = u'Usuário editado com sucesso!'
        flash(message, 'success')
        return redirect(url_for('users.admin'))