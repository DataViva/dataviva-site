from dataviva import db
from dataviva.apps.session.login_providers import facebook, twitter, google
from dataviva.apps.general.views import get_locale
from dataviva.apps.user.models import User
from dataviva.utils.encode import sha512
from dataviva.translations.dictionary import dictionary
from flask import Blueprint, request, render_template, session, redirect, Response, url_for, g
from flask.ext.login import login_user, logout_user
from forms import LoginForm
from urllib2 import Request, urlopen, URLError
import json


mod = Blueprint('session', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/session',
                static_folder='static')


@mod.before_request
def before_request():
    g.page_type = 'session'


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.route('/logout')
def logout():
    session.pop('twitter_token', None)
    session.pop('google_token', None)
    session.pop('facebook_token', None)
    logout_user()
    return redirect('/')


@mod.route('/login', methods=['GET', 'POST'])
@mod.route('/login/<provider>', methods=['GET', 'POST'])
def login(provider=None):
    form = LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data, password=sha512(form.password.data)).first()

            if user:
                if user.confirmed:
                    login_user(user, remember=True)
                    return redirect("/")
                else:
                    return Response("Confirm Pending", status=401, mimetype='application/json', )

        return Response(dictionary()["invalid_password"], status=400, mimetype='application/json')

    if provider:
        if provider == "google":
            callback = url_for('session.google_authorized', _external=True)
            return google.authorize(callback=callback)

        if provider == "twitter":
            callback = url_for('session.twitter_authorized',
                               next=request.args.get(
                                   'next') or request.referrer or None,
                               _external=True)
            return twitter.authorize(callback=callback)

        if provider == "facebook":
            callback = url_for('session.facebook_authorized',
                               next=request.args.get(
                                   'next') or request.referrer or None,
                               _external=True)
            return facebook.authorize(callback=callback)

    return render_template('session/signin.html', form=form)


@mod.route('/complete_login/', methods=['GET', 'POST'])
def after_login(provider, email, fullname, language, gender, image):

    user = User.query.filter_by(email=email, provider=provider).first()

    if user is None:
        user = User()
        user.nickname = email.split('@')[0]
        user.agree_mailer = True
        user.confirmed = True
        user.provider = provider
        user.email = email
        user.fullname = fullname
        user.language = language
        user.gender = gender
        user.image = image

        db.session.add(user)
        db.session.commit()

    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)

    return redirect('/')


"""
    GOOGLE LOGIN
    Here are the specific methods for logging in users with their
    google accounts.
"""


@google.tokengetter
def get_access_token():
    return session.get('google_token')


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

    return after_login(provider="google", email=email, fullname=fullname, language=language, gender=gender, image=image)


"""
    FACEBOOK LOGIN
    Here are the specific methods for logging in users with their
    facebook accounts.
"""


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('facebook_token')


@mod.route('/facebook_authorized/')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['facebook_token'] = (resp['access_token'], '')
    response = facebook.get('/me/?fields=picture,name,locale,email, gender').data

    email = response["email"] if "email" in response else None
    fullname = response["name"] if "name" in response else None
    language = response["locale"] if "locale" in response else None
    gender = response["gender"] if "gender" in response else None
    image = response["picture"]["data"]["url"] if "picture" in response else None

    return after_login(provider="facebook", fullname=fullname, email=email, language=language, gender=gender, image=image)


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

    response = twitter.get('users/show.json?screen_name=' + resp["screen_name"]).data

    fullname = response["name"] if "name" in response else None
    nickname = response["screen_name"] if "screen_name" in response else None
    language = response["lang"] if "lang" in response else None
    country = response["location"] if "location" in response else None
    image = response[
        "profile_image_url"] if "profile_image_url" in response else None
    id = response["id"] if "id" in response else None

    return after_login(twitter_id=id, fullname=fullname, nickname=nickname, language=language, country=country, image=image)
