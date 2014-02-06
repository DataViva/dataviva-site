from dataviva import db, lm
from dataviva.account.login_providers import facebook, twitter, google
from dataviva.account.models import User, Starred, ROLE_USER, ROLE_ADMIN
from dataviva.ask.forms import AskForm
from dataviva.ask.models import Question, Status, Reply
from dataviva.utils import exist_or_404
from datetime import datetime
from flask import Blueprint, request, render_template, flash, g, session, \
    redirect, url_for, jsonify, abort, current_app
from flask.ext.babel import gettext
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from forms import LoginForm, UserEditForm
from sqlalchemy import or_
from urllib2 import Request, urlopen, URLError
import json
# models
# forms
# utils
# login types

# from config import SITE_MIRROR
# import urllib2, urllib

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
        user = user,
        activity = activity)


def update_email_preferences(id, nickname, agree):
    user = User.query.filter_by(nickname=nickname).first_or_404()
    if user.id == int(id) and int(agree) in [0,1]:
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
    if g.user.is_authenticated() :
        if g.user.agree_mailer == 1:
            agree = 0
        else:
            agree = 1
            
        user = update_email_preferences(g.user.id, g.user.nickname, agree)
        flash(gettext("Preferences updated."))
        return redirect('/account/' + user.nickname )
    else:
        return redirect('/')

    
@mod.route('/complete_login/', methods=['GET', 'POST'])
def after_login(**user_fields):
    import re
    
    if request.method == "POST":
        user_fields = {k:v for k,v in request.form.items() if v is not None}
    else:
        user_fields = {k:v for k,v in user_fields.items() if v is not None}
    
    print(request.host)
    
    if "google_id" in user_fields:
        user = User.query.filter_by(google_id = user_fields["google_id"]).first()
    elif "twitter_id" in user_fields:
        user = User.query.filter_by(twitter_id = user_fields["twitter_id"]).first()
    elif "facebook_id" in user_fields:
        user = User.query.filter_by(facebook_id = user_fields["facebook_id"]).first()
    elif None is not re.match(r'^(localhost|127.0.0.1)', request.host ):
        user = User(id = 1)
        
    if user is None:
            
        # if request.remote_addr != SITE_MIRROR.split(":")[1][2:]:
        #     form_json = user_fields
        #     try:
        #         opener = urllib2.urlopen("{0}account/complete_login/".format(SITE_MIRROR),urllib.urlencode(form_json),5)
        #     except:
        #         flash(gettext("The server is not responding. Please try again later."))
        #         return render_template('account/complete_login.html')
        
        nickname = user_fields["nickname"] if "nickname" in user_fields else None
        if nickname is None or nickname == "":
            nickname = user_fields["email"].split('@')[0]
        nickname = User.make_unique_nickname(nickname)
        user_fields["nickname"] = nickname
        user = User(**user_fields)
        db.session.add(user)
        db.session.commit()
        
    # if request.remote_addr == SITE_MIRROR.split(":")[1][2:]:
    #     return jsonify({"success": 1})
    # else:
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)

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
