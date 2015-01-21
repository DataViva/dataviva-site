from flask import Blueprint, request, jsonify
from dataviva import db
from dataviva.secex_export.models import Yb_secex, Yw, Yp, Ybw, Ybp, Ypw, Ybpw
from dataviva.utils import table_helper, query_helper
from dataviva.utils.gzip_data import gzipped
from dataviva.utils.decorators import cache_api

mod = Blueprint('secex', __name__, url_prefix='/secex')

@mod.route('_export/<year>/<bra_id>/<hs_id>/<wld_id>/')
@mod.route('/<year>/<bra_id>/<hs_id>/<wld_id>/')
@gzipped
@cache_api('secex_export')
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

    allowed_when_not, possible_tables = table_helper.prepare(['bra_id', 'hs_id', 'wld_id'], [Yb_secex, Yw, Yp, Ybw, Ybp, Ypw, Ybpw])
    table = table_helper.select_best_table(kwargs, allowed_when_not, possible_tables)

    filters, groups, show_column = query_helper.build_filters_and_groups(table, kwargs, exclude=exclude)

    if ignore_zeros:
        filters.append( getattr(table, "val_usd") > 0 )

    results = query_helper.query_table(table, filters=filters, groups=groups, limit=limit, order=order, sort=sort, serialize=serialize)

    if table is Ybp:
        stripped_filters, stripped_groups, show_column2 = query_helper.convert_filters(Yp, kwargs, remove=['bra_id'])
        stripped_columns = [Yp.year, Yp.hs_id, Yp.pci]
        tmp = query_helper.query_table(Yp, columns=stripped_columns, filters=stripped_filters, groups=stripped_groups, limit=limit, order=order, sort=sort, serialize=serialize)
        results["pci"] = tmp

    if serialize or download:
        response = jsonify(results)
        if download:
            response.headers["Content-Disposition"] = "attachment;filename=secex_data.json"
        return response

    return results
