import os
from os import environ

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
from utils.jinja_helpers import jinja_momentjs, jinja_formatter, jinja_strip_html, jinja_split
from utils.redis import RedisSessionInterface
from flask.ext.mail import Mail

''' Base directory of where the site is held '''
datavivadir = os.path.abspath(os.path.dirname(__file__))

# Initialize app
app = Flask(__name__, template_folder=os.path.join(datavivadir, 'html'))



# Load default configuration from config.py
app.config.from_object('config')

mail = Mail(app)

# DB connection object
db = SQLAlchemy(app)

# Initialize cache for views
view_cache = Cache(app, config={'CACHE_TYPE': 'redis', \
                'CACHE_REDIS_HOST':'localhost', 'CACHE_REDIS_PORT':6379, \
                'CACHE_REDIS_PASSWORD':None})

# Set session store as server side (Redis)
redis_sesh = RedisSessionInterface()
if redis_sesh.redis:
    app.session_interface = redis_sesh

# Global Latest Year Variables
__latest_year__ = {"secex": 2014, "rais": 2002, "population": 2012}

# login manager for user management
lm = LoginManager()
lm.setup_app(app)

# babel configuration for lang support
babel = Babel(app)

# add a few extra template filters to jinja
app.jinja_env.globals['moment_js'] = jinja_momentjs
app.jinja_env.globals['format'] = jinja_formatter
app.jinja_env.filters['strip_html'] = jinja_strip_html
app.jinja_env.filters['split'] = jinja_split

# Load the modules for each different section of the site
''' data API view/models '''
from dataviva.attrs.views import mod as attrs_module
from dataviva.secex_export.views import mod as secex_export_module
from dataviva.secex_import.views import mod as secex_import_module
from dataviva.rais.views import mod as rais_module
from dataviva.hedu.views import mod as hedu_module
''' front facing views/models of site '''
from dataviva.general.views import mod as general_module
from dataviva.admin.views import mod as admin_module
from dataviva.account.views import mod as account_module
from dataviva.apps.views import mod as apps_module
from dataviva.guide.views import mod as guide_module
from dataviva.data.views import mod as data_module
from dataviva.ask.views import mod as ask_module
from dataviva.rankings.views import mod as rankings_module
from dataviva.about.views import mod as about_module
from dataviva.profiles.views import mod as profiles_module

''' Register these modules as blueprints '''
app.register_blueprint(attrs_module)
app.register_blueprint(secex_export_module)
app.register_blueprint(secex_import_module)
app.register_blueprint(rais_module)
app.register_blueprint(hedu_module)

app.register_blueprint(general_module)
app.register_blueprint(admin_module)
app.register_blueprint(account_module)
app.register_blueprint(apps_module)
app.register_blueprint(guide_module)
app.register_blueprint(data_module)
app.register_blueprint(ask_module)
app.register_blueprint(rankings_module)
app.register_blueprint(about_module)
app.register_blueprint(profiles_module)
