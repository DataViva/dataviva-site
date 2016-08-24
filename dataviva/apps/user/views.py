# -*- coding: utf-8 -*-
from dataviva import db, lm
from dataviva.apps.general.views import get_locale
from dataviva.apps.user.models import User
from dataviva.utils.encode import sha512
from dataviva.utils.send_mail import send_mail
from datetime import datetime
from dataviva.translations.dictionary import dictionary
from flask import Blueprint, render_template, g, session, redirect, jsonify, abort, Response, flash, request, url_for
from flask.ext.login import login_user, login_required
from forms import (SignupForm, ChangePasswordForm, ForgotPasswordForm, ProfileForm)
from hashlib import md5
from dataviva.apps.admin.views import required_roles


mod = Blueprint('user', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/user',
                static_folder='static')


@mod.before_request
def before_request():
    g.page_type = mod.name


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


def _gen_confirmation_code(email):
    return md5("%s-%s" % (email, datetime.now())).hexdigest()


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@mod.route('/new', methods=["POST", "GET"])
def create():
    form = SignupForm()
    if request.method == "POST":
        if form.validate() is False:
            if 'fullname' in form.errors:
                return Response(form.errors['fullname'], status=400, mimetype='application/json')
            if 'email' in form.errors:
                return Response(form.errors['email'], status=400, mimetype='application/json')
            if 'password' in form.errors:
                return Response(form.errors['password'], status=400, mimetype='application/json')
            return Response('Error in Form.', status=400, mimetype='application/json')
        else:
            if (User.query.filter_by(email=form.email.data).count() > 0):
                return Response(dictionary()["email_already_exists"], status=400, mimetype='application/json')
            try:
                confirmation_code = _gen_confirmation_code(form.email.data)
                user = User(
                    nickname=form.email.data.split('@')[0],
                    fullname=form.fullname.data,
                    email=form.email.data,
                    password=sha512(form.password.data),
                    confirmation_code=confirmation_code,
                    agree_mailer=form.agree_mailer.data
                )
                db.session.add(user)
                db.session.commit()
            except:
                return Response(dictionary()["Sorry, an unexpected error has occured. Please try again"], status=500, mimetype='application/json')

            send_confirmation(user)

            message = dictionary()["check_your_inbox"] + ' ' + user.email

            return Response(message, status=200, mimetype='application/json')

    return render_template('user/new.html', form=form)


@mod.route('/edit', methods=["GET"])
@login_required
def edit():
    form = ProfileForm()

    form.profile.data = g.user.profile
    form.fullname.data = g.user.fullname
    form.email.data = g.user.email
    form.birthday.data = g.user.birthday
    form.country.data = g.user.country
    form.uf.data = g.user.uf
    form.city.data = g.user.city
    form.occupation.data = g.user.occupation
    form.institution.data = g.user.institution
    form.agree_mailer.data = g.user.agree_mailer

    return render_template("user/edit.html", form=form)


@mod.route('/edit', methods=["POST"])
@login_required
def change_profile():
    form = ProfileForm()
    if form.validate():
        try:
            user = g.user

            user.profile = form.profile.data
            user.fullname = form.fullname.data
            user.email = form.email.data
            user.birthday = form.birthday.data
            user.country = form.country.data
            user.uf = form.uf.data
            user.city = form.city.data
            user.occupation = form.occupation.data
            user.institution = form.institution.data
            user.agree_mailer = form.agree_mailer.data

            db.session.commit()

            flash("Profile updated successfully!", "success")
        except:
            flash("Something went wrong!", "danger")

    return render_template("user/edit.html", form=form)


def send_confirmation(user):
    confirmation_url = "%s%s/user/confirm/%s" % (request.url_root, g.locale, user.confirmation_code)
    confirmation_tpl = render_template('user/mail/confirmation.html',
                                       confirmation_url=confirmation_url)

    send_mail("Account confirmation", [user.email], confirmation_tpl)


@mod.route('/confirm_pending/<user_email>', methods=["GET"])
def confirm_pending(user_email):
    ''' Used to inform to the user that its user is pending
    '''
    try:
        user = User.query.filter_by(email=user_email)[-1]
    except IndexError:
        abort(404, 'User not found')

    if user.confirmed:
        return redirect('/')

    return render_template('user/confirm_pending.html', user=user.serialize())


@mod.route('/confirm/<code>', methods=["GET"])
def confirm(code):
    try:
        user = User.query.filter_by(confirmation_code=code)[-1]
        user.confirmed = True
        db.session.commit()
        login_user(user, remember=True)
        flash("Lest us know more about you. Please complete your profile.", "info")
    except IndexError:
        abort(404, 'User not found')

    return redirect(url_for('user.edit'))


@mod.route('/resend_confirmation/<user_email>', methods=["GET"])
def resend_confirmation(user_email):
    '''Used to regen the confirmation_code and send the email again to the user
    '''
    try:
        user = User.query.filter_by(email=user_email, confirmed=False)[-1]
    except IndexError:
        abort(404, 'Entry not found')

    user.confirmation_code = _gen_confirmation_code(user.email)
    db.session.commit()
    send_confirmation(user)
    flash(dictionary()["check_your_inbox"] + ' ' + user_email, 'success')
    return redirect(url_for('user.confirm_pending', user_email=user.email))


@mod.route('/change_password', methods=["GET"])
@login_required
def change_password():
    form = ChangePasswordForm()
    return render_template("user/change_password.html", form=form)


@mod.route('/change_password', methods=["POST"])
@login_required
def change():
    form = ChangePasswordForm()
    user = load_user(session["user_id"])

    if form.validate():
        if user.password == sha512(form.current_password.data):
            user.password = sha512(form.new_password.data)
            db.session.commit()
            flash("Password successfully update!", "success")
        else:
            flash("The current password is invalid", "danger")

    return render_template("user/change_password.html", form=form)


@mod.route('/forgot_password', methods=["GET"])
def forgot_password():
    form = ForgotPasswordForm()
    return render_template("user/forgot_password.html", form=form)


@mod.route('/forgot_password', methods=["POST"])
def reset_password():
    form = ForgotPasswordForm()

    try:
        user = User.query.filter_by(email=form.email.data)[-1]
        pwd = md5(str(datetime.now()) + form.email.data).hexdigest()[0:5]
        user.password = sha512(pwd)
        db.session.commit()

        email_tp = render_template('user/mail/forgot.html',
                                   user=user.serialize(),
                                   new_pwd=pwd)
        send_mail("Forgot Password", [user.email], email_tp)
        flash("A new password has been sent to you! Please check you inbox!", "success")
    except:
        flash("We couldnt find any user with the informed email address", "danger")

    return render_template("user/forgot_password.html", form=form)


@mod.route('/admin', methods=['GET'])
@login_required
@required_roles(1)
def admin():
    user = User.query.all()
    return render_template('user/admin.html', user=user)


@mod.route('/all/', methods=['GET'])
def all():
    result = User.query.all()
    users = []
    for row in result:
        users += [(row.id, row.fullname, row.email, row.role)]
    return jsonify(users=users)


@mod.route('/admin/users/<status>/<status_value>', methods=['POST'])
@login_required
@required_roles(1)
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
