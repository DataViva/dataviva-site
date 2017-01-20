# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request, abort
from dataviva.apps.general.views import get_locale
import urllib

mod = Blueprint('stacked', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/stacked',
                static_folder='static')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/<dataset>/<area>')
def index(dataset, area):
    filters = urllib.urlencode([("product",request.args.get("product"))])

    import pdb; pdb.set_trace()
    return render_template('stacked/index.html', dataset=dataset, area=area, filters=filters)
