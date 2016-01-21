import StringIO, csv
from flask import Blueprint, request, jsonify, Response
from dataviva import db
from dataviva.api.attrs.models import Bra
from dataviva.api.rais.models import Yb_rais, Yi, Yo, Ybi, Ybi_reqs, Ybo, Yio, Ybio
from dataviva.utils import table_helper, query_helper
from dataviva.utils.gzip_data import gzip_response
from dataviva import view_cache
from dataviva.utils.cached_query import api_cache_key
from dataviva.utils.csv_helper import gen_csv, is_download

mod = Blueprint('rais', __name__, url_prefix='/rais')

@mod.route('/<year>/<bra_id>/<cnae_id>/<cbo_id>/')
@view_cache.cached(key_prefix=api_cache_key("rais"), unless=is_download)
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

    if required_bras:
        bra_id = kwargs.get("bra_id")
        cnae_id = kwargs.get("cnae_id").split(".")[0]
        reqs = Ybi_reqs.query.filter(Ybi_reqs.bra_id == bra_id).filter(Ybi_reqs.cnae_id == cnae_id)
        year = kwargs.get("year")
        if year != "all":
            reqs = reqs.filter(Ybi_reqs.year == year)
        reqs = reqs.all()
        results = {}
        for req in reqs:
            bras = [Bra.query.get(b).serialize() for b in req.required_bras.split(",")]
            results[req.year] = bras
        return jsonify(data=results)

    if exclude and "," in exclude:
        exclude = exclude.split(",")

    allowed_when_not, possible_tables = table_helper.prepare(['bra_id', 'cnae_id', 'cbo_id'], [ Yb_rais, Yi, Yo, Ybi, Ybo, Yio, Ybio ] )
    table = table_helper.select_best_table(kwargs, allowed_when_not, possible_tables)
    filters, groups, show_column = query_helper.build_filters_and_groups(table, kwargs, exclude=exclude)

    results = query_helper.query_table(table, filters=filters, groups=groups, limit=limit, order=order, sort=sort, offset=offset, serialize=serialize)

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
            return gen_csv(results, "rais")
        return gzip_response(response)
    return results
