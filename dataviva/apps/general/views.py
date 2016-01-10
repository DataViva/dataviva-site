from datetime import datetime
from flask import Blueprint, render_template, g, request, current_app, session, redirect, url_for, flash, abort, json
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.babel import gettext
from urlparse import urlparse
import time

mod = Blueprint('general', __name__, url_prefix='/<lang_code>')

from dataviva import app, db, babel, view_cache, data_api
from dataviva.apps.general.forms import AccessForm
from dataviva.apps.general.models import Short
from dataviva.apps.account.models import User
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
    g.page_type = mod.name
    g.dictionary = json.dumps(dictionary())
    g.attr_version = 14
    g.production = False if DEBUG else True

    if request.endpoint != 'static':
        url = urlparse(request.url)
        url_path = url.path.split('/')

        g.locale = get_locale(lang=url_path[1])

        # Check if the user is logged in, if so give the global object
        # a reference to the user from DB
        if g.user.is_authenticated:
            g.user.last_seen = datetime.utcnow()
            db.session.add(g.user)
            db.session.commit()

        if url_path[1] not in data_api:
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
        if user.is_authenticated:
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
        elif user.is_authenticated:
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


@mod.route('/', methods=['GET'])
@view_cache.cached(key_prefix=api_cache_key("homepage"))
def home():
    return render_template("general/index.html")


@mod.route('/inicie-uma-pesquisa/', methods=['GET'])
@view_cache.cached(key_prefix=api_cache_key("browsecat"))
def browse_categories():
    return render_template("general/browse_categories.html")


@mod.route('close/')
def close():
    return render_template("general/close.html")

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
    db.session.add(short)
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

        # allowed = True
        # requester = request.headers.get("from")
        # if requester:
        #   if "googlebot" in requester:
        #     allowed = False
        #
        # if "fancybox" in request.url:
        #   allowed = False
        #
        # if allowed and error_code != 404:
        #     admins = User.query.filter(User.role == 1).filter(User.email != "").filter(User.agree_mailer == 1).all()
        #     emails = [str(getattr(a,"email")) for a in admins]
        #
        #     if len(emails) > 0:
        #         subject = "DataViva Error: "+error
        #
        #         if e == "413":
        #             request_info["URL"] = ''
        #             error_text = "413: Request entity too large"
        #         else:
        #             error_text = str(e)
        #
        #         send_mail(subject, emails,
        #             render_template('admin/mail/error.html', title=subject,
        #             error=error_text, request_info=request_info, headers=headers))

        g.page_type = "error"

        sabrina = {}
        sabrina["outfit"] = "lab"
        sabrina["face"] = "scared"
        sabrina["hat"] = None

        return render_template('general/error.html',
            error = error, sabrina = sabrina), error_code
