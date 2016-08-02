from dataviva import db, lm, app
from dataviva.apps.general.views import get_locale
from dataviva.apps.account.login_providers import facebook, twitter, google
from dataviva.apps.account.models import User, Starred, ROLE_USER, ROLE_ADMIN
from dataviva.apps.ask.forms import AskForm
from dataviva.apps.ask.models import Question, Status, Reply
from dataviva.utils.exist_or_404 import exist_or_404
from dataviva.utils.encode import sha512
from dataviva.utils.send_mail import send_mail
from datetime import datetime
from dataviva.translations.dictionary import dictionary
from flask import Blueprint, request, render_template, flash, g, session, \
    redirect, url_for, jsonify, abort, current_app, Response, make_response
from flask.ext.babel import gettext
from flask.ext.login import login_user, logout_user, current_user, \
    login_required, LoginManager
from forms import (LoginForm, SignupForm, SigninForm, ChangePasswordForm,
                   ForgotPasswordForm, ProfileForm)
from sqlalchemy import or_
from urllib2 import Request, urlopen, URLError
import json
from hashlib import md5


mod = Blueprint('account', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/account',
                static_folder='static')


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
    confirmation_url = "%s%s/account/confirm/%s" % (request.url_root , g.locale, user.confirmation_code)
    confirmation_tpl = render_template('account/mail/confirmation.html',
                                       confirmation_url=confirmation_url)

    send_mail("Account confirmation", [user.email], confirmation_tpl)


@mod.route('/signup', methods=["GET"])
def signup():
    form = SignupForm()
    return render_template('account/signup.html', form=form)


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


@mod.route('/social_auth/<provider>', methods=["GET"])
def social_auth(provider):
    # TODO
    if provider == "google":
        callback = url_for('account.google_authorized', _external=True)
        return google.authorize(callback=callback)

    return render_template('account/signin.html', form=form)


@mod.route('/signin', methods=["GET", "POST"])
def signin():

    form = SigninForm()

    if request.method == "POST":
        user = User.query.filter_by(email=form.email.data, password=sha512(form.password.data)).first()
        if user:
            if user.confirmed:
                login_user(user, remember=True)
                return redirect("/")
            else:
                return Response("Confirm Pending", status=401, mimetype='application/json', )
        else:
            return Response("Email or Password Incorrect!", status=400, mimetype='application/json')

    else:
        return render_template('account/signin.html', form=form)


@mod.route('/confirm_pending/<user_email>', methods=["GET"])
def confirm_pending(user_email):
    ''' Used to inform to the user that its account is pending
    '''
    try:
        user = User.query.filter_by(email=user_email)[-1]
    except IndexError:
        abort(404, 'User not found')

    if user.confirmed:
        return redirect('/')

    return render_template('account/confirm_pending.html', user=user.serialize())


@mod.route('/confirm/<code>', methods=["GET"])
def confirm(code):
    try:
        user = User.query.filter_by(confirmation_code=code)[-1]
        user.confirmed = True
        db.session.commit()
        login_user(user, remember=True)
        flash(
            "Lest us know more about you. Please complete your profile.", "info")
    except IndexError:
        abort(404, 'User not found')

    return redirect('/account/edit_profile')


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
    return redirect('/account/confirm_pending/%s' % user.email)


@mod.route('/edit_profile', methods=["GET"])
@login_required
def edit_profile():
    form = ProfileForm()
    form.fullname.data = g.user.fullname
    form.gender.data = g.user.gender
    form.website.data = g.user.website
    form.bio.data = g.user.bio

    return render_template("account/edit_profile.html", form=form)


@mod.route('/edit_profile', methods=["POST"])
@login_required
def change_profile():
    form = ProfileForm()
    if form.validate():
        try:
            user = g.user
            user.fullname = form.fullname.data
            user.gender = form.gender.data
            user.website = form.website.data
            user.bio = form.bio.data
            db.session.commit()

            message = u'Profile updated successfully!'
            flash(message, 'success')
        except:
            flash("Something went wrong!", "danger")

    return render_template("account/edit_profile.html", form=form)


@mod.route('/change_password', methods=["GET"])
@login_required
def change_password():
    form = ChangePasswordForm()
    return render_template("account/change_password.html", form=form)


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
            
    return render_template("account/change_password.html", form=form)


@mod.route('/forgot_password', methods=["GET"])
def forgot_password():
    form = ForgotPasswordForm()
    return render_template("account/forgot_password.html", form=form)


@mod.route('/forgot_password', methods=["POST"])
def reset_password():
    form = ForgotPasswordForm()

    try:
        user = User.query.filter_by(email=form.email.data)[-1]
        pwd = md5(str(datetime.now()) + form.email.data).hexdigest()[0:5]
        user.password = sha512(pwd)
        db.session.commit()

        email_tp = render_template('account/mail/forgot.html',
                                   user=user.serialize(),
                                   new_pwd=pwd)
        send_mail("Forgot Password", [user.email], email_tp)
        flash(
            "A new password has been sent to you! Please check you inbox!", "success")
    except Exception as e:
        flash(
            "We couldnt find any user with the informed email address", "danger")

        return render_template("account/forgot_password.html", form=form)

    return redirect("account/signin")


###############################
# User management
# ---------------------------
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


###############################
# Views for ALL logged in users
# ---------------------------
@mod.route('/logout/')
def logout():
    session.pop('twitter_token', None)
    session.pop('google_token', None)
    session.pop('facebook_token', None)
    logout_user()
    return redirect('/')


@mod.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    providers = ["Facebook", "Google", "Twitter"]

    if form.validate_on_submit():
        provider = form.provider.data
        session['remember_me'] = form.remember_me.data
        session['provider'] = provider

        if provider == "google":
            callback = url_for('account.google_authorized', _external=True)
            return google.authorize(callback=callback)
        if provider == "twitter":
            callback = url_for('account.twitter_authorized',
                               next=request.args.get(
                                   'next') or request.referrer or None,
                               _external=True)
            return twitter.authorize(callback=callback)
        elif provider == "facebook":
            callback = url_for('account.facebook_authorized',
                               next=request.args.get(
                                   'next') or request.referrer or None,
                               _external=True)
            return facebook.authorize(callback=callback)

    return render_template(
        'account/login.html', form=form, providers=providers)


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

    return render_template("account/index.html",
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
        return redirect('/account/' + user.nickname)
    else:
        return redirect('/')


@mod.route('/complete_login/', methods=['GET', 'POST'])
def after_login(**user_fields):
    import re

    if request.method == "POST":
        user_fields = {k: v for k, v in request.form.items() if v is not None}
    else:
        user_fields = {k: v for k, v in user_fields.items() if v is not None}

    print(request.host)

    if "google_id" in user_fields:
        user = User.query.filter_by(google_id=user_fields["google_id"]).first()
    elif "twitter_id" in user_fields:
        user = User.query.filter_by(
            twitter_id=user_fields["twitter_id"]).first()
    elif "facebook_id" in user_fields:
        user = User.query.filter_by(
            facebook_id=user_fields["facebook_id"]).first()
    elif None is not re.match(r'^(localhost|127.0.0.1)', request.host):
        user = User(id=1)

    if user is None:

        nickname = user_fields[
            "nickname"] if "nickname" in user_fields else None
        if nickname is None or nickname == "":
            nickname = user_fields["email"].split('@')[0]
        nickname = User.make_unique_nickname(nickname)
        user_fields["nickname"] = nickname
        user_fields["agree_mailer"] = 1
        user = User(**user_fields)
        db.session.add(user)
        db.session.commit()

    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)

    return render_template('account/complete_login.html')

"""
    TWITTER LOGIN
    Here are the specific methods for logging in users with their
    twitter accounts.
"""


@twitter.tokengetter
def get_twitter_token():
    """This is used by the API to look for the auth token and secret
    it should use for API calls.  During the authorization handshake
    a temporary set of token and secret is used, but afterwards this
    function has to return the token and secret.  If you don't want
    to store this in the database, consider putting it into the
    session instead.
    """
    return session.get('twitter_token')


@mod.route('/twoauth-authorized/')
@twitter.authorized_handler
def twitter_authorized(resp):
    """Called after authorization.  After this function finished handling,
    the OAuth information is removed from the session again.  When this
    happened, the tokengetter from above is used to retrieve the oauth
    token and secret.

    Because the remote application could have re-authorized the application
    it is necessary to update the values in the database.

    If the application redirected back after denying, the response passed
    to the function will be `None`.  Otherwise a dictionary with the values
    the application submitted.  Note that Twitter itself does not really
    redirect back unless the user clicks on the application name.
    """

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    response = twitter.get(
        'users/show.json?screen_name='+resp["screen_name"]).data

    fullname = response["name"] if "name" in response else None
    nickname = response["screen_name"] if "screen_name" in response else None
    language = response["lang"] if "lang" in response else None
    country = response["location"] if "location" in response else None
    image = response[
        "profile_image_url"] if "profile_image_url" in response else None
    id = response["id"] if "id" in response else None

    return after_login(twitter_id=id, fullname=fullname, nickname=nickname, language=language, country=country, image=image)


"""
    FACEBOOK LOGIN
    Here are the specific methods for logging in users with their
    facebook accounts.
"""


@mod.route('/fblogin/authorized/')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['facebook_token'] = (resp['access_token'], '')
    response = facebook.get(
        '/me/?fields=picture,username,name,id,location,locale,email').data

    email = response["email"] if "email" in response else None
    fullname = response["name"] if "name" in response else None
    language = response["locale"] if "locale" in response else None
    country = response["location"]["name"] if "location" in response else None
    image = response["picture"]["data"][
        "url"] if "picture" in response else None
    id = response["id"] if "id" in response else None

    return after_login(facebook_id=id, fullname=fullname, email=email, language=language, country=country, image=image)


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('facebook_token')


"""
    GOOGLE LOGIN
    Here are the specific methods for logging in users with their
    google accounts.
"""


@mod.route('/google_authorized/')
@google.authorized_handler
def google_authorized(resp):
    access_token = resp['access_token']
    session['google_token'] = access_token, ''

    req = Request(
        'https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token='+access_token)
    try:
        res = urlopen(req)
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('google_token', None)
            raise Exception('error!')
            # return redirect(url_for('login'))
        return res.read()
        raise Exception('ERROR!', res.read())

    response = json.loads(res.read())
    email = response["email"] if "email" in response else None
    fullname = response["name"] if "name" in response else None
    language = response["locale"] if "locale" in response else None
    gender = response["gender"] if "gender" in response else None
    image = response["picture"] if "picture" in response else None
    id = response["id"] if "id" in response else None

    return after_login(google_id=id, email=email, fullname=fullname, language=language, gender=gender, image=image)


@google.tokengetter
def get_access_token():
    return session.get('google_token')
