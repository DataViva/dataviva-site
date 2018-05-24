import os
from importlib import import_module

# general flask library
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.babel import Babel
from flask.ext.cache import Cache
from flask.ext.mail import Mail

from utils.jinja_helpers import jinja_formatter, jinja_momentjs, jinja_split, \
    jinja_strip_html, max_digits, jinja_magnitude, ordinal

from utils.redis import RedisSessionInterface
from dataviva.api.stats.util import get_or_set_years


''' Base directory of where the site is held '''
datavivadir = os.path.abspath(os.path.dirname(__file__))

# Initialize app
app = Flask(__name__, template_folder=os.path.join(datavivadir, 'templates'),
            static_folder=os.path.join(datavivadir, 'static'))

app.config.from_object('config')
mail = Mail(app)
db = SQLAlchemy(app)

lm = LoginManager()
lm.login_view = "/session/login"
lm.init_app(app)

babel = Babel(app)

app.jinja_env.globals['moment_js'] = jinja_momentjs
app.jinja_env.globals['format'] = jinja_formatter
app.jinja_env.filters['strip_html'] = jinja_strip_html
app.jinja_env.filters['split'] = jinja_split
app.jinja_env.filters['max_digits'] = max_digits
app.jinja_env.filters['magnitude'] = jinja_magnitude
app.jinja_env.filters['ordinal'] = ordinal


def get_env_variable(var_name, default=-1):
    try:
        return os.environ[var_name]
    except KeyError:
        if default != -1:
            return default
        error_msg = "Set the %s os.environment variable" % var_name
        raise Exception(error_msg)


cache_prefix = get_env_variable("DATAVIVA_REDIS_PREFIX", "dv2016:")
cache_timeout = get_env_variable("DATAVIVA_REDIS_TIMEOUT", 60000000)
s3_host = get_env_variable("S3_HOST", 'https://dataviva.s3.amazonaws.com')
s3_bucket = get_env_variable("S3_BUCKET", 'dataviva-dev')
admin_email = get_env_variable("ADMINISTRATOR_EMAIL", 'contato@dataviva.info')
test_user_email = get_env_variable("TEST_USER_EMAIL","")
test_user_password = get_env_variable("TEST_USER_PASSWORD","")

view_cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_KEY_PREFIX': cache_prefix,
    'CACHE_DEFAULT_TIMEOUT': cache_timeout,
    'CACHE_REDIS_HOST': get_env_variable("DATAVIVA_REDIS_HOST", "localhost"),
    'CACHE_REDIS_PORT': get_env_variable("DATAVIVA_REDIS_PORT", 6379),
    'CACHE_REDIS_PASSWORD': get_env_variable("DATAVIVA_REDIS_PW", None),
    'CACHE_REDIS_DB': get_env_variable("DATAVIVA_REDIS_DB", 0),
})

redis_sesh = RedisSessionInterface(view_cache, "session:")
if redis_sesh.redis:
    app.session_interface = redis_sesh

__year_range__ = get_or_set_years(view_cache, "general:data_years")

data_viva_apis = [api_module for api_module in os.listdir(
    os.getcwd()+'/dataviva/api') if '.' not in api_module]
data_viva_modules = [app_module for app_module in os.listdir(
    os.getcwd()+'/dataviva/apps') if '.' not in app_module]

for api_module in data_viva_apis:
    views = import_module('dataviva.api.'+api_module+'.views')
    app.register_blueprint(views.mod)

for app_module in data_viva_modules:
    views = import_module('dataviva.apps.'+app_module+'.views')
    app.register_blueprint(views.mod)
