from flask import Blueprint, request, jsonify
from dataviva import db
import dataviva.secex_import.models as secex_import
from dataviva.secex_import.models import *
from dataviva.secex_export.models import Yp as Yp_export
from dataviva.utils import table_helper, query_helper
from dataviva.utils.gzip_data import gzipped
from dataviva.utils.decorators import cache_api
import dataviva

mod = Blueprint('secex_import', __name__, url_prefix='/secex_import')

@mod.route('/<year>/<bra_id>/<hs_id>/<wld_id>/')
@gzipped
# @cache_api('secex')
def secex_api(**kwargs):
    limit = int(kwargs.pop('limit', 0)) or int(request.args.get('limit', 0) )
    order = request.args.get('order', None) or kwargs.pop('order', None)
    sort = request.args.get('sort', None) or kwargs.pop('sort', 'desc')
    ignore_zeros = request.args.get('zeros', False) or kwargs.pop('zeros', False)
    serialize = request.args.get('serialize', None) or kwargs.pop('serialize', True)
    exclude = request.args.get('exclude', None) or kwargs.pop('exclude', None)
    download = request.args.get('download', None) or kwargs.pop('download', None)

    if exclude and "," in exclude:
        exclude = exclude.split(",")

    # -- 1. filter ALLs
    kwargs = {k:v for k,v in kwargs.items() if v != table_helper.ALL}
    # -- 2. select table

    allowed_when_not, possible_tables = table_helper.prepare(['bra_id', 'hs_id', 'wld_id'], [Yb_import, Yp_import, Yw_import, Ybw_import, Ybp_import, Ypw_import, Ybpw_import])
    table = table_helper.select_best_table(kwargs, allowed_when_not, possible_tables)

    filters, groups, show_column = query_helper.build_filters_and_groups(table, kwargs, exclude=exclude)

    if ignore_zeros:
        filters.append( getattr(table, "val_usd") > 0 )

    results = query_helper.query_table(table, filters=filters, groups=groups, limit=limit, order=order, sort=sort, serialize=serialize)

    if table is Ybp_import:
        stripped_filters, stripped_groups, show_column2 = query_helper.convert_filters(Yp_export, kwargs, remove=['bra_id'])
        stripped_columns = [Yp_export.year, Yp_export.hs_id, Yp_export.pci]
        tmp = query_helper.query_table(Yp_export, columns=stripped_columns, filters=stripped_filters, groups=stripped_groups, limit=limit, order=order, sort=sort, serialize=serialize)
        results["pci"] = tmp

    if serialize or download:
        response = jsonify(results)
        if download:
            response.headers["Content-Disposition"] = "attachment;filename=secex_data.json"
        return response

    return results
