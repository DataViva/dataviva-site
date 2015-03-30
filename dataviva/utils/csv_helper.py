from flask import Response, request

def gen_csv(raw_data, dataset):
    header = raw_data["headers"]
    data = raw_data["data"]
    all_rows = [header] + data
    def generate():
        for row in all_rows:
            yield ','.join(map(str, row)) + '\n'
    response = Response(generate(), mimetype='text/csv')
    response.headers["Content-Disposition"] = "attachment; filename={}_data.csv".format(dataset)
    return response

def is_download():
    return bool(request.args.get('download', False))
