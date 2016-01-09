from flask import Response, request
from dataviva.api.attrs.models import Bra

def add_ibge_id(header, data):
    bras = Bra.query.all()
    bra_lookup = {b.id : b.id_ibge for b in bras}

    bra_idx = header.index("bra_id")
    header.append("ibge_id")
    for item in data:
        ibge_id = bra_lookup[item[bra_idx]]
        item.append(ibge_id)
    return header, data

def add_pci(header, raw_pci, data):
    header.append("pci")
    year_idx = header.index("year")
    hs_idx = header.index("hs_id")

    pci_headers = raw_pci["headers"]
    y_i = pci_headers.index("year")
    hs_i = pci_headers.index("hs_id")
    pci_i = pci_headers.index("pci")

    pci_lookup = {"{}{}".format(itm[y_i], itm[hs_i]) : itm[pci_i] for itm in raw_pci["data"]}

    for item in data:
        pci_id = "{}{}".format(item[year_idx], item[hs_idx])
        if pci_id in pci_lookup:
            item.append( pci_lookup[pci_id] )
        else:
            item.append(None)
    return header, data

def gen_csv(raw_data, dataset):
    header = raw_data["headers"]
    data = raw_data["data"]
    all_rows = [header] + data

    if "bra_id" in header:
        header, data = add_ibge_id(header, data)

    if "pci" in raw_data:
        header, data = add_pci(header, raw_data["pci"], data)

    def generate():
        for row in all_rows:
            yield ','.join(map(str, row)) + '\n'
    response = Response(generate(), mimetype='text/csv')
    response.headers["Content-Disposition"] = "attachment; filename={}_data.csv".format(dataset)
    return response

def is_download():
    return bool(request.args.get('download', False))
