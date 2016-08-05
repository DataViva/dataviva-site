from dataviva import db, lm
from dataviva.apps.general.views import get_locale
from dataviva.apps.user.models import User, Starred
from dataviva.apps.ask.models import Question, Reply
from dataviva.utils.encode import sha512
from dataviva.utils.send_mail import send_mail
from datetime import datetime
from dataviva.translations.dictionary import dictionary
from flask import Blueprint, render_template, g, session, \
    redirect, jsonify, abort, Response, flash, request
from flask.ext.babel import gettext
from flask.ext.login import login_user, login_required
from forms import (SignupForm, ChangePasswordForm,
                   ForgotPasswordForm, ProfileForm)
from hashlib import md5


mod = Blueprint('user', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/user',
                static_folder='static')


@mod.before_request
def before_request():
    g.page_type = 'user'


def _gen_confirmation_code(email):
    return md5("%s-%s" % (email, datetime.now())).hexdigest()


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.route('/status/')
def check_status():
    result = g.user.is_authenticated
    data = {"logged_in": result}
    if result:
        data["user"] = g.user.nickname
        data["is_admin"] = g.user.is_admin()

    # Save variable in session so we can determine if this is the user's
    # first time on the site
    if 'first_time' in session:
        del session["first_time"]
    if 'first_visit' in session:
        session['first_visit'] = False
    else:
        session['first_visit'] = True

    return jsonify(data)


def send_confirmation(user):
    confirmation_url = "%s%s/user/confirm/%s" % (request.url_root, g.locale, user.confirmation_code)
    confirmation_tpl = render_template('user/mail/confirmation.html',
                                       confirmation_url=confirmation_url)

    send_mail("Account confirmation", [user.email], confirmation_tpl)


@mod.route('/signup', methods=["GET"])
def signup():
    form = SignupForm()
    return render_template('user/signup.html', form=form)


@mod.route('/signup', methods=["POST"])
def create_user():
    form = SignupForm()
    if form.validate() is False:
        if form.errors.has_key('fullname'):
            return Response(form.errors['fullname'], status=400, mimetype='application/json')
        if form.errors.has_key('email'):
            return Response(form.errors['email'], status=400, mimetype='application/json')
        if form.errors.has_key('password'):
            return Response(form.errors['password'], status=400, mimetype='application/json')
        return Response('Error in Form.', status=400, mimetype='application/json')
    else:
        if (User.query.filter_by(email=form.email.data).count() > 0):
            return Response(dictionary()["email_already_exists"], status=400, mimetype='application/json')
        try:
            confirmation_code = _gen_confirmation_code(form.email.data)
            user = User(
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

    flash(dictionary()["check_your_inbox"] + ' ' + user_email, 'success')
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

    return redirect('/user/edit_profile')


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
    return redirect('/user/confirm_pending/%s' % user.email)


@mod.route('/edit_profile', methods=["GET"])
@login_required
def edit_profile():
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

    return render_template("user/edit_profile.html", form=form)


@mod.route('/edit_profile', methods=["POST"])
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

    return render_template("user/edit_profile.html", form=form)


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
        flash(
            "A new password has been sent to you! Please check you inbox!", "success")
    except:
        flash(
            "We couldnt find any user with the informed email address", "danger")

        return render_template("user/forgot_password.html", form=form)

    return redirect("user/signin")


###############################
# User management
# ---------------------------
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@mod.route('/<nickname>/')
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first_or_404()
    activity = None

    stars = Starred.query.filter_by(user=user) \
        .order_by("timestamp desc").all()

    questions = Question.query.filter_by(user=user) \
        .order_by("timestamp desc").all()

    replies = Reply.query.filter_by(user=user) \
        .order_by("timestamp desc").all()

    activity = stars + questions + replies
    activity.sort(key=lambda a: a.timestamp, reverse=True)

    return render_template("user/index.html",
                           user=user,
                           activity=activity)


def update_email_preferences(id, nickname, agree):
    user = User.query.filter_by(nickname=nickname).first_or_404()
    if user.id == int(id) and int(agree) in [0, 1]:
        user.agree_mailer = agree
        db.session.add(user)
        db.session.commit()

    return user


@mod.route('/remove_email/<id>/<nickname>')
def remove_email_list(id, nickname):
    update_email_preferences(id, nickname, 0)
    flash(gettext("Preferences updated."))
    return redirect('/')


@mod.route('/preferences/change_email_preference')
def preferences():
    if g.user.is_authenticated:
        if g.user.agree_mailer == 1:
            agree = 0
        else:
            agree = 1

        user = update_email_preferences(g.user.id, g.user.nickname, agree)
        flash(gettext("Preferences updated."))
        return redirect('/user/' + user.nickname)
    else:
        return redirect('/')
