from datetime import datetime
from flask import Blueprint, render_template, g, request, current_app, session, redirect, url_for, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.babel import gettext

mod = Blueprint('general', __name__, url_prefix='/')

from visual import app, db, babel
from visual.general.forms import AccessForm

###############################
# General functions for ALL views
# ---------------------------
@app.before_request
def before_request():
    
    # Check if the user has access (temp log in for development purposes)
    if 'has_access' not in session:
        session['has_access'] = False

    # test if the user has access!
    # if not session['has_access'] and request.endpoint and request.endpoint != "static":
    #     if request.endpoint == "general.home":
    #         form = AccessForm()
    #         if "pw" in request.form:
    #             if request.form["pw"] == "parabens":
    #                 session['has_access'] = True
    #             else:
    #                 return render_template("general/access.html", form=form)
    #         else:
    #             return render_template("general/access.html", form=form)
    #     else:
    #         return redirect(url_for("general.home"))
            
    # Save variable in session so we can determine if this is the user's
    # first time on the site
    if 'first_time' in session:
        session['first_time'] = False
    else:
        session['first_time'] = True
        flash("I've noticed it's your first time on the site. Welcome!")
    
    # Check if the user is logged in, if so give the global object
    # a reference to the user from DB
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
    
    # Set the locale to either 'pt' or 'en' on the global object
    g.locale = get_locale()

@babel.localeselector
def get_locale():
    supported_langs = current_app.config['LANGUAGES'].keys()
    user = getattr(g, 'user', None)
    locale = None
    if 'lang' in session:
        locale = session['lang']
    # if a user is logged in, use the locale from the user settings
    elif user is not None:
        lang = getattr(user, 'language', None)
        if lang is not None and lang in supported_langs:
            locale = lang
    # otherwise try to guess the language from the user accept
    # header the browser transmits. Supported languages are found
    # in config.py. The best match wins.
    if locale is None:
        locale = request.accept_languages.best_match(supported_langs)
    return locale

@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone

###############################
# General views 
# ---------------------------
@mod.before_request
def before_request():
    g.page_type = mod.name

@mod.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@mod.route('access/')
@mod.route('access/logout/')
def access():
    session['has_access'] = False
    return redirect(url_for('general.home'))

###############################
# Set language views 
# ---------------------------
@mod.route('set_lang/<lang>')
def set_lang(lang):
    supported_langs = current_app.config['LANGUAGES'].keys()
    user = getattr(g, 'user', None)
    if lang in supported_langs:
        session['lang'] = lang
    return redirect(url_for('general.home'))

###############################
# 404 view
# ---------------------------
@app.errorhandler(404)
def page_not_found(e):
    g.page_type = "error404"
    return render_template('general/404.html', error = e), 404
    
###############################
# Selector Snippit
# ---------------------------
@mod.route('selector/<category>/')
def guide_selector(category = None):        
    return render_template("general/selector.html",
        category = category)