import json
from sqlalchemy import or_
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, jsonify, abort, current_app
from flask.ext.login import login_user, logout_user, current_user, login_required
from visual import db, lm
from forms import LoginForm, UserEditForm
from datetime import datetime
from urllib2 import Request, urlopen, URLError
# models
from visual.account.models import User, Starred, ROLE_USER, ROLE_ADMIN
from visual.ask.models import Question, Status, Reply
# forms
from visual.ask.forms import AskForm
# utils
from visual.utils import exist_or_404, Pagination
# login types
from visual.account.login_providers import facebook, twitter, google

mod = Blueprint('account', __name__, url_prefix='/account')

RESULTS_PER_PAGE = 10

@mod.errorhandler(404)
def page_not_found(error):
    return error, 404

###############################
# User management
# ---------------------------
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@mod.route('/complete_login/')
def complete_login():
    return render_template('account/complete_login.html')

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
            callback=url_for('account.google_authorized', _external=True)
            return google.authorize(callback=callback)
        elif provider == "twitter":
            callback=url_for('account.twitter_authorized',
                next=request.args.get('next') or request.referrer or None,
                _external=True)
            return twitter.authorize(callback=callback)
        elif provider == "facebook":
            callback=url_for('account.facebook_authorized',
                next=request.args.get('next') or request.referrer or None,
                _external=True)
            return facebook.authorize(callback=callback)
    
    return render_template('account/login.html', 
        form = form,
        providers = providers)

@mod.route('/<nickname>/')
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first_or_404()
    return render_template("account/user_home.html", user=user)

@mod.route('/<nickname>/questions/')
@mod.route('/<nickname>/questions/<status>/')
def questions(nickname, status=None):
    user = User.query.filter_by(nickname=nickname).first_or_404()    
    offset = request.args.get('offset', 0)
    activity_dict = {}
    activity_list = []
    limit = 50
    
    this_status = Status.query.filter_by(name=status).first()
    approved_status = Status.query.filter_by(name='approved').first()
    if g.user != user and this_status:
        return redirect(url_for(".questions", nickname=user.nickname))
    
    if request.is_xhr:
        
        qs = Question.query
        if this_status and g.user == user:
            qs = qs.filter_by(status=this_status)
        elif g.user != user:
            qs = qs.filter_by(status=approved_status)
        qs = qs.filter_by(user=user) \
                    .order_by("timestamp desc") \
                    .limit(limit).offset(offset)
        items = [q.serialize() for q in qs.all()]
    
        return jsonify({"activities":items})
    
    return render_template("account/questions.html", 
                status=status,
                user=user)

@mod.route('/<nickname>/starred/')
def starred(nickname):
    user = User.query.filter_by(nickname=nickname).first_or_404()        
    offset = request.args.get('offset', 0)
    activity_dict = {}
    activity_list = []
    limit = 50
    
    if request.is_xhr:
        items = Starred.query.filter_by(user=user) \
                    .order_by("timestamp desc") \
                    .limit(limit).offset(offset).all()
        items = [i.serialize() for i in items]
        
        return jsonify({"activities":items})
    
    return render_template("account/starred.html",
                user=user)


@mod.route('/<nickname>/replies/')
def replies(nickname):
    user = User.query.filter_by(nickname=nickname).first_or_404()    
    offset = request.args.get('offset', 0)
    activity_dict = {}
    activity_list = []
    limit = 50
    
    if request.is_xhr:
        items = Reply.query.filter_by(user=user) \
                    .order_by("timestamp desc") \
                    .limit(limit).offset(offset).all()
        items = [i.serialize() for i in items]
        
        return jsonify({"activities":items})
    
    return render_template("account/replies.html",
                user=user)


def after_login(**user_fields):
    # Remove None values
    user_fields = {k:v for k,v in user_fields.items() if v is not None}
    if "google_id" in user_fields:
        user = User.query.filter_by(google_id = user_fields["google_id"]).first()
    elif "twitter_id" in user_fields:
        user = User.query.filter_by(twitter_id = user_fields["twitter_id"]).first()
    elif "facebook_id" in user_fields:
        user = User.query.filter_by(facebook_id = user_fields["facebook_id"]).first()
    if user is None:
        nickname = user_fields["nickname"] if "nickname" in user_fields else None
        if nickname is None or nickname == "":
            nickname = user_fields["email"].split('@')[0]
        nickname = User.make_unique_nickname(nickname)
        user_fields["nickname"] = nickname
        user = User(**user_fields)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)

    return redirect(url_for('account.complete_login'))





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
    # user = g.user
    # if user is not None:
    #     return user.oauth_token, user.oauth_secret

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
    # session['oauth_token'] = (resp['oauth_token'], '')
    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    response = twitter.get('users/show.json?screen_name='+resp["screen_name"]).data

    fullname = response["name"] if "name" in response else None
    nickname = response["screen_name"] if "screen_name" in response else None
    language = response["lang"] if "lang" in response else None
    country = response["location"] if "location" in response else None
    image = response["profile_image_url"] if "profile_image_url" in response else None
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
    # me = facebook.get('/me/')
    response = facebook.get('/me/?fields=picture,username,name,id,location,locale,email').data
    
    email = response["email"] if "email" in response else None
    fullname = response["name"] if "name" in response else None
    language = response["locale"] if "locale" in response else None
    country = response["location"]["name"] if "location" in response else None
    image = response["picture"]["data"]["url"] if "picture" in response else None
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
    # raise Exception(session['google_access_token'])
    access_token = resp['access_token']
    session['google_token'] = access_token, ''
    
    # headers = {'Authorization': 'OAuth '+access_token}
    # req = Request('https://www.googleapis.com/plus/v1/people/me',
    #               None, headers)
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token='+access_token)
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
