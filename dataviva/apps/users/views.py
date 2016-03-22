# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, make_response, redirect, url_for, flash, jsonify, request
from dataviva.apps.general.views import get_locale

from dataviva.apps.account.models import User
from dataviva.apps.ask.models import Question, Status, Reply, Flag, Vote
from dataviva import db
from datetime import datetime


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

@mod.route('/users/', methods=['GET'])
def admin_users():

    users = User.query.all()
    return render_template('/users/control.html', users=users)

@mod.route('/users/', methods=['POST'])
def admin_update():
    for id, role in request.form.iteritems():
        user = User.query.filter_by(id=id).first_or_404()
        user.role = role == u'true'
        db.session.commit()
    message = u"Administradores(s) atualizados com sucesso!"
    return message


@mod.route('/all/', methods=['GET'])
def all():
    result = User.query.all()
    users = []
    for row in result:
        users+=[(row.id, row.fullname,row.email, row.role)]
    return jsonify(users=users)
