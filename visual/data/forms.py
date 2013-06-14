from flask.ext.wtf import Form, HiddenField
from flask.ext.wtf import Required

class DownloadForm(Form):
    output_format = HiddenField('output_format', id="output_format")
    data = HiddenField('data', id="data")
    title = HiddenField('title', id="title")
