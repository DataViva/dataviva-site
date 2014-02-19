from datetime import datetime
from flask import Blueprint, render_template, g, request, current_app, session, redirect, url_for, flash, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.babel import gettext

import time

mod = Blueprint('general', __name__, url_prefix='/')

from dataviva import app, db, babel, __latest_year__
from dataviva.general.forms import AccessForm
from dataviva.general.models import Short

from config import STATIC_URL, ACCOUNTS

###############################
# General functions for ALL views
# ---------------------------
@app.before_request
def before_request():
    
    g.accounts = True if ACCOUNTS in ["True","true","Yes","yes","Y","y",1] else False
    g.color = "#af1f24"
    g.static_url = STATIC_URL
    g.page_type = mod.name
    g.latest_year = {}
    for dataset in __latest_year__:
        g.latest_year[dataset] = __latest_year__[dataset]
            
    # Save variable in session so we can determine if this is the user's
    # first time on the site
    if 'first_time' in session:
        session['first_time'] = False
    else:
        session['first_time'] = True
    
    # Check if the user is logged in, if so give the global object
    # a reference to the user from DB
    g.user = current_user
    if g.user.is_authenticated() and request.endpoint != 'static':
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
    
    # Set the locale to either 'pt' or 'en' on the global object
    if request.endpoint != 'static':
        g.locale = get_locale()

@babel.localeselector
def get_locale(lang=None):
    supported_langs = current_app.config['LANGUAGES'].keys()
    new_lang = request.accept_languages.best_match(supported_langs, "en")
    # user = getattr(g, 'user', None)
    user = current_user
    if lang:
        if lang in supported_langs:
            new_lang = lang
        if user.is_authenticated():
            # set users preferred lang
            user.language = new_lang
            db.session.add(user)
            db.session.commit()
        else:
            session['locale'] = new_lang
    else:
        current_locale = getattr(g, 'locale', None)
        # return new_lang
        if current_locale:
            new_lang = current_locale
        elif user.is_authenticated():
            user_preferred_lang = getattr(user, 'language', None)
            if user_preferred_lang and user_preferred_lang in supported_langs:
                new_lang = user_preferred_lang
            else:
                # set users preferred lang
                user.language = new_lang
                db.session.add(user)
                db.session.commit()
        elif 'locale' in session:
            new_lang = session['locale']
        else:
            session['locale'] = new_lang
    
    return new_lang

@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone

###############################
# General views 
# ---------------------------
@app.after_request
def after_request(response):
    return response
    
@mod.route('/', methods=['GET', 'POST'])
def home():
    g.page_type = "home"
    return render_template("home.html")
    
@mod.route('upgrade/')
def upgrade():
    return render_template("general/upgrade.html")

@mod.route('access/')
@mod.route('access/logout/')
def access():
    session['has_access'] = False
    return redirect(url_for('general.home'))

###############################
# Set language views 
# ---------------------------
@mod.route('set_lang/<lang>/')
def set_lang(lang):
    g.locale = get_locale(lang)
    return redirect(request.args.get('next') or \
               request.referrer or \
               url_for('general.home'))

###############################
# Handle shortened URLs
# ---------------------------
@mod.route('<slug>/')
def redirect_short_url(slug):
    short = Short.query.filter_by(slug = slug).first_or_404()
    short.clicks += 1
    db.session.add(short)
    db.session.commit()
    
    return redirect(short.long_url)

###############################
# 404 view
# ---------------------------
@app.errorhandler(404)
def page_not_found(e):
    g.page_type = "error404"

    sabrina = {}
    sabrina["outfit"] = "lab"
    sabrina["face"] = "scared"
    sabrina["hat"] = None
    
    return render_template('general/404.html', 
        error = e, sabrina = sabrina), 404