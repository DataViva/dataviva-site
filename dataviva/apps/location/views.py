# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.services import Location as LocationService
from dataviva.api.secex.models import Ymb
from dataviva.api.secex.services import Location as LocationBodyService
from sqlalchemy import desc

mod = Blueprint('location', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/location',
                static_folder='static')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/<bra_id>')
def index(bra_id):

    location_service = LocationService(bra_id=bra_id)
    location_body_service = LocationBodyService(bra_id=bra_id)

    ''' Query básica para SECEX'''
    eci = Ymb.query.filter_by(bra_id=bra_id, month=0) \
        .order_by(desc(Ymb.year)).limit(1).first().eci

    header = {
        'name': location_service.name(),
        'bra_id' : bra_id[:3],
        'gdp': location_service.gdp(),
        'life_expectation': location_service.life_expectation(),
        'population': location_service.population(),
        'gdp_per_capita': location_service.gdp_per_capita(),
        'hdi': location_service.hdi(),
        'eci': eci,
    }

    body = {
        'main_product_by_export_value' : location_body_service.main_product_by_export_value()
        #'main_product_by_export_value_name' : location_body_service.main_product_by_export_value_name()


    }

    return render_template('location/index.html',
                           header=header, body=body)
