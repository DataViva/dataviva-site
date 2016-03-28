from sqlalchemy import func
from flask import Blueprint, render_template, g, redirect, url_for, \
    flash, request, jsonify, make_response
from flask.ext.login import login_required
from flask.ext.babel import gettext
from dataviva import db, app
from datetime import datetime
from dataviva.apps.general.views import get_locale
# models
from dataviva.apps.account.models import User
from dataviva.apps.ask.models import Question, Status, Reply, Flag, Vote
# forms
from dataviva.apps.admin.forms import AdminQuestionUpdateForm
from dataviva.utils.jinja_helpers import jinja_strip_html

# utils
from dataviva.utils import send_mail

from functools import wraps

# import urllib2, urllib
# from config import SITE_MIRROR

mod = Blueprint('admin', __name__, url_prefix='/<lang_code>/admin')


def get_current_user_role():
    return g.user.role


def required_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_current_user_role() not in roles:
                return gettext("You dont have permission to view this page.")
            return f(*args, **kwargs)
        return wrapped
    return wrapper


@mod.before_request
def before_request():
    g.page_type = mod.name


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.route('/')
def index():
    return 'admin'
