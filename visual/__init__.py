import os
from os import environ

# general flask library
from flask import Flask
# flask-sqlalchemy connector for database queries
from flask.ext.sqlalchemy import SQLAlchemy
# flask-login for managing users
from flask.ext.login import LoginManager
# flask-babel for handling L18n and L10n
from flaskext.babel import Babel
# for new filters, redis sessions
from utils import Momentjs, strip_html, jinja_split, RedisSessionInterface

''' Base directory of where the site is held '''
visualdir = os.path.abspath(os.path.dirname(__file__))

# Initialize app
app = Flask(__name__, template_folder=os.path.join(visualdir, 'html'))

# Load default configuration from config.py
app.config.from_object('config')

# DB connection object
db = SQLAlchemy(app)

# Set session store as server side (Redis)
app.session_interface = RedisSessionInterface()

# login manager for user management
lm = LoginManager()
lm.setup_app(app)

# babel configuration for lang support
babel = Babel(app)

# add a few extra template filters to jinja
app.jinja_env.globals['momentjs'] = Momentjs
app.jinja_env.filters['strip_html'] = strip_html
app.jinja_env.filters['split'] = jinja_split

# Load the modules for each different section of the site
''' data API view/models '''
from visual.attrs.views import mod as attrs_module
from visual.secex.views import mod as secex_module
from visual.rais.views import mod as rais_module
''' front facing views/models of site '''
from visual.general.views import mod as general_module
from visual.admin.views import mod as admin_module
from visual.account.views import mod as account_module
from visual.apps.views import mod as apps_module
from visual.guide.views import mod as guide_module
from visual.data.views import mod as data_module
from visual.ask.views import mod as ask_module
from visual.about.views import mod as about_module
from visual.explore.views import mod as explore_module

''' Register these modules as blueprints '''
app.register_blueprint(attrs_module)
app.register_blueprint(secex_module)
app.register_blueprint(rais_module)

app.register_blueprint(general_module)
app.register_blueprint(admin_module)
app.register_blueprint(account_module)
app.register_blueprint(apps_module)
app.register_blueprint(guide_module)
app.register_blueprint(data_module)
app.register_blueprint(ask_module)
app.register_blueprint(about_module)
app.register_blueprint(explore_module)
