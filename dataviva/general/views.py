from datetime import datetime
from flask import Blueprint, render_template, g, request, current_app, session, redirect, url_for, flash, abort, json
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.babel import gettext
from urlparse import urlparse
import time

mod = Blueprint('general', __name__, url_prefix='/<lang_code>')

from dataviva import app, db, babel, view_cache, data_api
from dataviva.general.forms import AccessForm
from dataviva.general.models import Short
from dataviva.account.models import User
from dataviva.attrs.models import Bra, Hs, Cbo, Cnae, Course_hedu
from dataviva.translations.dictionary import dictionary
from dataviva.stats.helper import stats_list, make_items

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

    if request.endpoint != 'static':
        url = urlparse(request.url)
        url_path = url.path.split('/')

        g.locale = get_locale(lang=url_path[1])

        if url_path[1] not in ['attrs', 'hedu', 'rais', 'sc', 'secex', 'stats']:
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
@view_cache.cached(key_prefix=api_cache_key("homepage"))
@gzipped
def home():

    # return render_template("test.html")

    g.page_type = "home"

    carousels = []

    limit = 20
    carousel_base = "/stats/carousel/?metric={}&show={}&profile={}&limit={}"

    metric, show, profile = "export_val", "bra_id", "bra"
    data = stats_list(metric, show, limit=limit)
    items = make_items(data, Bra)
    carousels.append({
        "title": gettext("Top Exporting Municipalities"),
        "type": profile,
        "items": items,
        "url" : carousel_base.format(metric, show, profile, limit),
        "metric" : metric
    })

    metric, show, profile = "pci", "hs_id", "hs"
    data = stats_list(metric, show, limit=limit)
    items = make_items(data, Hs)
    carousels.append({
        "title": gettext("Most Complex Products"),
        "sub": gettext("%(link)s for more information on product complexity.", link = "<a href='/about/glossary/complexity/'>{}</a>".format(gettext("Click here"))),
        "type": profile,
        "items": items,
        "url" : carousel_base.format(metric, show, profile, limit),
        "metric" : metric
    })

    metric, show, profile = "wage_avg", "bra_id", "bra"
    data = stats_list(metric, show, limit=limit)
    items = make_items(data, Bra)
    carousels.append({
        "title": gettext("Richest Municipalities"),
        "sub": gettext("Municipalities with the highest average wage, excluding those with less than 50,000 people."),
        "type": profile,
        "items": items,
        "url" : carousel_base.format(metric, show, profile, limit),
        "metric" : metric
    })

    metric, show, profile = "wage_avg", "cbo_id", "cbo"
    data = stats_list(metric, show, limit=limit)
    items = make_items(data, Cbo)
    carousels.append({
        "title": gettext("Best Paid Occupations"),
        "type": profile,
        "items": items,
        "url" : carousel_base.format(metric, show, profile, limit),
        "metric" : metric
    })

    metric, show, profile = "num_jobs", "cnae_id", "cnae"
    data = stats_list(metric, show, limit=limit)
    items = make_items(data, Cnae)
    carousels.append({
        "title": gettext("Largest Industries by Employment"),
        "type": profile,
        "items": items,
        "url" : carousel_base.format(metric, show, profile, limit),
        "metric" : metric
    })

    metric, show, profile = "num_emp_growth", "cnae_id", "cnae"
    data = stats_list(metric, show, limit=limit)
    items = make_items(data, Cnae)
    carousels.append({
        "title": gettext("Industries by Employment Growth"),
        "sub": gettext("Excluding industries with less than 10,000 employees."),
        "type": profile,
        "items": items,
        "url" : carousel_base.format(metric, show, profile, limit),
        "metric" : metric
    })

    metric, show, profile = "enrolled", "course_hedu_id", "course_hedu"
    data = stats_list(metric, show, limit=limit)
    items = make_items(data, Course_hedu)
    carousels.append({
        "title": gettext("Most Popular Courses by Enrollment"),
        "type": profile,
        "items": items,
        "url" : carousel_base.format(metric, show, profile, limit),
        "metric" : metric
    })

    metric, show, profile = "enrolled", "bra_id", "bra"
    data = stats_list(metric, show, limit=limit)
    items = make_items(data, Bra)
    carousels.append({
        "title": gettext("Cities by Largest University Enrollment"),
        "type": profile,
        "items": items,
        "url" : carousel_base.format(metric, show, profile, limit),
        "metric" : metric
    })

    return render_template("general/home.html", carousels = carousels)

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
