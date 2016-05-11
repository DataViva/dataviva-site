from flask import Blueprint, render_template, g
from flask.ext.babel import gettext
from dataviva.apps.general.views import get_locale
from flask.ext.login import login_required
from functools import wraps

mod = Blueprint('admin', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/admin')


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
@login_required
def index():
    return render_template('admin/index.html')
