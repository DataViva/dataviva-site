# -*- coding: utf-8 -*-
import urllib2
import json
from datetime import datetime as dt
from sqlalchemy import func
from flask import Blueprint, request, render_template, g, Response, make_response, send_file, jsonify, redirect, url_for
from flask.ext.babel import gettext as _

from dataviva import db, view_cache, __year_range__
from dataviva.utils.cached_query import cached_query, api_cache_key
from dataviva.translations.dictionary import dictionary

from dataviva.apps.account.models import User, Starred
from dataviva.apps.general.views import get_locale
from dataviva.apps.embed.models import UI
from dataviva.api.attrs.models import Bra, Wld, Hs, Cnae, Cbo, University, Course_hedu, Course_sc


mod = Blueprint('data', __name__, url_prefix='/<lang_code>/data')


@mod.before_request
def before_request():
    g.page_type = mod.name
    g.color = "#1abbee"


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/')
def index():
    return render_template('data_download/index.html')
