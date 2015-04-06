from flask import Response, request
from dataviva.attrs.models import Bra

def add_ibge_id(header, data):
    bras = Bra.query.all()
    bra_lookup = {b.id : b.id_ibge for b in bras}

    bra_idx = header.index("bra_id")
    header.append("ibge_id")
    for item in data:
        ibge_id = bra_lookup[item[bra_idx]]
        item.append(ibge_id)
    return header, data

def gen_csv(raw_data, dataset):
    header = raw_data["headers"]
    data = raw_data["data"]
    all_rows = [header] + data

    if "bra_id" in header:
        header, data = add_ibge_id(header, data)

    def generate():
        for row in all_rows:
            yield ','.join(map(str, row)) + '\n'
    response = Response(generate(), mimetype='text/csv')
    response.headers["Content-Disposition"] = "attachment; filename={}_data.csv".format(dataset)
    return response

def is_download():
    return bool(request.args.get('download', False))
