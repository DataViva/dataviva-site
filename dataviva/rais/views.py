import StringIO, csv
from flask import Blueprint, request, render_template, flash, g, session, \
            redirect, url_for, jsonify, make_response, Response
from dataviva import db

from dataviva.rais.models import Yb_rais, Yi, Yo, Ybi, Ybo, Yio, Ybio
from dataviva.utils import table_helper, query_helper
from dataviva.utils.gzip_data import gzipped
from dataviva.utils.decorators import cache_api
mod = Blueprint('rais', __name__, url_prefix='/rais')

@mod.route('/<year>/<bra_id>/<cnae_id>/<cbo_id>/')
@gzipped
# @cache_api('rais')
def rais_api(**kwargs):
    limit = int(kwargs.pop('limit', 0)) or int(request.args.get('limit', 0) )
    order = request.args.get('order', None) or kwargs.pop('order', None)
    sort = request.args.get('sort', None) or kwargs.pop('sort', 'desc')
    # ignore_zeros = request.args.get('zeros', True) or kwargs.pop('zeros', True)
    serialize = request.args.get('serialize', None) or kwargs.pop('serialize', True)
    exclude = request.args.get('exclude', None) or kwargs.pop('exclude', None)
    if exclude and "," in exclude:
        exclude = exclude.split(",")

    # -- 1. filter ALLs
    kwargs = {k:v for k,v in kwargs.items() if v != table_helper.ALL}
    # -- 2. select table
    allowed_when_not, possible_tables = table_helper.prepare(['bra_id', 'cnae_id', 'cbo_id'], [ Yb_rais, Yi, Yo, Ybi, Ybo, Yio, Ybio ] )
    table = table_helper.select_best_table(kwargs, allowed_when_not, possible_tables)
    filters, groups, show_column = query_helper.build_filters_and_groups(table, kwargs, exclude=exclude)

    results = query_helper.query_table(table, filters=filters, groups=groups, limit=limit, order=order, sort=sort, serialize=serialize)

    if table is Ybi:
        stripped_filters, stripped_groups, show_column2 = query_helper.convert_filters(Yi, kwargs, remove=['bra_id'])
        stripped_columns = [Yi.year, Yi.cnae_id, Yi.cbo_diversity, Yi.cbo_diversity_eff]
        diversity_results = query_helper.query_table(Yi, columns=stripped_columns, filters=stripped_filters, groups=stripped_groups, limit=limit, order=order, sort=sort, serialize=serialize)
        results["diversity"] = diversity_results
    elif table is Ybo:
        stripped_filters, stripped_groups, show_column2 = query_helper.convert_filters(Yi, kwargs, remove=['bra_id'])
        stripped_columns = [Yo.year, Yo.cbo_id, Yo.cnae_diversity, Yo.cnae_diversity_eff]
        diversity_results = query_helper.query_table(Yo, columns=stripped_columns, filters=stripped_filters, groups=stripped_groups, limit=limit, order=order, sort=sort, serialize=serialize)
        results["diversity"] = diversity_results

    if serialize:
        return jsonify(results)

    return results
