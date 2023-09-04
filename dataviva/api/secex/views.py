from flask import Blueprint, request, jsonify
from dataviva import db
from dataviva.apps.general.views import get_locale
from dataviva.api.secex.models import Ymb, Ymp, Ymbp, Ymbpw, Ymbw, Ympw, Ymw
from dataviva.utils import table_helper, query_helper
from dataviva.utils.gzip_data import gzip_response
from dataviva import view_cache
from dataviva.utils.cached_query import api_cache_key
from dataviva.utils.csv_helper import gen_csv, is_download

mod = Blueprint('secex', __name__, url_prefix='/secex')

@mod.route('/<year>/<bra_id>/<hs_id>/<wld_id>/')
@mod.route('/<year>-<month>/<bra_id>/<hs_id>/<wld_id>/')
def secex_api(**kwargs):
    limit = int(kwargs.pop('limit', 0)) or int(request.args.get('limit', 0) )
    order = request.args.get('order', None) or kwargs.pop('order', None)
    sort = request.args.get('sort', None) or kwargs.pop('sort', 'desc')
    offset = request.args.get('offset', None) or kwargs.pop('offset', None)
    if order and "." in order:
        order, sort = order.split(".")
    ignore_zeros = request.args.get('zeros', False) or kwargs.pop('zeros', False)
    serialize = request.args.get('serialize', None) or kwargs.pop('serialize', True)
    exclude = request.args.get('exclude', None) or kwargs.pop('exclude', None)
    download = request.args.get('download', None) or kwargs.pop('download', None)

    if not "month" in kwargs:
        kwargs["month"] = query_helper.ALL

    if exclude and "," in exclude:
        exclude = exclude.split(",")

    tables = [Ymw, Ymp, Ymb, Ympw, Ymbw, Ymbp, Ymbpw]
    allowed_when_not, possible_tables = table_helper.prepare(['bra_id', 'hs_id', 'wld_id'], tables)
    table = table_helper.select_best_table(kwargs, allowed_when_not, possible_tables)

    filters, groups, show_column = query_helper.build_filters_and_groups(table, kwargs, exclude=exclude)

    # if ignore_zeros:
        # filters.append( getattr(table, "val_usd") > 0 )
    results = query_helper.query_table(table, filters=filters, groups=groups, limit=limit, order=order, sort=sort, offset=offset, serialize=serialize)

    if table is Ymbp:
        stripped_filters, stripped_groups, show_column2 = query_helper.convert_filters(Ymp, kwargs, remove=['bra_id', 'month'])
        stripped_columns = [Ymp.year, Ymp.hs_id, Ymp.pci]
        stripped_filters.append(Ymp.month == 0)
        tmp = query_helper.query_table(Ymp, columns=stripped_columns, filters=stripped_filters, groups=stripped_groups, serialize=serialize)
        results["pci"] = tmp

        stripped_filters, stripped_groups, show_column2 = query_helper.convert_filters(Ymb, kwargs, remove=['hs_id', 'month'])
        stripped_columns = [Ymb.year, Ymb.bra_id, Ymb.eci]
        stripped_filters.append(Ymb.month == 0)
        tmp = query_helper.query_table(Ymp, columns=stripped_columns, filters=stripped_filters, groups=stripped_groups, serialize=serialize)
        tmp = {d[0]: d[2] for d in tmp["data"]}
        results["eci"] = tmp

    if serialize or download:
        response = jsonify(results)
        if download:
            return gen_csv(results, "secex")
        return gzip_response(response)

    return results
