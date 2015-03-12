import StringIO, csv
from flask import Blueprint, request, jsonify, Response
from dataviva import db
from dataviva.rais.models import Yb_rais, Yi, Yo, Ybi, Ybo, Yio, Ybio
from dataviva.utils import table_helper, query_helper
from dataviva.utils.gzip_data import gzipped
from dataviva import view_cache
from dataviva.utils.cached_query import api_cache_key

mod = Blueprint('rais', __name__, url_prefix='/rais')

@mod.route('/<year>/<bra_id>/<cnae_id>/<cbo_id>/')
@gzipped
@view_cache.cached(key_prefix=api_cache_key("rais"))
def rais_api(**kwargs):
    limit = int(kwargs.pop('limit', 0)) or int(request.args.get('limit', 0) )
    order = request.args.get('order', None) or kwargs.pop('order', None)
    sort = request.args.get('sort', None) or kwargs.pop('sort', 'desc')
    offset = request.args.get('offset', None) or kwargs.pop('offset', None)
    if order and "." in order:
        order, sort = order.split(".")
    # ignore_zeros = request.args.get('zeros', True) or kwargs.pop('zeros', True)
    serialize = request.args.get('serialize', None) or kwargs.pop('serialize', True)
    exclude = request.args.get('exclude', None) or kwargs.pop('exclude', None)
    download = request.args.get('download', None) or kwargs.pop('download', None)
    required_bras = request.args.get('required_bras', False) or kwargs.pop('required_bras', False)

    if exclude and "," in exclude:
        exclude = exclude.split(",")

    allowed_when_not, possible_tables = table_helper.prepare(['bra_id', 'cnae_id', 'cbo_id'], [ Yb_rais, Yi, Yo, Ybi, Ybo, Yio, Ybio ] )
    table = table_helper.select_best_table(kwargs, allowed_when_not, possible_tables)
    filters, groups, show_column = query_helper.build_filters_and_groups(table, kwargs, exclude=exclude)

    columns = []
    if not required_bras:
       columns = [c for c in table.__table__.columns if c.key != 'required_bras']

    results = query_helper.query_table(table, columns=columns, filters=filters, groups=groups, limit=limit, order=order, sort=sort, offset=offset, serialize=serialize)

    if required_bras and table is Ybi and results['data']:
        required_idx = results['headers'].index(Ybi.required_bras.key)
        bras = results['data'][0][required_idx]
        results = [bra.serialize() for bra in query_helper.bra_profiles(bras)]
        return jsonify(data=results)

    if table is Ybi:
        stripped_filters, stripped_groups, show_column2 = query_helper.convert_filters(Yi, kwargs, remove=['bra_id'])
        stripped_columns = [Yi.year, Yi.cnae_id, Yi.cbo_diversity, Yi.cbo_diversity_eff]
        diversity_results = query_helper.query_table(Yi, columns=stripped_columns, filters=stripped_filters, groups=stripped_groups, limit=limit, order=order, sort=sort, serialize=serialize)
        results["diversity"] = diversity_results
    elif table is Ybo:
        stripped_filters, stripped_groups, show_column2 = query_helper.convert_filters(Yo, kwargs, remove=['bra_id'])
        stripped_columns = [Yo.year, Yo.cbo_id, Yo.cnae_diversity, Yo.cnae_diversity_eff]
        diversity_results = query_helper.query_table(Yo, columns=stripped_columns, filters=stripped_filters, groups=stripped_groups, limit=limit, order=order, sort=sort, serialize=serialize)
        results["diversity"] = diversity_results

    if serialize or download:
        response = jsonify(results)
        if download:
            response.headers["Content-Disposition"] = "attachment;filename=rais_data.json"
        return response
    return results
