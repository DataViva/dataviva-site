import os
from importlib import import_module

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
    jinja_strip_html, max_digits, jinja_magnitude

from utils.redis import RedisSessionInterface
from dataviva.api.stats.util import get_or_set_years


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
__year_range__ = get_or_set_years(view_cache, "general:data_years")


lm = LoginManager()
lm.login_view = "/account/signin"
lm.init_app(app)

# babel configuration for lang support
babel = Babel(app)

# add a few extra template filters to jinja
app.jinja_env.globals['moment_js'] = jinja_momentjs
app.jinja_env.globals['format'] = jinja_formatter
app.jinja_env.filters['strip_html'] = jinja_strip_html
app.jinja_env.filters['split'] = jinja_split
app.jinja_env.filters['max_digits'] = max_digits
app.jinja_env.filters['magnitude'] = jinja_magnitude


# Load the modules for each different section of the site
data_viva_apis = [api_module for api_module in os.listdir(os.getcwd()+'/dataviva/api') if '.' not in api_module]
data_viva_modules = [app_module for app_module in os.listdir(os.getcwd()+'/dataviva/apps') if '.' not in app_module]


for api_module in data_viva_apis:
    views = import_module('dataviva.api.'+api_module+'.views')
    app.register_blueprint(views.mod)

for app_module in data_viva_modules:
    views = import_module('dataviva.apps.'+app_module+'.views')
    app.register_blueprint(views.mod)
