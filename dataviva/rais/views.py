import StringIO, csv
from flask import Blueprint, request, render_template, flash, g, session, \
            redirect, url_for, jsonify, make_response, Response
from dataviva import db
from dataviva.utils.make_query import make_query
from dataviva.rais.models import Yb_rais, Yi, Yo, Ybi, Ybo, Yio, Ybio

mod = Blueprint('rais', __name__, url_prefix='/rais')

import time

timing = []

RESULTS_PER_PAGE = 40

@mod.errorhandler(404)
def page_not_found(error):
    return error, 404

@mod.after_request
def per_request_callbacks(response):
    if response.status_code != 302 and response.mimetype != "text/csv":
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = str(len(response.data))
    return response

############################################################
# ----------------------------------------------------------
# 2 variable views
# 
############################################################

@mod.route('/all/<bra_id>/all/all/')
@mod.route('/<year>/<bra_id>/all/all/')
def rais_yb(**kwargs):
    return make_response(make_query(Yb_rais, request.args, g.locale, **kwargs))

@mod.route('/all/all/<isic_id>/all/')
@mod.route('/<year>/all/<isic_id>/all/')
def rais_yi(**kwargs):
    return make_response(make_query(Yi, request.args, g.locale, **kwargs))

@mod.route('/all/all/all/<cbo_id>/')
@mod.route('/<year>/all/all/<cbo_id>/')
def rais_yo(**kwargs):
    return make_response(make_query(Yo, request.args, g.locale, **kwargs))

############################################################
# ----------------------------------------------------------
# 3 variable views
# 
############################################################

@mod.route('/all/<bra_id>/<isic_id>/all/')
@mod.route('/<year>/<bra_id>/<isic_id>/all/')
def rais_ybi(**kwargs):
    kwargs["join"] = [{
                        "table": Yi,
                        "columns": ["cbo_diversity","cbo_diversity_eff"],
                        "on": ["year", "isic_id"]
                    }]
    return make_response(make_query(Ybi, request.args, g.locale, **kwargs))

@mod.route('/all/<bra_id>/all/<cbo_id>/')
@mod.route('/<year>/<bra_id>/all/<cbo_id>/')
def rais_ybo(**kwargs):
    kwargs["join"] = [{
                        "table": Yo,
                        "columns": ["isic_diversity","isic_diversity_eff"],
                        "on": ["year", "cbo_id"]
                    }]
    return make_response(make_query(Ybo, request.args, g.locale, **kwargs))

@mod.route('/all/all/<isic_id>/<cbo_id>/')
@mod.route('/<year>/all/<isic_id>/<cbo_id>/')
def rais_yio(**kwargs):
    return make_response(make_query(Yio, request.args, g.locale, **kwargs))

############################################################
# ----------------------------------------------------------
# 4 variable views
# 
############################################################

@mod.route('/all/<bra_id>/<isic_id>/<cbo_id>/')
@mod.route('/<year>/<bra_id>/<isic_id>/<cbo_id>/')
def rais_ybio(**kwargs):
    return make_response(make_query(Ybio, request.args, g.locale, **kwargs))