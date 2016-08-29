from datetime import datetime
from flask import Blueprint, render_template, g, request, current_app, session, redirect, url_for, flash, abort, json
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.babel import gettext
from urlparse import urlparse
from random import randrange
import time

mod = Blueprint('general', __name__, url_prefix='/<lang_code>')

from dataviva import app, db, babel, view_cache, data_viva_apis, s3_host, s3_bucket
from dataviva.apps.general.forms import AccessForm
from dataviva.apps.general.models import Short
from dataviva.apps.user.models import User
from dataviva.apps.news.models import Publication
from dataviva.apps.blog.models import Post
from dataviva.apps.contact.forms import ContactForm
from dataviva.apps.user.forms import SignupForm
from dataviva.apps.user.forms import LoginForm

from dataviva.api.attrs.models import Bra, Hs, Cbo, Cnae, Course_hedu
from dataviva.translations.dictionary import dictionary
from dataviva.api.stats.helper import stats_list, make_items

from dataviva.utils.cached_query import cached_query, api_cache_key
from dataviva.utils.gzip_data import gzipped

from config import ACCOUNTS, DEBUG

#utils
# from dataviva.utils.send_mail import send_mail

###############################
# General functions for ALL views
# ---------------------------
@app.before_request
def before_request():

    g.user = current_user
    g.accounts = True if ACCOUNTS in ["True","true","Yes","yes","Y","y",1] else False
    g.color = "#af1f24"
    g.dictionary = json.dumps(dictionary())
    g.attr_version = 15
    g.production = False if DEBUG else True
    g.contact_form = ContactForm()
    g.signup_form = SignupForm()
    g.signin_form = LoginForm()
    g.s3_host = s3_host
    g.s3_bucket = s3_bucket

    if request.endpoint != 'static':
        url = urlparse(request.url)
        url_path = url.path.split('/')

        g.locale = get_locale(lang=url_path[1])

        # Check if the user is logged in, if so give the global object
        # a reference to the user from DB
        # if g.user.is_authenticated:
        #     g.user.last_seen = datetime.utcnow()
        #     db.session.add(g.user)
        #     db.session.commit()

        if url_path[1] not in data_viva_apis:
            if g.locale not in url_path:
                if url.query:
                    new_url= "{}://{}/{}{}?{}".format(url.scheme, url.netloc, g.locale, url.path, url.query)
                else:
                    new_url= "{}://{}/{}{}".format(url.scheme, url.netloc, g.locale, url.path)
                return redirect(new_url)


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')

@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())

@babel.localeselector
def get_locale(lang=None):
    supported_langs = current_app.config['LANGUAGES'].keys()
    new_lang = request.accept_languages.best_match(supported_langs, "en")
    # user = getattr(g, 'user', None)
    user = current_user
    if lang:
        if lang in supported_langs:
            new_lang = lang
        # if user.is_authenticated:
        #     # set users preferred lang
        #     user.language = new_lang
        #     db.session.add(user)
        #     db.session.commit()
        else:
            session['locale'] = new_lang
    else:
        current_locale = getattr(g, 'locale', None)
        # return new_lang
        if current_locale:
            new_lang = current_locale
        elif user.is_authenticated:
            user_preferred_lang = getattr(user, 'language', None)
            if user_preferred_lang and user_preferred_lang in supported_langs:
                new_lang = user_preferred_lang
            else:
                # set users preferred lang
                user.language = new_lang
                #db.session.add(user)
                # db.session.commit()
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

@mod.route('/', methods=['GET'])
def home():
    g.page_type = 'home'

    news_publications = Publication.query.filter(Publication.id != id, Publication.active, Publication.show_home).all()
    blog_posts = Post.query.filter(Post.id != id, Post.active, Post.show_home).all()

    news_publications += blog_posts

    all_publications = sorted(news_publications, key=lambda x: x.publish_date, reverse=True)

    if len(all_publications) > 6:
        all_publications = all_publications[0:6]

    return render_template("general/index.html", publications=all_publications)


@mod.route('/inicie-uma-pesquisa/', methods=['GET'])
def search():
    g.page_type = 'search'
    return render_template("general/browse_categories.html")


@mod.route('close/')
def close():
    return render_template("general/close.html")

@mod.route('upgrade/')
def upgrade():
    return render_template("general/upgrade.html")


###############################
# Set language views
# ---------------------------
@mod.route('set_lang/<lang>')
def set_lang(lang):
    g.locale = get_locale(lang)
    return redirect(request.args.get('next') or \
               request.referrer or \
               url_for('general.home'))

###############################
# Handle shortened URLs
# ---------------------------
@mod.route('/<slug>/')
def redirect_short_url(slug):
    short = Short.query.filter_by(slug = slug).first_or_404()
    short.clicks += 1
    # db.session.add(short)
    db.session.commit()

    return redirect(short.long_url)

# ###############################
# # 404 view
# # ---------------------------
if not DEBUG:
    @app.errorhandler(Exception)
    @app.errorhandler(404)
    @app.errorhandler(500)
    @mod.route('413/')
    def page_not_found(e="413"):

        error = str(e).split(":")[0]
        try:
            error_code = int(error)
        except:
            error = "500"
            error_code = int(error)

        request_info = {
            "Date": datetime.today().ctime(),
            "IP": request.remote_addr,
            "Method": request.method,
            "URL": request.url,
            "Data": request.data
        }

        headers = list(request.headers)

        g.page_type = "error"

        sabrina = {}
        sabrina["outfit"] = "lab"
        sabrina["face"] = "scared"
        sabrina["hat"] = None

        return render_template('general/error.html',
            error = error, sabrina = sabrina), error_code

@mod.route('contact/')
def contact():
    return render_template("general/contact.html")


@mod.route('/error/')
def error():
        g.page_type = "error"

        sabrina = {}
        sabrina["outfit"] = "lab"
        sabrina["face"] = "scared"
        sabrina["hat"] = None

        error = "500"
        error_code = int(error)

        return render_template('general/error.html',
            error = error, sabrina = sabrina), error_code
