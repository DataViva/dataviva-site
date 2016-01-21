from flask_wtf import Form
from wtforms import HiddenField

class DownloadForm(Form):
    output_format = HiddenField('output_format', id="output_format")
    data = HiddenField('data', id="data")
    title = HiddenField('title', id="title")
    downloadToken = HiddenField('downloadToken', id="downloadToken")
