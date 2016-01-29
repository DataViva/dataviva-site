import os

# general flask library
from flask import Flask
# flask-sqlalchemy connector for database queries
from flask.ext.sqlalchemy import SQLAlchemy
# flask-login for managing users
from flask.ext.login import LoginManager
# flask-babel for handling L18n and L10n
from flask.ext.babel import Babel

# flask-cache for caching
from flask.ext.cache import Cache

# for new filters, redis sessions
from flask.ext.mail import Mail
from utils.jinja_helpers import jinja_formatter, jinja_momentjs, jinja_split, \
 jinja_strip_html

from utils.redis import RedisSessionInterface


def get_env_variable(var_name, default=-1):
    try:
        return os.environ[var_name]
    except KeyError:
        if default != -1:
            return default
        error_msg = "Set the %s os.environment variable" % var_name
        raise Exception(error_msg)

''' Base directory of where the site is held '''
datavivadir = os.path.abspath(os.path.dirname(__file__))

# Initialize app
app = Flask(__name__, template_folder=os.path.join(datavivadir, 'templates'),
            static_folder=os.path.join(datavivadir, 'static'))

# Load default configuration from config.py
app.config.from_object('config')

mail = Mail(app)

# DB connection object
db = SQLAlchemy(app)

cache_prefix = get_env_variable("DATAVIVA_REDIS_PREFIX", "dv2015:")
cache_timeout = get_env_variable("DATAVIVA_REDIS_TIMEOUT", 60000000)

# Initialize cache for views
view_cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_KEY_PREFIX': cache_prefix,
    'CACHE_DEFAULT_TIMEOUT': cache_timeout,
    'CACHE_REDIS_HOST': get_env_variable("DATAVIVA_REDIS_HOST", "localhost"),
    'CACHE_REDIS_PORT': get_env_variable("DATAVIVA_REDIS_PORT", 6379),
    'CACHE_REDIS_PASSWORD': get_env_variable("DATAVIVA_REDIS_PW", None)
})

# Set session store as server side (Redis)
redis_sesh = RedisSessionInterface(view_cache, "session:")
if redis_sesh.redis:
    app.session_interface = redis_sesh

# Global Latest Year Variables
from dataviva.api.stats.util import get_or_set_years
__year_range__ = get_or_set_years(view_cache, "general:data_years")

# login manager for user management
lm = LoginManager()
lm.init_app(app)

# babel configuration for lang support
babel = Babel(app)

# add a few extra template filters to jinja
app.jinja_env.globals['moment_js'] = jinja_momentjs
app.jinja_env.globals['format'] = jinja_formatter
app.jinja_env.filters['strip_html'] = jinja_strip_html
app.jinja_env.filters['split'] = jinja_split

# Load the modules for each different section of the site

''' data API view/models '''
data_api = ['attrs', 'hedu', 'rais', 'sc', 'secex', 'stats']
from dataviva.api.attrs.views import mod as attrs_module
from dataviva.api.hedu.views import mod as hedu_module
from dataviva.api.rais.views import mod as rais_module
from dataviva.api.sc.views import mod as sc_module
from dataviva.api.secex.views import mod as secex_module
from dataviva.api.stats.views import mod as stats_module

''' front facing views/models of site '''
from dataviva.apps.about.views import mod as about_module
from dataviva.apps.account.views import mod as account_module
from dataviva.apps.admin.views import mod as admin_module
from dataviva.apps.ask.views import mod as ask_module
from dataviva.apps.basic_course.views import mod as basic_course_module
from dataviva.apps.data.views import mod as data_module
from dataviva.apps.general.views import mod as general_module
from dataviva.apps.graphs.views import mod as graphs_module
from dataviva.apps.location.views import mod as location_module
from dataviva.apps.product.views import mod as product_module
from dataviva.apps.occupation.views import mod as occupation_module
from dataviva.apps.trade_partner.views import mod as trade_partner_module
from dataviva.apps.rankings.views import mod as rankings_module
from dataviva.apps.university.views import mod as university_module
from dataviva.apps.wizard.views import mod as wizard_module
from dataviva.apps.industry.views import mod as industry_module


''' Register these modules as blueprints '''
app.register_blueprint(attrs_module)
app.register_blueprint(hedu_module)
app.register_blueprint(rais_module)
app.register_blueprint(sc_module)
app.register_blueprint(secex_module)
app.register_blueprint(stats_module)
app.register_blueprint(general_module)
app.register_blueprint(admin_module)
app.register_blueprint(account_module)
app.register_blueprint(graphs_module)
app.register_blueprint(data_module)
app.register_blueprint(ask_module)
app.register_blueprint(rankings_module)
app.register_blueprint(about_module)
app.register_blueprint(location_module)
app.register_blueprint(product_module)
app.register_blueprint(occupation_module)
app.register_blueprint(trade_partner_module)
app.register_blueprint(university_module)
app.register_blueprint(wizard_module)
app.register_blueprint(basic_course_module)
app.register_blueprint(industry_module)
