# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, redirect, url_for, jsonify, request
from dataviva.apps.general.views import get_locale
from dataviva.apps.account.models import User
from flask.ext.login import login_required
from dataviva import db


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
@login_required
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
@login_required
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
@login_required
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
